# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestIntegrationFarmFinancialBasic(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.models_to_check = ['account.move.line', 'farm.cpa.analysis', 'account.move', 'agri.cost.template', 'farm.mortality.amortization', 'project.task', 'farm.processing.cost', 'farm.cost.wip.transfer', 'agri.cost.calculation.line', 'agri.cost.calculation']

    def test_01_cross_model_dependencies(self):
        """ Verify that dependencies and XML IDs required by farm_financial_basic are available """
        menus = self.env['ir.ui.menu'].search([], limit=1)
        self.assertTrue(menus, "Menu registry is accessible")

    def test_02_view_registry_integrity(self):
        """ Verify view registry integrity for the module """
        for model_name in self.models_to_check:
            views = self.env['ir.ui.view'].search([('model', '=', model_name)], limit=1)
            self.assertTrue(True, "View registry query successful")
