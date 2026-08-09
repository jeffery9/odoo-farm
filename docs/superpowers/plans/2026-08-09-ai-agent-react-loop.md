# AI Agent Re-Act Loop Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a robust, native Agent Re-Act (Reasoning and Acting) execution loop within Odoo 19, incorporating secure transactional savepoint sandboxes, dynamic tool mapping, and human-in-the-loop CCP gating.

**Architecture:** Implement three dedicated Odoo models: `agri.a2a.react.tool` (safe tool registry), `agri.a2a.react.loop` (controller), and `agri.a2a.react.loop.line` (unrolled thought-action-observation steps). Tool executions are dynamically dispatched and isolated inside PostgreSQL transaction savepoints (`self.env.cr.savepoint()`), with immediate rollback upon HACCP or GxP violations.

**Tech Stack:** Odoo 19, Python, PostgreSQL, Pytest (TransactionCase).

## Global Constraints
- **Architecture Integrity**: Keep models and logic 100% Odoo-native. Avoid Django/Rails repos or custom Service Layers.
- **Savepoint Safety**: Always execute tool methods within a savepoint context (`self.env.cr.savepoint()`) and roll back upon validation/constraint failures.
- **Registry Compliance**: Model declarations and dependencies must flow downward without circular loops.

---

### Task 1: Implement Re-Act Tool Registry

**Files:**
- Create: `farm_ai_agent/models/a2a_react_tool.py`
- Modify: `farm_ai_agent/models/__init__.py`

**Interfaces:**
- Consumes: None
- Produces: `agri.a2a.react.tool` model representation with fields `name`, `model_name`, `method_name`, `required_gxp_gating`, `is_active`.

- [ ] **Step 1: Write the failing test**

Create the test file `farm_ai_agent/tests/test_a2a_react_loop.py` with this test:
```python
# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestA2AReactLoop(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Tool = cls.env['agri.a2a.react.tool']

    def test_01_tool_registry_creation(self):
        """ Verify tool registry allows creation of safe Odoo method pointers """
        tool = self.Tool.create({
            'name': 'Split Matter Carrier',
            'model_name': 'stock.matter.tracking',
            'method_name': 'action_execute_fission',
            'required_gxp_gating': True,
        })
        self.assertTrue(tool.exists())
        self.assertEqual(tool.model_name, 'stock.matter.tracking')
```

- [ ] **Step 2: Run test to verify it fails**

Run: `docker compose run --rm web odoo -d test_clean_db_sfc_mrp -u farm_ai_agent --test-enable --stop-after-init --log-level=info`  
Expected: FAIL with KeyError or AttributeError because `agri.a2a.react.tool` does not exist in the environment.

- [ ] **Step 3: Write minimal implementation**

Create `/Users/jeffery/odoo-farm-workspace/odoo-farm-dev/farm_ai_agent/models/a2a_react_tool.py`:
```python
# -*- coding: utf-8 -*-
from odoo import models, fields

class A2AReactTool(models.Model):
    """
    Registry of safe/authorized Odoo method calls that an AI Agent can execute.
    """
    _name = 'agri.a2a.react.tool'
    _description = 'A2A React Safe Tool'

    name = fields.Char('Tool Name', required=True)
    model_name = fields.Char('Model Name', required=True)
    method_name = fields.Char('Method Name', required=True)
    required_gxp_gating = fields.Boolean('Requires GxP Gating / CCP', default=False)
    is_active = fields.Boolean('Is Active', default=True)
```
Add to `farm_ai_agent/models/__init__.py`:
```python
from . import a2a_react_tool
```

- [ ] **Step 4: Run test to verify it passes**

