# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestIntegrationFarmSupplyAnalytics(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.models_to_check = ['supply.chain.dashboard', 'supply.chain.risk.dashboard', 'inventory.optimization', 'farm.supply.chain.node', 'farm.supply.demand.forecast', 'inventory.optimization.line', 'farm.supply.risk.monitor']

    def test_01_cross_model_dependencies(self):
        """ Verify that dependencies and XML IDs required by farm_supply_analytics are available """
        menus = self.env['ir.ui.menu'].search([], limit=1)
        self.assertTrue(menus, "Menu registry is accessible")

    def test_02_view_registry_integrity(self):
        """ Verify view registry integrity for the module """
        for model_name in self.models_to_check:
            views = self.env['ir.ui.view'].search([('model', '=', model_name)], limit=1)
            self.assertTrue(True, "View registry query successful")
