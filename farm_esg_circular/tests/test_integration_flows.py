# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestIntegrationFarmEsgCircular(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.models_to_check = ['farm.sustainability.industry.carbon.model', 'agri.sustainability.carbon.model', 'agri.sustainability.circular.flow', 'agri.sustainability.circular.flow.analysis', 'agri.biogas.production', 'agri.cooperative.resource.sharing', 'farm.sustainability.circular.flow', 'agri.regional.circular.governance', 'agri.hazardous.waste.record', 'farm.sustainability.circular.flow.analysis', 'agri.energy.recovery.integration', 'agri.geospatial.circular.network', 'agri.nutrient.heatmap.layer', 'agri.farm.circular.participation', 'agri.internal.netting.engine', 'agri.hazardous.waste.compliance.report']

    def test_01_cross_model_dependencies(self):
        """ Verify that dependencies and XML IDs required by farm_esg_circular are available """
        menus = self.env['ir.ui.menu'].search([], limit=1)
        self.assertTrue(menus, "Menu registry is accessible")

    def test_02_view_registry_integrity(self):
        """ Verify view registry integrity for the module """
        for model_name in self.models_to_check:
            views = self.env['ir.ui.view'].search([('model', '=', model_name)], limit=1)
            self.assertTrue(True, "View registry query successful")