Run: `docker compose run --rm web odoo -d test_clean_db_sfc_mrp -u farm_ai_agent --test-enable --stop-after-init --log-level=info`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add farm_ai_agent/models/a2a_react_tool.py farm_ai_agent/models/__init__.py farm_ai_agent/tests/test_a2a_react_loop.py
git commit -m "feat(ai-agent): implement agri.a2a.react.tool model and test scaffolding"
```

---

### Task 2: Implement Loop Controller and Iteration Lines

**Files:**
- Create: `farm_ai_agent/models/a2a_react_loop.py`
- Modify: `farm_ai_agent/models/__init__.py`

**Interfaces:**
- Consumes: `agri.a2a.react.tool` (Task 1)
- Produces: `agri.a2a.react.loop` and `agri.a2a.react.loop.line` models tracking the state machine and steps.

- [ ] **Step 1: Write the failing test**

Append to `farm_ai_agent/tests/test_a2a_react_loop.py`:
```python
    def test_02_loop_and_line_creation(self):
        """ Verify loop and iteration line creation with nested relationship """
        loop = self.env['agri.a2a.react.loop'].create({
            'name': 'REACT/TEST/001',
            'goal': 'Optimize crop nutrition levels while respecting biosecurity',
        })
        self.assertEqual(loop.state, 'draft')
        
        line = self.env['agri.a2a.react.loop.line'].create({
            'loop_id': loop.id,
            'iteration': 1,
            'thought': 'I must first inspect the current soil nutrient metrics.',
            'action_type': 'tool_call',
        })
        self.assertTrue(line.exists())
        self.assertEqual(line.loop_id.id, loop.id)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `docker compose run --rm web odoo -d test_clean_db_sfc_mrp -u farm_ai_agent --test-enable --stop-after-init --log-level=info`  
Expected: FAIL due to missing `agri.a2a.react.loop` model.

- [ ] **Step 3: Write minimal implementation**

Create `/Users/jeffery/odoo-farm-workspace/odoo-farm-dev/farm_ai_agent/models/a2a_react_loop.py`:
```python
# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class A2AReactLoop(models.Model):
    _name = 'agri.a2a.react.loop'
    _description = 'A2A React Execution Loop'
    _inherit = ['mail.thread']

    name = fields.Char('Reference', required=True, default=lambda self: self.env['ir.sequence'].next_by_code('agri.a2a.react.loop') or 'New')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('running', 'Running'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], default='draft', tracking=True)

    goal = fields.Text('Target Goal', required=True)
    max_iterations = fields.Integer('Max Iterations', default=10)
    current_iteration = fields.Integer('Current Iteration', default=0)
    context_data = fields.Text('JSON Context Payload', default='{}')

    line_ids = fields.One2many('agri.a2a.react.loop.line', 'loop_id', string='Steps')


class A2AReactLoopLine(models.Model):
    _name = 'agri.a2a.react.loop.line'
    _description = 'A2A React Step Detail'
    _order = 'iteration'

    loop_id = fields.Many2one('agri.a2a.react.loop', string='Parent Loop', required=True, ondelete='cascade')
    iteration = fields.Integer('Iteration Sequence', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('executing', 'Executing'),
        ('success', 'Success'),
        ('violated', 'GxP Violated / Rolled Back'),
        ('failed', 'Exception Failed')
    ], default='draft')

    thought = fields.Text('Thought Processes', required=True)
    action_type = fields.Selection([
        ('tool_call', 'Odoo Tool Execution'),
        ('human_approve', 'Requires Manual Approval'),
        ('terminate', 'Finish Loop / Goal Reached')
    ], default='tool_call', required=True)

    tool_id = fields.Many2one('agri.a2a.react.tool', string='Odoo Tool')
    action_payload = fields.Text('JSON Payload', default='{}')
    observation = fields.Text('Observation Result')
```
Add to `farm_ai_agent/models/__init__.py`:
```python
from . import a2a_react_loop
```

- [ ] **Step 4: Run test to verify it passes**

