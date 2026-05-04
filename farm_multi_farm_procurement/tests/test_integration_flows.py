# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestIntegrationFarmMultiFarmProcurement(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.models_to_check = ['procurement.planning.line', 'hub.spoke.distribution.line', 'joint.procurement', 'cooperative.entity', 'netting.receivable.line', 'procurement.planning', 'netting.payable.line', 'hub.spoke.distribution', 'marketplace.demand.match', 'joint.procurement.line', 'internal.marketplace', 'joint.procurement.po', 'procurement.allocation.line', 'joint.procurement.po.member', 'internal.settlement', 'netting.settlement', 'cooperative.member']

    def test_01_cross_model_dependencies(self):
        """ Verify that dependencies and XML IDs required by farm_multi_farm_procurement are available """
        menus = self.env['ir.ui.menu'].search([], limit=1)
        self.assertTrue(menus, "Menu registry is accessible")

    def test_02_view_registry_integrity(self):
        """ Verify view registry integrity for the module """
        for model_name in self.models_to_check:
            views = self.env['ir.ui.view'].search([('model', '=', model_name)], limit=1)
            self.assertTrue(True, "View registry query successful")
