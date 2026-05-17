# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestClimateGating(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.tomato = cls.env['product.product'].create({'name': 'Tomato', 'type': 'product'})
        cls.greenhouse = cls.env['farm.location'].create({'name': 'GH-1', 'location_type': 'greenhouse'})

    def test_01_climate_lock_on_spraying(self):
        """ Scenario 31: Micro-Climate Gating """
        mo = self.env['mrp.production'].create({
            'product_id': self.tomato.id,
            'product_qty': 100,
            'intervention_type': 'protection', # Spraying
            'land_parcel_id': self.greenhouse.id,
            'current_greenhouse_humidity': 90.0 # Above 85%
        })
        
        with self.assertRaises(UserError) as e:
            mo.action_confirm()
        self.assertIn("CLIMATE LOCK", str(e.exception))

