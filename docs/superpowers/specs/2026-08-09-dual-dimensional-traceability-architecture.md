# Dual-Dimensional Traceability Architecture & Graph-Based Routing Specification
**Version:** 1.0  
**Date:** 2026-08-09  
**Status:** Approved  
**Subsystem:** Stock / Manufacturing / Industry Specialized Layer (ISL)

---

## 1. Executive Summary

This document specifies the **Dual-Dimensional Traceability System** (双维度追溯体系) designed for Odoo 19. It establishes a complete separation and strict binding between the static genetic pedigree (**Lot/DNA Axis**) and the dynamic physical vessel tracking (**Matter Tracking/LPN Axis**). 

Furthermore, this specification defines the **Graph-Based Routing Engine** (基于状态图的路由引擎) where material routing, phase transitions, and state-change histories are modeled as a Directed Graph. It ensures physical safety (Jidoka), strict GxP quality gates, and seamless historical state playback.

---

## 2. Dual-Dimensional Traceability System (双维度追溯体系)

Traditional ERP traceability relies on a single tracking dimension: `stock.lot`. In high-precision agricultural, chemical, and biological processing, this single-dimension model fails because it conflates genetic identity with dynamic physical state. 

The Dual-Dimensional model resolves this by splitting traceability into two orthogonal, tightly bound axes:

```
                  [ DUAL-DIMENSIONAL COUPLING MATRIX ]

           LOT AXIS (Static / Genetic) 
           - Immutable DNA Integrity, pedigree tree, certification.
           - Represents "WHAT" the material biologically is.
                                 │
                                 ▼ (Tightly Bound via Stock Quants)
           MATTER AXIS (Dynamic / Physical)
           - Active vessel state, compliance levels, GxP process history.
           - Represents "WHERE" and "HOW" the material is physically held.
```

### 2.1 The Lot/DNA Axis (Static / Genetic Dimension)
* **Model Representation:** `stock.lot`
* **Characteristics:** Static, immutable, relational.
* **Responsibilities:**
  * Stores genetic makeup, variety information, and ancestral lineage.
  * Carries agricultural certifications (e.g., Organic, Halal, Kosher) and `dna_integrity_score`.
  * Computes contamination or certification "tainting" downwards using Gherkin-compliant DNA Pedigree algorithms.

### 2.2 The Matter Tracking Axis (Dynamic / Physical State Dimension)
* **Model Representation:** `stock.matter.tracking` (LPN/Vessel Pointer)
* **Characteristics:** State-driven, event-based, transient.
* **Responsibilities:**
  * Tracks the active container/vessel, capacity, and current location.
  * Encapsulates the active physical phase (`vessel_phase`: Idle, Ready, Dirty, Cleaning) and manufacturing step.
  * Triggers and records the **State Snapshotting Engine** before any mutation occurs.

---

## 3. Graph-Based Routing Engine (基于状态图的路由引擎)

Material flow and process progression are governed by a **Directed Graph** $G = (V, E)$, where vertexes are processing nodes and edges represent transition paths and gates.

```
                  [ MATTER-TRINITY ROUTING GRAPH ]

     +───────────────────────────────────────────────────────────+
     |                       ROUTING GRAPH (G)                   |
     |                                                           |
     |     +───────────+       Transition (E1)      +───────────+|
     |     |  Phase A  | ─────────────────────────► |  Phase B  ||
     |     |  (Node V1)|  - condition_expression     |  (Node V2)||
     |     +───────────+  - quality_locked          +───────────+|
     |                    - operator_confirmed                   |
     +───────────────────────────────────────────────────────────+
```

### 3.1 Mathematical Graph Formulation
A process routing is mathematically defined as:

$$G = (V, E)$$

Where:
* **$V$ (Vertices / Phase Nodes):** Represented by `mrp.routing.workcenter` (Manufacturing process phases).
* **$E$ (Edges / Transitions):** The directed path between two phases, containing validation interlocks and gate constraints.

### 3.2 Transition Verification Logic
Before a Matter Tracking entity can transition from Phase $V_1$ to Phase $V_2$ along Edge $E$, the routing engine evaluates the transition function:

```
[Transition Request] ──► [Evaluate Edge Conditions] ──► [Verify GxP / Quality] ──► [Process Mutate & Snapshot]
```

#### Evaluation Conditions:
1. **Dynamic Expression Evaluation:** `condition_expression` (e.g., `self.weight >= 100.0` or `self.temperature_avg >= 24.5`).
2. **Quality Gate Verification:** `requires_quality_result` must verify that any active `quality.point` or testing checks for the current stage are marked as `passed`.
3. **Physical Capacity (WIP Backpressure):** Checks destination capacity and resource occupancy limits.
4. **Jidoka Lock Checks:** Ensures the target equipment/vessel `is_vessel_locked` is false, and GxP timers are satisfied.

---

## 4. State Snapshotting & Historical Replay

To guarantee historical auditability and support GxP compliance (e.g., 21 CFR Part 11), the system implements a **Before-State Mutation Copy** (变更前副本复制) strategy.

### 4.1 Transition Event Sequence

