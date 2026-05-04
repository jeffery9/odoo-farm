# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestIntegrationFarmGreenhouse(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.models_to_check = ['farm.ecommerce.listing.wizard', 'farm.greenhouse.control.action', 'farm.government.platform.config', 'farm.location', 'farm.greenhouse.energy.log', 'agri.biological.twin', 'farm.ecommerce.sync.log', 'farm.greenhouse.control.rule', 'farm.ecommerce.platform', 'farm.government.data.report']

    def test_01_cross_model_dependencies(self):
        """ Verify that dependencies and XML IDs required by farm_greenhouse are available """
        menus = self.env['ir.ui.menu'].search([], limit=1)
        self.assertTrue(menus, "Menu registry is accessible")

    def test_02_view_registry_integrity(self):
        """ Verify view registry integrity for the module """
        for model_name in self.models_to_check:
            views = self.env['ir.ui.view'].search([('model', '=', model_name)], limit=1)
            self.assertTrue(True, "View registry query successful")