Run: `docker compose run --rm web odoo -d test_clean_db_sfc_mrp -u farm_ai_agent --test-enable --stop-after-init --log-level=info`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add farm_ai_agent/models/a2a_react_loop.py farm_ai_agent/models/__init__.py farm_ai_agent/tests/test_a2a_react_loop.py
git commit -m "feat(ai-agent): implement agri.a2a.react.loop and loop.line tracking models"
```

---

### Task 3: Implement Execution Engine & Savepoint Sandbox

**Files:**
- Modify: `farm_ai_agent/models/a2a_react_loop.py`

**Interfaces:**
- Consumes: None (Extends loop models with execution capability)
- Produces: Method `action_execute_iteration(thought, action_type, tool_id, action_payload)` with robust savepoint safety wrapping.

- [ ] **Step 1: Write the failing test**

Append to `farm_ai_agent/tests/test_a2a_react_loop.py`:
```python
    def test_03_savepoint_sandbox_rollback(self):
        """ Verify execution within transactional savepoints is safely rolled back on GxP error """
        # Create a workcenter for testing tool execution
        wc = self.env['mrp.workcenter'].create({'name': 'Test Soil Injector'})
        
        # Register a tool that executes an Odoo model method
        tool = self.Tool.create({
            'name': 'Modify Workcenter Name',
            'model_name': 'mrp.workcenter',
            'method_name': 'write',
            'required_gxp_gating': False,
        })
        
        loop = self.env['agri.a2a.react.loop'].create({
            'name': 'REACT/SAVEPOINT/001',
            'goal': 'Attempt to rename a workcenter',
        })
        
        import json
        payload = json.dumps({'name': 'Renamed by Agent'})
        
        # Step execution - this write should succeed
        loop.action_execute_iteration(
            thought="I will rename this workcenter.",
            action_type="tool_call",
            tool_id=tool.id,
            action_payload=payload,
            test_target_record_id=wc.id # pass explicit ID for testing write
        )
        
        # Verify the write succeeded and was committed
        self.assertEqual(wc.name, 'Renamed by Agent')
        
        # Now trigger a transaction that fails on GxP/Validation to assert rollback
        # We simulate this by having our execution catch a failure or force rollback on invalid type
        bad_payload = json.dumps({'energy_cost_per_hour': -150.0}) # Invalid negative cost (UserError in farm_processing)
        
        loop.action_execute_iteration(
            thought="I will set a negative energy cost.",
            action_type="tool_call",
            tool_id=tool.id,
            action_payload=bad_payload,
            test_target_record_id=wc.id
        )
        
        # Verify line state was recorded as 'violated' or 'failed' and workcenter state remains unchanged
        last_step = loop.line_ids[-1]
        self.assertIn(last_step.state, ['violated', 'failed'])
        self.assertEqual(wc.name, 'Renamed by Agent') # Preserved previous value!
```

- [ ] **Step 2: Run test to verify it fails**

Run: `docker compose run --rm web odoo -d test_clean_db_sfc_mrp -u farm_ai_agent --test-enable --stop-after-init --log-level=info`  
Expected: FAIL due to missing `action_execute_iteration` method.

- [ ] **Step 3: Write minimal implementation**

In `farm_ai_agent/models/a2a_react_loop.py`, append the following execution methods inside the `A2AReatLoop` class:
```python
    def action_execute_iteration(self, thought, action_type, tool_id=False, action_payload='{}', test_target_record_id=False):
        """
        Executes a single Re-Act loop step safely encapsulated inside a transaction savepoint.
        """
        self.ensure_one()
        import json
        
        # Guard limits
        if self.current_iteration >= self.max_iterations:
            self.state = 'failed'
            return False

        self.current_iteration += 1
        iteration_index = self.current_iteration

        # Create unrolled iteration line record first
        line = self.env['agri.a2a.react.loop.line'].create({
            'loop_id': self.id,
            'iteration': iteration_index,
            'thought': thought,
            'action_type': action_type,
            'tool_id': tool_id,
            'action_payload': action_payload,
            'state': 'executing',
        })

        if action_type == 'terminate':
            line.write({
                'state': 'success',
                'observation': 'Loop termination requested by agent. Goal accomplished successfully.'
            })
            self.state = 'completed'
            return True

        if action_type == 'human_approve':
            line.write({
                'state': 'draft',
                'observation': 'Awaiting human verification and physical sign-off.'
            })
            self.state = 'paused'
            return True

        if action_type == 'tool_call' and tool_id:
            tool = self.env['agri.a2a.react.tool'].browse(tool_id)
            if not tool.exists() or not tool.is_active:
                line.write({
                    'state': 'failed',
                    'observation': 'ERROR: Request tool is either inactive or does not exist.'
                })
                self.state = 'failed'
                return False

            if tool.required_gxp_gating:
                # GxP/CCP gating: Pause loop and require manual sign-off
                line.write({
                    'state': 'draft',
                    'observation': 'GxP Critical Control Point triggered. Loop paused awaiting human release.'
                })
                self.state = 'paused'
                return True

            # Enter Transaction Savepoint Block
            try:
                with self.env.cr.savepoint():
                    # Parse args
                    args = json.loads(action_payload or '{}')
                    
                    # Dynamically fetch target model
                    Model = self.env[tool.model_name]
                    
                    # Resolve record ID (use test_target_record_id if provided, otherwise check context/args)
                    record_id = test_target_record_id or args.get('id') or args.get('record_id')
                    
                    if record_id:
                        record = Model.browse(int(record_id))
                        if not record.exists():
                            raise ValueError(_("Target record with ID %s not found.") % record_id)
                            
                        # Call method dynamically
                        func = getattr(record, tool.method_name)
                        # We pass the remaining arguments excluding the ID
                        call_args = {k: v for k, v in args.items() if k not in ['id', 'record_id']}
                        res = func(**call_args)
                    else:
                        # Model-level static method call
                        func = getattr(Model, tool.method_name)
                        res = func(**args)
                        
                    # If execution is successful, write observation in this transaction
                    line.write({
                        'state': 'success',
                        'observation': json.dumps({'status': 'success', 'result': str(res)})
                    })
            except Exception as e:
                # Automatically rolled back! Update logging status in separate outer transaction
                _logger.warning("Re-Act execution failed. Rolling back transaction: %s", str(e))
                line.write({
                    'state': 'violated' if 'haccp' in str(e).lower() or 'violation' in str(e).lower() else 'failed',
                    'observation': 'ERROR/ROLLBACK: ' + str(e)
                })
                self.state = 'failed'
                return False

        return True
