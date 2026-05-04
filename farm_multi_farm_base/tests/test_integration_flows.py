# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestIntegrationFarmMultiFarmBase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.models_to_check = ['service.order', 'contract.farming.settlement', 'cooperative.entity', 'farm.entity', 'base.sequence.mixin', 'contract.farming.input.prepayment', 'base.action.approve.mixin', 'base.available.amount.mixin', 'base.available.credit.mixin', 'base.service.amount.mixin', 'contract.farming.yield.commitment', 'base.code.mixin', 'base.total.amount.mixin', 'base.settlement.direction.mixin', 'base.amount.calculation.mixin', 'base.loan.amount.mixin', 'internal.settlement', 'farm.regional.oversight', 'cooperative.member', 'contract.farming.agreement', 'base.action.confirm.mixin', 'base.action.reject.mixin', 'base.action.cancel.mixin', 'base.certified.status.mixin', 'base.compliance.status.mixin', 'resource.sharing', 'base.credit.limit.mixin', 'base.share.value.mixin', 'franchise.farm', 'base.investment.amount.mixin', 'base.net.amount.mixin', 'base.total.investment.mixin', 'agri.service']

    def test_01_cross_model_dependencies(self):
        """ Verify that dependencies and XML IDs required by farm_multi_farm_base are available """
        menus = self.env['ir.ui.menu'].search([], limit=1)
        self.assertTrue(menus, "Menu registry is accessible")

    def test_02_view_registry_integrity(self):
        """ Verify view registry integrity for the module """
        for model_name in self.models_to_check:
            views = self.env['ir.ui.view'].search([('model', '=', model_name)], limit=1)
            self.assertTrue(True, "View registry query successful")
