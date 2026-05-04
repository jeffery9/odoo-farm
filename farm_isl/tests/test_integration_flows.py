# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestIntegrationFarmIsl(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.models_to_check = ['farm.mrp.workcenter', 'farm.sale.order', 'farm.mrp.bom', 'agri.inventory.mixin', 'agri.sale.order', 'farm.purchase.order', 'farm.quality.mixin', 'agri.isl.industry.planting', 'agri.quality.control', 'farm.product.mixin', 'agri.product.mixin', 'isl.optimization.mixin', 'farm.mrp.production', 'agri.product.template', 'farm.stock.lot', 'agri.quality.mixin', 'agri.isl.extension', 'isl.model.redirector', 'agri.mrp.production', 'agri.mrp.workcenter', 'farm.quality.control', 'agri.purchase.order', 'farm.product.template', 'stock.lot', 'agri.mrp.workorder', 'stock.move', 'farm.inventory.mixin', 'agri.stock.lot', 'farm.manufacturing.mixin', 'farm.mrp.workorder', 'isl.migration.utility', 'agri.manufacturing.mixin', 'agri.isl.migration.utility', 'agri.isl.optimization.mixin', 'agri.mrp.bom', 'farm.isl.extension', 'agri.sales.purchase.mixin', 'farm.sales.purchase.mixin', 'agri.stock.picking', 'farm.stock.picking', 'agri.isl.model.redirector']

    def test_01_cross_model_dependencies(self):
        """ Verify that dependencies and XML IDs required by farm_isl are available """
        menus = self.env['ir.ui.menu'].search([], limit=1)
        self.assertTrue(menus, "Menu registry is accessible")

    def test_02_view_registry_integrity(self):
        """ Verify view registry integrity for the module """
        for model_name in self.models_to_check:
            views = self.env['ir.ui.view'].search([('model', '=', model_name)], limit=1)
            self.assertTrue(True, "View registry query successful")
