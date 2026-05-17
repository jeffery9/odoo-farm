# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestBarrelTracking(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.wine = cls.env['product.product'].create({'name': 'Cabernet Sauvignon', 'type': 'product'})
        cls.barrel = cls.env['maintenance.equipment'].create({'name': 'French Oak Barrel 001'})

    def test_01_barrel_aging_and_blending(self):
        """ Scenario 32: Barrel Aging & Vintage Lot Identity """
        mo = self.env['farm.winery.production'].create({
            'product_id': self.wine.id,
            'product_qty': 200,
            'vintage_year': '2026'
        })
        
        mo.action_transfer_to_barrel(self.barrel)
        self.assertEqual(mo.barrel_id.id, self.barrel.id)
        
        # Test AI recommendation
        mo.sensory_score = 96.0
        mo.action_ai_blending_recommendation()
        
        messages = mo.message_ids.mapped('body')
        self.assertTrue(any('Grand Vin' in str(m) for m in messages), "Score 96 should recommend Grand Vin.")

