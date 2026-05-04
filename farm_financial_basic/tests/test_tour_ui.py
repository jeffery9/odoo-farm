# -*- coding: utf-8 -*-
from odoo.tests.common import HttpCase, tagged

@tagged('post_install', '-at_install')
class TestTourFarmFinancialBasic(HttpCase):
    def test_01_tour_stub(self):
        """ Tour test stub for farm_financial_basic """
        self.assertTrue(True, "Tour test scaffold")
