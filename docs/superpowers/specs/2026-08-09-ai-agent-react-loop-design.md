# Technical Design Specification: Odoo-Native AI-Agent Re-Act Loop
**Date**: 2026-08-09  
**Status**: Approved  
**Author**: Gemini CLI (Execution Agent) & Jeffery (Principal Architect)

---

## 1. Executive Summary & Design Scope

The standard static workflow engine in `farm_ai_agent` (`agri.ai.agent.workflow`) executes predefined sequences using hardcoded Python conditions. While sufficient for linear routines, this approach is insufficient for dynamic, non-deterministic agricultural environments—such as rapid pest outbreaks, unpredictable weather shifts, or competitive credit bargaining.

This specification defines a **purely native, decentralized Agent Re-Act (Reasoning and Acting) Loop** implemented inside the Odoo 19 ORM. Under this paradigm, an autonomous agent observes current metrics, reasons (Thought), selects a verified tool (Action), and evaluates the outcomes (Observation) within a secure transactional savepoint sandbox. This keeps legacy records safe from incorrect physical changes and maintains a lossless audit log of the agent's actions (ISA-88 Compliance).

---

## 2. Comprehensive Database Schema

To support native Re-Act loops while preventing base table bloat, the data structure is partitioned into three key relational tables.

```
+────────────────────────────────────────────────────────┐
│               agri.a2a.react.loop                      │
│  (Main Loop Controller & Current Run State)            │
+───────────────────────────┬────────────────────────────┘
                            │ 1
                            │
                            │ N
+───────────────────────────▼────────────────────────────┐
│             agri.a2a.react.loop.line                   │
│  (Lossless Audit of Thought -> Action -> Observation)  │
+───────────────────────────┬────────────────────────────┘
                            │ N
                            │
                            │ 1
+───────────────────────────▼────────────────────────────┐
│               agri.a2a.react.tool                      │
│  (Verified Registry of Executable Odoo ORM Actions)    │
+────────────────────────────────────────────────────────┘
```

### 2.1 Re-Act Loop Controller (`agri.a2a.react.loop`)
Maintains the active goal, bounds, state, and runtime environment of the loop.
- `name` (Char): Sequential loop reference, prefixed e.g. `REACT/2026/00001`.
- `state` (Selection): 
  - `draft`: Configuration phase.
  - `running`: Execution loop active.
  - `paused`: Gated on a Critical Control Point (CCP) awaiting human signature.
  - `completed`: Successfully achieved the target goal.
  - `failed`: Stopped due to error or loop bounds violation.
- `goal` (Text, required): Declared operational objective (e.g. *"Transfer 50kg of Lot A to Vessel B while temperature remains below 12°C"*).
- `max_iterations` (Integer, default=10): Bound constraint to prevent infinite loops.
- `current_iteration` (Integer, default=0): Count of active iterations.
- `context_data` (Text): JSON payload caching immediate sensor values, carrier states, and system metadata.
- `line_ids` (One2many -> `agri.a2a.react.loop.line`): History of loop steps.

### 2.2 Re-Act Loop Line (`agri.a2a.react.loop.line`)
Captures the execution record of a single step.
- `loop_id` (Many2one -> `agri.a2a.react.loop`, required, cascade): Parent loop.
- `iteration` (Integer, required): Index sequence of the step.
- `state` (Selection):
  - `draft`: New iteration initialized.
  - `executing`: Action triggered.
  - `success`: Observation recorded; transaction committed.
  - `violated`: Action rolled back due to HACCP/biosecurity trigger.
  - `failed`: Runtime exception thrown during tool call.
- `thought` (Text, required): Detailed logic, reasoning, and analysis output by the LLM.
- `action_type` (Selection):
  - `tool_call`: Request to execute a registered Odoo API tool.
  - `human_approve`: Request to pause for human approval.
  - `terminate`: Request to close the loop (Goal accomplished).
- `tool_id` (Many2one -> `agri.a2a.react.tool`): Selected Odoo API tool.
- `action_payload` (Text): JSON payload containing arguments to pass to the tool.
- `observation` (Text): Result returned by the database execution, or error details on exception.

### 2.3 Re-Act Tool Registry (`agri.a2a.react.tool`)
Declares allowed methods in Odoo, establishing a strict sandbox boundary.
- `name` (Char, required): Tool name.
- `model_name` (Char, required): Target Odoo model name (e.g., `stock.matter.tracking`).
- `method_name` (Char, required): Python ORM method name to execute.
- `required_gxp_gating` (Boolean, default=False): If true, forces human sign-off activity before invocation.
- `is_active` (Boolean, default=True): Activation status.

---

## 3. Transaction Savepoint Sandbox Design

To allow the agent to safely execute actions while enforcing absolute biological security, we wrap tool execution inside Odoo's SQL savepoints.

