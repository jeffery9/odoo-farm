# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError

@tagged('post_install', '-at_install')
class TestWaterValveBackpressure(TransactionCase):

    def test_water_valve_high_pressure_backpressure_cutoff(self):
        """ Verify high-pressure write triggers emergency cutoff and logs red safety HTML card """
        valve = self.env['farm.water.valve'].create({
            'name': 'Test Main Pump Valve',
            'status': 'open',
            'pressure_psi': 80.0
        })
        # Overpressure write
        valve.write({'pressure_psi': 135.0})
        self.assertEqual(valve.status, 'cutoff', "Overpressure must trigger automatic cutoff!")
        self.assertEqual(valve.pressure_psi, 0.0, "Overpressure must reset operating pressure to 0.")
        
        # Verify card is posted
        messages = self.env['mail.message'].search([('model', '=', 'farm.water.valve'), ('res_id', '=', valve.id)])
        self.assertTrue(any("HIGH PRESSURE WARNING" in m.body for m in messages))