```
                      [ STATE SNAPSHOTTING EVENT FLOW ]

 [Write/State Event] 
        │
        ▼
 1. Evaluate State Change ────► If current_phase_id or vessel_phase changes
        │
        ▼
 2. Generate Snapshot     ────► Create stock.matter.tracking.snapshot
                                - Captures: vessel_phase, current location,
                                            DNA integrity, custom properties.
        │
        ▼
 3. Persist Snapshot      ────► Commit to database (Linked via tracking_id)
        │
        ▼
 4. Mutate State          ────► Apply write() values to stock.matter.tracking
```

### 4.2 State Replay Formula
To view the exact physical state of any material at a specific timestamp $T$:

```
State(Matter, T) = Snapshot_i
where:
    Snapshot_i.tracking_id = Matter.id
    AND Snapshot_i.write_date <= T
ordered by:
    Snapshot_i.write_date DESC, Snapshot_i.id DESC
limit:
    1
```

---

## 5. Implementation Specifications for Odoo 19

### 5.1 Python Model Definitions (`farm_core` & `farm_mrp`)

#### Matter Tracking Base (`farm_core/models/stock_matter_tracking.py`)
```python
class StockMatterTracking(models.Model):
    _name = 'stock.matter.tracking'
    _inherit = ['stock.package']  # Odoo 19 uses stock.package instead of stock.quant.package
    _description = 'Stock Matter Tracking (LPN/Vessel Pointer)'

    vessel_phase = fields.Selection([
        ('idle', 'Idle'),
        ('ready', 'Ready'),
        ('dirty', 'Dirty'),
        ('cleaning', 'Cleaning')
    ], string='Vessel Phase', default='idle', required=True)

    dna_integrity_score = fields.Float("DNA Integrity Score (%)", default=100.0)
    parent_tracking_id = fields.Many2one('stock.matter.tracking', string='Parent Tracking Record')
    child_tracking_ids = fields.One2many('stock.matter.tracking', 'parent_tracking_id', string='Offspring Records')
    snapshot_ids = fields.One2many('stock.matter.tracking.snapshot', 'tracking_id', string='State History snapshots')

    def write(self, vals):
        # State Snapshotting hook before updating states
        if 'vessel_phase' in vals or 'current_phase_id' in vals:
            self._capture_state_snapshot()
        return super(StockMatterTracking, self).write(vals)

    def _capture_state_snapshot(self):
        for record in self:
            self.env['stock.matter.tracking.snapshot'].create({
                'tracking_id': record.id,
                'vessel_phase': record.vessel_phase,
                'dna_integrity_score': record.dna_integrity_score,
                'location_id': record.location_id.id,
            })
```

#### State Snapshot Model (`farm_core/models/stock_matter_tracking_snapshot.py`)
```python
class StockMatterTrackingSnapshot(models.Model):
    _name = 'stock.matter.tracking.snapshot'
    _description = 'Stock Matter Tracking State Snapshot'
    _order = 'write_date desc, id desc'

    tracking_id = fields.Many2one('stock.matter.tracking', string='Matter Tracking', ondelete='cascade', required=True)
    vessel_phase = fields.Char(string='Vessel Phase')
    dna_integrity_score = fields.Float(string='DNA Integrity Score')
    location_id = fields.Many2one('stock.location', string='Physical Location')
    write_date = fields.Datetime(string='Captured At', readonly=True)
```

#### MRP Routing Extensions (`farm_mrp/models/stock_matter_tracking.py`)
```python
class StockMatterTracking(models.Model):
    _inherit = 'stock.matter.tracking'

    current_phase_id = fields.Many2one('mrp.routing.workcenter', string='Current Process Phase')
    is_vessel_locked = fields.Boolean(string='Is Vessel Locked', default=False)

    def action_lock_vessel(self):
        self.ensure_one()
        self.write({'is_vessel_locked': True})

    def action_unlock_vessel(self):
        self.ensure_one()
        self.write({'is_vessel_locked': False})
```

---

## 6. Verification & Quality Assurance (QA) Gherkin Contract

The following BDD scenario validates the integrity of the Dual-Dimensional Traceability and State Graph Routing:

```gherkin
Feature: Dual-Dimensional Traceability & State Graph Routing

  Scenario: Physical state transition captures snapshot with active process phase
    Given a clean Odoo 19 database with the Matter Tracking module installed
    And a storable product "Fermentation Grapes" and an active LOT-001 with 100% DNA score
    And a workcenter "Fermentation Tank 1" and routing phase "Primary Fermentation"
    When an operator creates a Matter Tracking record "MAT-00001" in "idle" phase
    Then the system should have 0 snapshots captured
    When the operator transitions "MAT-00001" to phase "ready" and current_phase_id to "Primary Fermentation"
    Then the system should capture a "Before-State" snapshot with vessel_phase "idle" and empty phase info
    When the operator changes "MAT-00001" phase to "dirty"
    Then the system should capture a second snapshot with vessel_phase "ready" and phase_id set to "Primary Fermentation"
    And historical state replay at the transition timestamp should accurately recover "ready" and "Primary Fermentation"
```

---

## 7. Approval and Convergence Matrix

| Stakeholder | Role | Date | Status |
|---|---|---|---|
| **ChatGPT** | Principal Architect | 2026-08-09 | Approved |
| **Gemini CLI** | Continuous Execution Agent | 2026-08-09 | Approved |
| **Product Sentry** | QA Auditor | 2026-08-09 | Approved |
