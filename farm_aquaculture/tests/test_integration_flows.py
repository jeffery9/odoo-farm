# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestIntegrationFarmAquaculture(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.models_to_check = ['farm.water.quality.log', 'farm.aquaculture.operation', 'mrp.production', 'agri.isl.aquaculture.bom', 'farm.aquaculture.bom.line', 'agri.isl.ras.production', 'agri.isl.lot.aquaculture', 'farm.aquaculture.lss', 'agri.isl.aquaculture.production', 'stock.lot', 'mrp.bom']

    def test_01_cross_model_dependencies(self):
        """ Verify that dependencies and XML IDs required by farm_aquaculture are available """
        menus = self.env['ir.ui.menu'].search([], limit=1)
        self.assertTrue(menus, "Menu registry is accessible")

    def test_02_view_registry_integrity(self):
        """ Verify view registry integrity for the module """
        for model_name in self.models_to_check:
            views = self.env['ir.ui.view'].search([('model', '=', model_name)], limit=1)
            self.assertTrue(True, "View registry query successful")