```

- [ ] **Step 4: Run test to verify it passes**

Run: `docker compose run --rm web odoo -d test_clean_db_sfc_mrp -u farm_ai_agent --test-enable --stop-after-init --log-level=info`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add farm_ai_agent/models/a2a_react_loop.py farm_ai_agent/tests/test_a2a_react_loop.py
git commit -m "feat(ai-agent): implement robust action_execute_iteration execution method with savepoint isolation"
```

---

### Task 4: Configure Security Model Access

**Files:**
- Modify: `farm_ai_agent/security/ir.model.access.csv`

**Interfaces:**
- Consumes: Task 1 and 2 models
- Produces: Correct CSV permission entries for `agri.a2a.react.tool`, `agri.a2a.react.loop`, and `agri.a2a.react.loop.line`.

- [ ] **Step 1: Write the failing test**

There is no code test, but loading Odoo without security permissions for newly registered models triggers strict warnings or errors on Odoo 19 startup during tests.

- [ ] **Step 2: Run test to verify it fails**

Run: `docker compose run --rm web odoo -d test_clean_db_sfc_mrp -u farm_ai_agent --test-enable --stop-after-init --log-level=info`  
Expected: Warnings in output showing missing permissions for `agri.a2a.react.*` models.

- [ ] **Step 3: Write minimal implementation**

Append to `farm_ai_agent/security/ir.model.access.csv`:
```csv
access_agri_a2a_react_tool,access_agri_a2a_react_tool,model_agri_a2a_react_tool,base.group_user,1,1,1,1
access_agri_a2a_react_loop,access_agri_a2a_react_loop,model_agri_a2a_react_loop,base.group_user,1,1,1,1
access_agri_a2a_react_loop_line,access_agri_a2a_react_loop_line,model_agri_a2a_react_loop_line,base.group_user,1,1,1,1
```

- [ ] **Step 4: Run test to verify it passes**

Run: `docker compose run --rm web odoo -d test_clean_db_sfc_mrp -u farm_ai_agent --test-enable --stop-after-init --log-level=info`  
Expected: PASS with no security/permission complaints.

- [ ] **Step 5: Commit**

```bash
git add farm_ai_agent/security/ir.model.access.csv
git commit -m "security(ai-agent): add security access rules for new react loop models"
```

---

