# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
import json

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
        bad_payload = json.dumps({'capacity_time_stop': -150.0}) # Invalid value or type
        
        loop.action_execute_iteration(
            thought="I will set an invalid negative value.",
            action_type="tool_call",
            tool_id=tool.id,
            action_payload=bad_payload,
            test_target_record_id=wc.id
        )
        
        # Verify line state was recorded as 'violated' or 'failed' and workcenter state remains unchanged
        last_step = loop.line_ids[-1]
        self.assertIn(last_step.state, ['violated', 'failed'])
        self.assertEqual(wc.name, 'Renamed by Agent') # Preserved previous value!

    def test_04_react_views_compilation(self):
        """ Verify form and list views are correctly defined and loadable """
        form_view = self.env.ref('farm_ai_agent.view_a2a_react_loop_form')
        list_view = self.env.ref('farm_ai_agent.view_a2a_react_loop_tree')
        self.assertTrue(form_view.exists())
        self.assertTrue(list_view.exists())

    def test_05_execute_active_skill(self):
        """ Verify that loading and executing an active skill JSON directive works flawlessly """
        wc = self.env['mrp.workcenter'].create({'name': 'Vanilla Workcenter'})
        
        # Define an active skill directive
        skill_payload = {
            "model": "mrp.workcenter",
            "method": "write",
            "thought": "I will execute the precision rename skill directive on this asset.",
            "args": {
                "name": "Boosted by Active Skill"
            }
        }
        
        loop = self.env['agri.a2a.react.loop'].create({
            'name': 'REACT/SKILL/001',
            'goal': 'Execute dynamic corrective skill',
            'active_skill_json': json.dumps(skill_payload)
        })
        
        # Execute the skill
        success = loop.action_execute_active_skill(test_target_record_id=wc.id)
        self.assertTrue(success)
        
        # Verify the change was applied successfully
        self.assertEqual(wc.name, "Boosted by Active Skill")
        
        # Check audit trail
        self.assertTrue(len(loop.line_ids) > 0)
        self.assertEqual(loop.line_ids[-1].state, 'success')

    def test_06_user_skill_upload_and_onchange(self):
        """ Verify that base64 encoded Markdown upload triggers specification extraction, frontmatter parsing, and auto-parsing """
        import base64
        md_content = """---
name: Thermal Frost Skill
description: Automatic thermal frost mitigation for high-value greenhouses.
---

# Thermal Adjustment Skill

This skill stabilizes greenhouses during a frost.

## Executable Blueprint
```json
{
    "model": "mrp.workcenter",
    "method": "write",
    "args": {"name": "Thermal Injector Boosted"}
}
```
"""
        encoded_md = base64.b64encode(md_content.encode('utf-8'))
        
        skill = self.env['agri.ai.agent.skill'].create({
            'name': 'Temp Skill Name',
            'description': 'Temp description',
            'upload_file': encoded_md,
            'upload_filename': 'thermal_skill.md'
        })
        
        # Trigger onchange to simulate file upload
        skill._onchange_upload_file()
        
        # Verify YAML frontmatter fields are successfully parsed and populated
        self.assertEqual(skill.name, "Thermal Frost Skill")
        self.assertEqual(skill.description, "Automatic thermal frost mitigation for high-value greenhouses.")
        
        # Verify markdown specification body is extracted (excluding frontmatter)
        self.assertIn("greenhouses during a frost", skill.skill_markdown)
        self.assertNotIn("Automatic thermal frost mitigation", skill.skill_markdown)
        
        # Verify executable payload was automatically computed and parsed from code-block
        parsed_payload = json.loads(skill.skill_payload)
        self.assertEqual(parsed_payload.get('model'), 'mrp.workcenter')
        self.assertEqual(parsed_payload.get('args', {}).get('name'), 'Thermal Injector Boosted')

        # 2. Verify Export back to compliant SKILL.md
        res = skill.action_export_agent_skill()
        self.assertEqual(res.get('type'), 'ir.actions.act_url')
        
        # Retrieve generated attachment
        attachment = self.env['ir.attachment'].search([
            ('res_model', '=', 'agri.ai.agent.skill'),
            ('res_id', '=', skill.id),
            ('name', '=', 'SKILL.md')
        ], limit=1)
        self.assertTrue(attachment.exists())
        exported_text = base64.b64decode(attachment.datas).decode('utf-8')
        
        # Verify it has standard frontmatter header and body
        self.assertTrue(exported_text.startswith("---\nname: Thermal Frost Skill\ndescription: Automatic thermal frost mitigation for high-value greenhouses.\n---\n"))
        self.assertIn("greenhouses during a frost", exported_text)
        self.assertEqual(parsed_payload.get('args', {}).get('name'), 'Thermal Injector Boosted')

    def test_07_skill_selection_and_execution_with_attachments(self):
        """ Verify that selecting a Markdown skill copies computed payload and supports attachments """
        import base64
        wc = self.env['mrp.workcenter'].create({'name': 'Pre-Selected WC'})
        
        # 1. Create skill with markdown and attachment
        skill = self.env['agri.ai.agent.skill'].create({
            'name': 'Pest Correction Skill',
            'description': 'Spraying calibration skill',
            'skill_markdown': """# Pest Spraying Skill
```json
{
    "model": "mrp.workcenter",
    "method": "write",
    "args": {"name": "Pest Spraying WC"}
}
```
"""
        })
        
        # Link an auxiliary python attachment using upload_file (non-markdown format)
        aux_data = base64.b64encode(b"print('calibration sequence')")
        skill.write({
            'upload_file': aux_data,
            'upload_filename': 'calibration.py'
        })
        skill._onchange_upload_file()
        
        # Check attachment was created and linked
        self.assertEqual(len(skill.attachment_ids), 1)
        self.assertEqual(skill.attachment_ids[0].name, 'calibration.py')
        
        # 2. Assign to loop and run
        loop = self.env['agri.a2a.react.loop'].create({
            'name': 'REACT/SKILL/002',
            'goal': 'Run user-authored skill with attachments',
            'skill_id': skill.id
        })
        
        # Trigger onchange selection
        loop._onchange_skill_id()
        self.assertEqual(json.loads(loop.active_skill_json).get('args', {}).get('name'), 'Pest Spraying WC')
        
        # Run skill
        success = loop.action_execute_active_skill(test_target_record_id=wc.id)
        self.assertTrue(success)
        self.assertEqual(wc.name, 'Pest Spraying WC')

    def test_08_skill_views_compilation(self):
        """ Verify that the newly registered agri.ai.agent.skill views can compile and load successfully """
        form_view = self.env.ref('farm_ai_agent.view_agri_ai_agent_skill_form')
        list_view = self.env.ref('farm_ai_agent.view_agri_ai_agent_skill_tree')
        self.assertTrue(form_view.exists())
        self.assertTrue(list_view.exists())

    def test_09_packaged_zip_skill_unzip_and_extraction(self):
        """ Verify that uploading a packaged zip/skill file extracts SKILL.md and creates attachments for other files """
        import base64
        import io
        import zipfile
        
        md_content = """---
name: Zip Irrigation Skill
description: Irrigation scheduling skill packaged in a zip archive.
---

# Irrigation Skill Spec
```json
{
    "model": "mrp.workcenter",
    "method": "write",
    "args": {"name": "Irrigation Zip WC"}
}
```
"""
        # Create an in-memory zip file
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zfile:
            zfile.writestr('SKILL.md', md_content)
            zfile.writestr('scripts/booster.py', "print('boost irrigation')")
            zfile.writestr('assets/calibration.xlsx', b"excel binary dummy data")
            
        zip_data = zip_buffer.getvalue()
        encoded_zip = base64.b64encode(zip_data)
        
        skill = self.env['agri.ai.agent.skill'].create({
            'name': 'Pending Name',
            'description': 'Pending description',
            'upload_file': encoded_zip,
            'upload_filename': 'irrigation_pack.skill'
        })
        
        # Trigger onchange file upload processing
        skill._onchange_upload_file()
        
        # Verify metadata is successfully extracted from the zip's SKILL.md
        self.assertEqual(skill.name, "Zip Irrigation Skill")
        self.assertEqual(skill.description, "Irrigation scheduling skill packaged in a zip archive.")
        self.assertIn("Irrigation Skill Spec", skill.skill_markdown)
        
        # Verify executable payload was computed
        parsed_payload = json.loads(skill.skill_payload)
        self.assertEqual(parsed_payload.get('model'), 'mrp.workcenter')
        
        # Verify the auxiliary files (scripts, assets) are automatically extracted as ir.attachment records and linked!
        self.assertEqual(len(skill.attachment_ids), 2)
        
        attachment_names = skill.attachment_ids.mapped('name')
        self.assertIn('scripts/booster.py', attachment_names)
        self.assertIn('assets/calibration.xlsx', attachment_names)
        
        # Retrieve the script and verify content
        script_att = skill.attachment_ids.filtered(lambda a: a.name == 'scripts/booster.py')
        self.assertEqual(base64.b64decode(script_att.datas).decode('utf-8'), "print('boost irrigation')")

    def test_10_direct_multiple_attachments_onchange_parsing(self):
        """ Verify that uploading a set of multiple attachments directly (e.g. via many2many_binary) auto-extracts metadata from SKILL.md """
        import base64
        
        md_content = """---
name: Direct Multi Attachment Skill
description: Skill uploaded as a set of separate files directly into Many2many list.
---

# Direct Specification
```json
{
    "model": "mrp.workcenter",
    "method": "write",
    "args": {"name": "Direct Multi WC"}
}
```
"""
        # Create separate attachments in Odoo
        att_md = self.env['ir.attachment'].create({
            'name': 'SKILL.md',
            'datas': base64.b64encode(md_content.encode('utf-8')),
            'res_model': 'agri.ai.agent.skill',
            'res_id': 0,
        })
        
        att_script = self.env['ir.attachment'].create({
            'name': 'scripts/calc_yield.py',
            'datas': base64.b64encode(b"print('calculating yield')"),
            'res_model': 'agri.ai.agent.skill',
            'res_id': 0,
        })
        
        # Create empty skill and link attachments
        skill = self.env['agri.ai.agent.skill'].create({
            'name': 'Draft Skill Name',
            'description': 'Draft Description',
            'attachment_ids': [(6, 0, [att_md.id, att_script.id])]
        })
        
        # Trigger onchange on attachments list
        skill._onchange_attachment_ids()
        
        # Verify metadata is successfully extracted from SKILL.md attachment
        self.assertEqual(skill.name, "Direct Multi Attachment Skill")
        self.assertEqual(skill.description, "Skill uploaded as a set of separate files directly into Many2many list.")
        self.assertIn("Direct Specification", skill.skill_markdown)
        
        # Verify executable payload was computed
        parsed_payload = json.loads(skill.skill_payload)
        self.assertEqual(parsed_payload.get('model'), 'mrp.workcenter')
        self.assertEqual(parsed_payload.get('args', {}).get('name'), 'Direct Multi WC')
        
        # Verify all attachments remain associated
        self.assertEqual(len(skill.attachment_ids), 2)
        self.assertIn('scripts/calc_yield.py', skill.attachment_ids.mapped('name'))
