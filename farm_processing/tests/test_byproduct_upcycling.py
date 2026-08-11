# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestByproductUpcycling(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.juice = cls.env['product.product'].create({'name': 'Orange Juice', 'type': 'consu', 'is_storable': True})
        cls.pectin = cls.env['product.product'].create({'name': 'Pectin Extract', 'type': 'consu', 'is_storable': True})

    def test_01_trigger_secondary_mo(self):
        """ Scenario 37: By-Product Upcycling """
        mo1 = self.env['mrp.production'].create({
            'product_id': self.juice.id,
            'product_qty': 1000
        })
        
        mo1.action_confirm()
        mo1.button_mark_done()
        
        # Check if secondary MO was created
        mo2 = self.env['mrp.production'].search([('origin', '=', f"Upcycled from {mo1.name}")])
        self.assertTrue(mo2, "Secondary MO for pectin must be generated.")
        self.assertEqual(mo2.product_qty, 600.0, "Quantity should be 60% of juice batch.")