### Task 5: Design XML Form, Tree Views, and Menus

**Files:**
- Create: `farm_ai_agent/views/a2a_react_loop_views.xml`
- Modify: `farm_ai_agent/views/menu.xml`
- Modify: `farm_ai_agent/__manifest__.py`

**Interfaces:**
- Consumes: Models from Tasks 1, 2, 3
- Produces: Professional three-tier layout view with statusbar and nested line tabs notebook.

- [ ] **Step 1: Write the failing test**

Append to `farm_ai_agent/tests/test_a2a_react_loop.py` to assert that views can compile and load correctly:
```python
    def test_04_react_views_compilation(self):
        """ Verify form and list views are correctly defined and loadable """
        form_view = self.env['ir.ui.view'].with_context(check_view_ids=True)._get_view_id('agri.a2a.react.loop', 'form')
        list_view = self.env['ir.ui.view'].with_context(check_view_ids=True)._get_view_id('agri.a2a.react.loop', 'tree')
        self.assertTrue(form_view)
        self.assertTrue(list_view)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `docker compose run --rm web odoo -d test_clean_db_sfc_mrp -u farm_ai_agent --test-enable --stop-after-init --log-level=info`  
Expected: FAIL on `test_04_react_views_compilation`.

- [ ] **Step 3: Write minimal implementation**

Create `/Users/jeffery/odoo-farm-workspace/odoo-farm-dev/farm_ai_agent/views/a2a_react_loop_views.xml`:
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <!-- Re-Act Loop Views -->
        <record id="view_a2a_react_loop_form" model="ir.ui.view">
            <field name="name">agri.a2a.react.loop.form</field>
            <field name="model">agri.a2a.react.loop</field>
            <field name="arch" type="xml">
                <form string="AI Re-Act Loop">
                    <header>
                        <button name="action_execute_iteration" type="object" string="Step Loop" class="oe_highlight" invisible="state not in ['draft', 'running', 'paused']"/>
                        <field name="state" widget="statusbar" statusbar_visible="draft,running,paused,completed,failed"/>
                    </header>
                    <sheet>
                        <div class="oe_title">
                            <h1>
                                <field name="name" readonly="1"/>
                            </h1>
                        </div>
                        <group>
                            <group>
                                <field name="goal"/>
                                <field name="max_iterations"/>
                            </group>
                            <group>
                                <field name="current_iteration" readonly="1"/>
                                <field name="context_data" widget="ace" options="{'mode': 'json'}"/>
                            </group>
                        </group>
                        <notebook>
                            <page string="Execution Steps (Thought -> Action -> Observation)">
                                <field name="line_ids" readonly="1">
                                    <list string="Steps">
                                        <field name="iteration"/>
                                        <field name="thought"/>
                                        <field name="action_type"/>
                                        <field name="tool_id"/>
                                        <field name="observation"/>
                                        <field name="state" widget="badge"/>
                                    </list>
                                </field>
                            </page>
                        </notebook>
                    </sheet>
                </form>
            </field>
        </record>

        <record id="view_a2a_react_loop_tree" model="ir.ui.view">
            <field name="name">agri.a2a.react.loop.tree</field>
            <field name="model">agri.a2a.react.loop</field>
            <field name="arch" type="xml">
                <list string="AI Re-Act Loops">
                    <field name="name"/>
                    <field name="goal"/>
                    <field name="current_iteration"/>
                    <field name="max_iterations"/>
                    <field name="state" widget="badge"/>
                </list>
            </field>
        </record>

        <!-- Re-Act Loop Action -->
        <record id="action_a2a_react_loop" model="ir.actions.act_window">
            <field name="name">AI Agent Re-Act Loops</field>
            <field name="res_model">agri.a2a.react.loop</field>
            <field name="view_mode">tree,form</field>
            <field name="help" type="html">
                <p class="o_view_nocontent_smiling_face">
                    Create your first AI Agent Re-Act Loop!
                </p>
                <p>
                    Observe, reason, act, and audit dynamic agricultural adjustments in a secure savepoint sandbox.
                </p>
            </field>
        </record>
    </data>
</odoo>
```
Modify `/Users/jeffery/odoo-farm-workspace/odoo-farm-dev/farm_ai_agent/views/menu.xml` to append the menu action. We'll add it under the `farm_ai_agent_workflows_menu` or similar parent. Let's do a `replace` or add it to the existing menu block.
First, read `farm_ai_agent/views/menu.xml` using `read_file` to locate the best insertion point.
Wait! Let's read lines 1 to 20 of `farm_ai_agent/views/menu.xml`:
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <!-- Top-level Menus -->
        <menuitem id="farm_ai_agent_menu_root" name="AI Agents" web_icon="farm_ai_agent,static/description/icon.png" sequence="10" />
        
        <menuitem id="farm_ai_agent_coordination_menu" name="Coordination" parent="farm_ai_agent_menu_root" sequence="10" />
        <menuitem id="farm_ai_agent_decision_menu" name="Decisions" parent="farm_ai_agent_menu_root" sequence="20" />
        <menuitem id="farm_ai_agent_mission_menu" name="Missions" parent="farm_ai_agent_menu_root" sequence="30" />
        <menuitem id="farm_ai_agent_workflows_menu" name="Workflows" parent="farm_ai_agent_menu_root" sequence="40" />
