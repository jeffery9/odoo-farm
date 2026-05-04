# -*- coding: utf-8 -*-
from odoo.tests.common import HttpCase, tagged

@tagged('post_install', '-at_install')
class TestTourFarmAiDecision(HttpCase):
    def test_01_tour_stub(self):
        """ Tour test stub for farm_ai_decision """
        self.assertTrue(True, "Tour test scaffold")
