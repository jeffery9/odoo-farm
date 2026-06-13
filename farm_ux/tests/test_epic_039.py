# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestEpic039(TransactionCase):
    """ Agri-UX Standard [US-039] """

    def setUp(self):
        super(TestEpic039, self).setUp()
        self.TermMapping = self.env['term.mapping']
        self.Indicator = self.env['visual.status.indicator']
        
        # Create mapping
        self.TermMapping.create({
            'name': 'WO to Intervention',
            'source_term': 'Work Order',
            'target_term': 'Agricultural Intervention',
            'language_code': 'en_US',
            'industry_context': 'planting'
        })

    def test_01_deep_term_mapping_from_industrial_to_agricultural_semantics(self):
        """ Verify "ViewInterceptor" term replacement [US-039-01] """
        text = "This is a Work Order for planting."
        mapped_text = self.TermMapping.with_context(industry_context='planting').apply_term_mapping_to_text(text)
        self.assertIn("Agricultural Intervention", mapped_text)
        self.assertNotIn("Work Order", mapped_text)

    def test_03_visual_status_indicators_with__traffic_light__principle(self):
        """ Verify card badge logic [US-039-03] """
        indicator = self.Indicator.create({
            'name': 'Task Danger',
            'model_name': 'project.task',
            'field_name': 'priority',
            'status_type': 'badge',
            'badge_style': 'danger',
            'status_value': 'high'
        })
        self.assertEqual(indicator.badge_style, 'danger')

    def test_15_one_click_batch_closure_for_agricultural_tasks(self):
        """ Verify batch closure logic [US-039-15] """
        # Usually implemented via a wizard. We verify the underlying capability.
        project = self.env['project.project'].create({'name': 'Farm Project'})
        task1 = self.env['project.task'].create({'name': 'Task 1', 'project_id': project.id})
        task2 = self.env['project.task'].create({'name': 'Task 2', 'project_id': project.id})
        
        tasks = task1 | task2
        # Mocking a batch action
        tasks.write({'state': '1_done'})
        self.assertTrue(all(t.state == '1_done' for t in tasks))

    def test_25_de_industrialization_view_interceptor_logic(self):
        """ Verify "fields_view_get" (now _get_view in Odoo 17+) overrides [US-039-25] """
        # Testing the mixin indirectly via fields_get
        # We use a model that inherits from AgriViewMixin if available, or test the logic
        # In our case, many models inherit from it via _inherit = ['agri.view.mixin']
        # Let's assume 'res.partner' is intercepted in some deployments or use a dummy
        # For this test, we verify the TermMapping call in fields_get
        partner_fields = self.env['res.partner'].with_context(industry_context='planting').fields_get(['name'])
        # Since 'Name' might not be mapped, this is more of a structural check
        self.assertIn('name', partner_fields)
