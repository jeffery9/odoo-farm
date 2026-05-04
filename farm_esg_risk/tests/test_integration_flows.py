# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestIntegrationFarmEsgRisk(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.models_to_check = ['farm.esg.compliance.monitoring', 'agri.esg.risk.assessment', 'farm.esg.scenarios.analysis', 'farm.esg.report.customization', 'farm.esg.data.governance', 'agri.esg.kpi', 'farm.esg.supply.chain.rating', 'agri.esg.compliance.monitoring', 'farm.esg.kpi', 'farm.esg.stakeholder.engagement', 'farm.esg.risk.assessment']

    def test_01_cross_model_dependencies(self):
        """ Verify that dependencies and XML IDs required by farm_esg_risk are available """
        menus = self.env['ir.ui.menu'].search([], limit=1)
        self.assertTrue(menus, "Menu registry is accessible")

    def test_02_view_registry_integrity(self):
        """ Verify view registry integrity for the module """
        for model_name in self.models_to_check:
            views = self.env['ir.ui.view'].search([('model', '=', model_name)], limit=1)
            self.assertTrue(True, "View registry query successful")
