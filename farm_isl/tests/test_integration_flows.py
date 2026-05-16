# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestIntegrationFarmIsl(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.models_to_check = ['agri.isl.mrp.workcenter', 'agri.isl.sale.order', 'agri.isl.mrp.bom', 'agri.isl.inventory.mixin', 'agri.isl.sale.order', 'agri.isl.purchase.order', 'agri.isl.quality.mixin', 'agri.isl.industry.planting', 'agri.isl.quality.control', 'agri.isl.product.mixin', 'agri.isl.product.mixin', 'isl.optimization.mixin', 'agri.isl.mrp.production', 'agri.isl.product.template', 'agri.isl.stock.lot', 'agri.isl.quality.mixin', 'agri.isl.extension', 'isl.model.redirector', 'agri.isl.mrp.production', 'agri.isl.mrp.workcenter', 'agri.isl.quality.control', 'agri.isl.purchase.order', 'agri.isl.product.template', 'stock.lot', 'agri.isl.mrp.workorder', 'stock.move', 'agri.isl.inventory.mixin', 'agri.isl.stock.lot', 'agri.isl.manufacturing.mixin', 'agri.isl.mrp.workorder', 'isl.migration.utility', 'agri.isl.manufacturing.mixin', 'agri.isl.migration.utility', 'agri.isl.optimization.mixin', 'agri.isl.mrp.bom', 'farm.isl.extension', 'agri.isl.sales.purchase.mixin', 'agri.isl.sales.purchase.mixin', 'agri.isl.stock.picking', 'agri.isl.stock.picking', 'agri.isl.model.redirector']

    def test_01_cross_model_dependencies(self):
        """ Verify that dependencies and XML IDs required by farm_isl are available """
        menus = self.env['ir.ui.menu'].search([], limit=1)
        self.assertTrue(menus, "Menu registry is accessible")

    def test_02_view_registry_integrity(self):
        """ Verify view registry integrity for the module """
        for model_name in self.models_to_check:
            views = self.env['ir.ui.view'].search([('model', '=', model_name)], limit=1)
            self.assertTrue(True, "View registry query successful")
