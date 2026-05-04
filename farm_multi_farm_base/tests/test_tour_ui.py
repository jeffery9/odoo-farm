# -*- coding: utf-8 -*-
from odoo.tests.common import HttpCase, tagged

@tagged('post_install', '-at_install')
class TestTourFarmMultiFarmBase(HttpCase):
    def test_01_tour_stub(self):
        """ Tour test stub for farm_multi_farm_base """
        self.assertTrue(True, "Tour test scaffold")
