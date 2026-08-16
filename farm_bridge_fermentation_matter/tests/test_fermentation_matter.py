# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestFermentationMatterBridge(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env['product.product'].create({
            'name': 'Test Fermentation Input Product',
            'type': 'consu',
        })
        cls.order = cls.env['farm.fermentation.order'].create({
            'product_id': cls.product.id,
            'product_qty': 1.0,
            'intervention_type': 'protection',
        })
        
    def test_field_injection_and_saving(self):
        matter = self.env['stock.matter.tracking'].create({
            'name': 'LPN-FERMENTATION-TEST-001',
            'fermentation_order_id': self.order.id,
        })
        self.assertEqual(matter.fermentation_order_id.id, self.order.id)
