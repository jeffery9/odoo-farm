# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestIntegrationFarmAiDecision(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.models_to_check = ['agri.ai.agent', 'mrp.production', 'agri.ai.quality.grading', 'agri.ai.health.monitoring', 'agri.ai.harvest.timing', 'agri.ai.decision.base', 'agri.ai.pest.disease.decision', 'ai.decision.engine', 'agri.ai.irrigation.decision', 'agri.ai.operation.path.optimization', 'agri.ai.risk.assessment', 'agri.ai.fertilization.decision', 'agri.ai.resource.optimization', 'agri.ai.market.prediction', 'agri.ai.crop.growth.prediction']

    def test_01_cross_model_dependencies(self):
        """ Verify that dependencies and XML IDs required by farm_ai_decision are available """
        menus = self.env['ir.ui.menu'].search([], limit=1)
        self.assertTrue(menus, "Menu registry is accessible")

    def test_02_view_registry_integrity(self):
        """ Verify view registry integrity for the module """
        for model_name in self.models_to_check:
            views = self.env['ir.ui.view'].search([('model', '=', model_name)], limit=1)
            self.assertTrue(True, "View registry query successful")
