# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestFloricultureColdChain(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.rose = cls.env['product.product'].create({'name': 'Red Rose', 'type': 'product'})

    def test_01_vase_life_downgrade(self):
        """ Scenario 33: Floriculture Cold Chain & Vase Life Prediction """
        mo = self.env['farm.flower.order'].create({
            'product_id': self.rose.id,
            'product_qty': 1000,
            'vase_life_days': 14
        })
        
        mo.cold_chain_breach_minutes = 45 # > 30 mins
        mo._onchange_cold_chain()
        
        self.assertEqual(mo.vase_life_days, 5, "Vase life must be downgraded on breach.")

