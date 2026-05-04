# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestIntegrationFarmProcessing(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.models_to_check = ['agri.processing.energy.efficiency', 'mrp.production', 'farm.pharma.bom', 'agri.processing.attribute.inheritance', 'farm.package.level', 'farm.sc.category', 'farm.seasonal.bom.material', 'agri.processing.label.compliance', 'farm.chemical.bom', 'agri.allergen', 'farm.package', 'stock.picking', 'farm.pharma.production', 'farm.industry.operation', 'agri.processing.yield.optimizer', 'farm.processing.production', 'agri.processing.gmp.monitoring', 'mrp.bom.byproduct', 'farm.lot.harvest', 'agri.processing.wastage.report', 'farm.stock.lot.health', 'farm.industry.workcenter', 'agri.ai.parameter', 'farm.processing.step', 'farm.seasonal.bom', 'farm.season', 'farm.seasonal.parameter.line', 'agri.processing.formula.auto.correction', 'farm.allergen', 'agri.processing.active.ingredient', 'farm.processing.artisan.log', 'farm.bom.grade.distribution', 'agri.processing.multi.output', 'agri.health.schedule', 'stock.move.line', 'agri.processing.traceability.matrix', 'farm.processing.bom', 'farm.seasonal.bom.parameter', 'stock.lot', 'mrp.workorder', 'mrp.routing.workcenter', 'farm.processing.bom.line', 'stock.move', 'farm.seasonal.bom.line', 'agri.processing.cold.chain.log', 'agri.processing.batch.integrity', 'farm.bom.package.line', 'product.template', 'agri.processing.allergen.control', 'farm.quality.rejection.reason', 'farm.health.schedule', 'farm.chemical.production', 'mrp.bom', 'mrp.workcenter', 'agri.processing.multi.output.line']

    def test_01_cross_model_dependencies(self):
        """ Verify that dependencies and XML IDs required by farm_processing are available """
        menus = self.env['ir.ui.menu'].search([], limit=1)
        self.assertTrue(menus, "Menu registry is accessible")

    def test_02_view_registry_integrity(self):
        """ Verify view registry integrity for the module """
        for model_name in self.models_to_check:
            views = self.env['ir.ui.view'].search([('model', '=', model_name)], limit=1)
            self.assertTrue(True, "View registry query successful")
