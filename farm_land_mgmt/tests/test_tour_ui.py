# -*- coding: utf-8 -*-
from odoo.tests.common import HttpCase, tagged

@tagged('post_install', '-at_install')
class TestTourFarmLandMgmt(HttpCase):
    def test_01_tour_stub(self):
        """ Tour test stub for farm_land_mgmt """
        self.assertTrue(True, "Tour test scaffold")
