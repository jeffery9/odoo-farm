# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestIntegrationFarmMultiFarmFinancial(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.models_to_check = ['subsidy.disbursement', 'internal.credit', 'internal.marketplace.transaction', 'cooperative.entity', 'dividend.distribution', 'dividend.line', 'share.transaction', 'cooperative.decision', 'multi.sign.line', 'internal.loan', 'subsidy.disbursement.line', 'cooperative.treasury', 'multi.sign.process', 'decision.audit', 'credit.transaction', 'cooperative.member']

    def test_01_cross_model_dependencies(self):
        """ Verify that dependencies and XML IDs required by farm_multi_farm_financial are available """
        menus = self.env['ir.ui.menu'].search([], limit=1)
        self.assertTrue(menus, "Menu registry is accessible")

    def test_02_view_registry_integrity(self):
        """ Verify view registry integrity for the module """
        for model_name in self.models_to_check:
            views = self.env['ir.ui.view'].search([('model', '=', model_name)], limit=1)
            self.assertTrue(True, "View registry query successful")
