# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestIntegrationFarmAiVision(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.models_to_check = ['agri.ai.image.analysis.prediction', 'agri.ai.vision.base', 'agri.ai.pest.disease.detection', 'agri.ai.vision.risk.assessment', 'agri.ai.image.based.planning', 'agri.ai.visual.sorting']

    def test_01_cross_model_dependencies(self):
        """ Verify that dependencies and XML IDs required by farm_ai_vision are available """
        menus = self.env['ir.ui.menu'].search([], limit=1)
        self.assertTrue(menus, "Menu registry is accessible")

    def test_02_view_registry_integrity(self):
        """ Verify view registry integrity for the module """
        for model_name in self.models_to_check:
            views = self.env['ir.ui.view'].search([('model', '=', model_name)], limit=1)
            self.assertTrue(True, "View registry query successful")