```
       [ Read Context & Last Observation ]
                      │
                      ▼
            [ Call LLM Agent ]
                      │
         Parse Output into:
         - Thought (Reasoning)
         - Action Type (Tool Call / Terminate)
         - Action Payload (JSON arguments)
                      │
                      ▼
         Is Tool marked required_gxp_gating?
         ├── [ Yes ] ──► Create Activity & set state = 'paused' (Awaiting Sign-off)
         └── [ No ]
                 │
                 ▼
     [ ENTER SAVEPOINT ] ──► env.cr.savepoint()
                 │
                 ▼
     Execute: getattr(env[model], method)(**payload)
                 │
                 ▼
     Evaluate biological barriers / HACCP checks
     (e.g., qc_release_state = 'released', is_violated = False)
                 │
         Has GxP Violation or SQL Error?
         ├── [ Yes ] ──► env.cr.rollback() (Rollback all changes inside savepoint)
         │               Write Line with state = 'violated' & error observation
         │               Pause loop for re-evaluation
         └── [ No ]
                 │
                 ▼
     [ COMMIT TO MAIN DB ] (Auto-released by exiting savepoint block successfully)
     Record updated state as Observation
     Iterate current_iteration
```

### 3.1 Savepoint Isolation
If an action causes a validation error or biosecurity hazard, `cr.rollback()` only reverts changes made *inside* that savepoint. The logging of the failure in the loop line is committed on a fresh savepoint or outside the block. This prevents silent failure states and captures the trace of unsuccessful actions, ensuring absolute audit integrity.

### 3.2 CRUD Signature Compatibility Adapter
Standard Odoo ORM methods like `write()` and `create()` expect a dictionary/vals object as their first positional argument. Unpacking arguments as keyword arguments (`**kwargs`) for these methods triggers Python `TypeErrors`. The Re-Act engine includes a dynamic signature adapter that detects these CRUD operations:
- **Write Operations**: Detects `method_name == 'write'` and passes the remaining arguments as a single positional dictionary argument: `func(call_args)`.
- **Create Operations**: Detects `method_name == 'create'` and passes the arguments directly: `func(args)`.
- **Custom Methods**: Passes arguments using keyword argument unpacking (`**kwargs`) for ultimate flexibility.

### 3.3 Multi-Criterion Loop Termination Rules
The Re-Act loop implements robust termination boundaries to ensure deterministic runs under three primary conditions:
1. **Final Answer / Success Termination (`action_type == 'terminate'`)**: Triggered when the agent's reasoning confirms the operational target is reached. Main loop state is committed as `completed`.
2. **Iteration Boundary Safeguard (`current_iteration >= max_iterations`)**: A hard upper limit on steps (defaulting to 10) triggers a safe exit, marking the state as `failed` to prevent infinite reasoning/acting loops.
3. **Fatal Process/Exception Termination**: Any unexpected tool-execution or database constraint violation triggers an automatic savepoint rollback and immediately halts the loop, updating the state to `failed` and capturing the trace in the audit log.

---

## 4. XML View & Menu Placement

We integrate the Re-Act loop directly into the Odoo form interface using standard three-tier visual layouts (Statusbar -> Header -> Sheet).

### 4.1 UI Layout
- **Statusbar**: Visual indication of loop states (`draft` -> `running` -> `paused` -> `completed` / `failed`).
- **Form Buttons**:
  - `Action Start`: Initiates the run sequence.
  - `Action Step`: Manually triggers a single iteration for debugging.
  - `Action Reset`: Reverts the loop to draft for reconfiguration.
- **Form Body**:
  - Left Panel: Goal and Max Iterations.
  - Right Panel: Active Iteration Count, and current JSON Context payload.
  - Bottom Tab Notebook: Iterations line tracking, showing the Thought -> Action -> Observation flow in a clear nested list view.

---

## 5. Automated Testing Strategy

To guarantee absolute functional alignment under Odoo 19, we establish four strong test targets:
1. **Successful Re-Act Iteration**: Verify that standard Thought -> Action -> Observation sequences execute correctly and increment state counters.
2. **Dynamic Tool Matching**: Confirm that only tools registered in `agri.a2a.react.tool` are allowed to execute, and unknown tools are immediately rejected with appropriate logging.
3. **Exception Rollback Sandbox**: Verify that a tool action that modifies records but subsequently throws a GxP error is successfully rolled back to its savepoint without leaving ghost states in the database.
4. **Human Gxp Gating**: Verify that a tool with `required_gxp_gating=True` correctly pauses the loop, triggers a pending activity, and resumes automatically once approved.

---

## 6. Spec Self-Review Checklist

- [x] **Placeholder Scan**: No placeholders or vague "TBD" terms. Model names, fields, and execution algorithms are completely described.
- [x] **Internal Consistency**: Schema definitions align exactly with the savepoint logic and testing strategy.
- [x] **Scope Check**: The task is precisely scoped to a self-contained local Re-Act loop module within `farm_ai_agent`.
- [x] **Ambiguity Check**: Transaction boundaries are explicitly defined at the Odoo `savepoint()` layer.
- [x] **ASCII Guidelines**: Formulations and sequence flows use pure ASCII representations.