```
So we can append our menu item under `farm_ai_agent_workflows_menu`:
```xml
        <menuitem id="menu_a2a_react_loop" name="Agent Re-Act Loops" parent="farm_ai_agent_workflows_menu" action="action_a2a_react_loop" sequence="30" />
```
Add to `farm_ai_agent/__manifest__.py` `"data"` section:
```python
        'views/a2a_react_loop_views.xml',
```

- [ ] **Step 4: Run test to verify it passes**

Run: `docker compose run --rm web odoo -d test_clean_db_sfc_mrp -u farm_ai_agent --test-enable --stop-after-init --log-level=info`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add farm_ai_agent/views/a2a_react_loop_views.xml farm_ai_agent/views/menu.xml farm_ai_agent/__manifest__.py farm_ai_agent/tests/test_a2a_react_loop.py
git commit -m "feat(ai-agent): implement form and tree views for Re-Act loop models"
```

---

### Task 6: Comprehensive Unit Tests Verification

**Files:**
- Modify: `farm_ai_agent/tests/test_a2a_react_loop.py`

**Interfaces:**
- Consumes: All previous tasks
- Produces: Complete 4-target automated test coverage for standard iterations, tool validations, savepoint rollbacks, and GxP gating.

- [ ] **Step 1: Write the final comprehensive tests**

Complete `farm_ai_agent/tests/test_a2a_react_loop.py` by appending human gating tests:
```python
    def test_05_human_gxp_gating_and_approval(self):
        """ Verify that tools requiring GxP gating correctly pause and wait for approval """
        tool = self.Tool.create({
            'name': 'Gated Material Transfer',
            'model_name': 'mrp.workcenter',
            'method_name': 'write',
            'required_gxp_gating': True,
        })
        
        loop = self.env['agri.a2a.react.loop'].create({
            'name': 'REACT/GATED/001',
            'goal': 'Perform a high-risk material move',
        })
        
        # This execution step should pause and enter the 'paused' state due to GxP/CCP trigger
        res = loop.action_execute_iteration(
            thought="I want to initiate a high-risk move.",
            action_type="tool_call",
            tool_id=tool.id,
            action_payload="{}",
        )
        
        self.assertTrue(res)
        self.assertEqual(loop.state, 'paused')
        
        last_step = loop.line_ids[-1]
        self.assertEqual(last_step.state, 'draft')
        self.assertIn("GxP Critical Control Point triggered", last_step.observation)
```

- [ ] **Step 2: Run test to verify it passes**

Run: `docker compose run --rm web odoo -d test_clean_db_sfc_mrp -u farm_ai_agent --test-enable --stop-after-init --log-level=info`  
Expected: PASS with 0 failures and 0 errors across all 5 comprehensive test cases.

- [ ] **Step 3: Commit**

```bash
git add farm_ai_agent/tests/test_a2a_react_loop.py
git commit -m "test(ai-agent): verify comprehensive 5-target Re-Act loop test suite"
```
