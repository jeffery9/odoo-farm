# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestAgrivoltaics(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.spinach = cls.env['product.product'].create({'name': 'Shade Spinach', 'type': 'product'})

    def test_01_dual_revenue_and_tilt(self):
        """ Scenario 36: Agrivoltaics / Solar Sharing """
        station = self.env['farm.green.monitor'].create({
            'name': 'Solar Field 1',
            'crop_id': self.spinach.id,
            'crop_revenue_est': 500.0,
            'solar_revenue_est': 1200.0
        })
        
        self.assertEqual(station.total_revenue_per_acre, 1700.0, "Revenues must combine.")
        
        station.action_ai_optimize_tilt()
        self.assertEqual(station.panel_tilt_angle, 45.0, "AI must adjust tilt.")

