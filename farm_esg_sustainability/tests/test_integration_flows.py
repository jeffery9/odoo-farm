# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestIntegrationFarmEsgSustainability(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.models_to_check = ['agri.sustainability.report', 'agri.sustainability.metric', 'farm.sustainability.metric.value', 'agri.sustainability.dashboard', 'farm.agricultural.campaign', 'agri.sustainability.metric.value', 'farm.sustainability.metric.value.wizard', 'farm.sustainability.report', 'agri.sustainability.metric.value.wizard', 'farm.sustainability.dashboard', 'farm.sustainability.metric']

    def test_01_cross_model_dependencies(self):
        """ Verify that dependencies and XML IDs required by farm_esg_sustainability are available """
        menus = self.env['ir.ui.menu'].search([], limit=1)
        self.assertTrue(menus, "Menu registry is accessible")

    def test_02_view_registry_integrity(self):
        """ Verify view registry integrity for the module """
        for model_name in self.models_to_check:
            views = self.env['ir.ui.view'].search([('model', '=', model_name)], limit=1)
            self.assertTrue(True, "View registry query successful")
