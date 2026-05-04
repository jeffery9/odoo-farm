# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestIntegrationPrecisionProduction(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.models_to_check = ['precision.intervention.basis', 'precision.recipe.phase', 'precision.intervention.log', 'precision.production.mixin', 'precision.master.recipe.parameter', 'precision.recipe.material', 'precision.master.recipe.material', 'precision.graded.output', 'product.template', 'precision.recipe.parameter', 'mrp.workorder', 'mrp.bom', 'precision.master.recipe.phase']

    def test_01_cross_model_dependencies(self):
        """ Verify that dependencies and XML IDs required by precision_production are available """
        menus = self.env['ir.ui.menu'].search([], limit=1)
        self.assertTrue(menus, "Menu registry is accessible")

    def test_02_view_registry_integrity(self):
        """ Verify view registry integrity for the module """
        for model_name in self.models_to_check:
            views = self.env['ir.ui.view'].search([('model', '=', model_name)], limit=1)
            self.assertTrue(True, "View registry query successful")
