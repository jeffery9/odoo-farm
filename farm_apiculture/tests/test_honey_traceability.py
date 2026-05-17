# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestHoneyTraceability(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.honey = cls.env['product.product'].create({'name': 'Acacia Honey', 'type': 'product'})
        
    def test_01_honey_extraction_certification(self):
        """ Scenario 29: Honey Batch Integrity & Hive Health """
        mo = self.env['farm.apiculture.production'].create({
            'product_id': self.honey.id,
            'product_qty': 50,
            'bloom_period': 'Acacia Spring'
        })
        
        # Add QC check
        self.env['agri.quality.check'].create({
            'production_id': mo.id,
            'check_type': 'chemical',
            'result': 'pass',
            'lot_id': self.env['stock.lot'].create({'name':'mock', 'product_id': self.honey.id}).id # Mock
        })
        
        lot = mo.action_extract_honey()
        self.assertTrue(mo.antibiotic_free_cert, "Must be certified if chemical test passed.")
        self.assertTrue(lot, "A honey lot must be created.")

