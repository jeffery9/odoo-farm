# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestMarketing(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.GIRegistry = cls.env['agri.gi.registry']
        cls.Product = cls.env['product.template'].create({'name': 'Organic Rice'})
        cls.Lot = cls.env['stock.lot']
        
    def test_01_gi_registry_and_lot_linkage(self):
        """ Test GI registry creation and lot linking """
        gi = self.GIRegistry.create({
            'name': 'Wuchang Rice',
            'code': 'GI-CN-2301',
            'product_template_id': self.Product.id,
        })
        self.assertTrue(gi.exists())
        
        lot = self.Lot.create({
            'name': 'LOT-2026-001',
            'product_id': self.Product.product_variant_id.id,
            'gi_registry_id': gi.id,
        })
        
        lot.action_generate_gi_code()
        self.assertTrue(lot.gi_security_code)
        self.assertIn('GI-CN-2301', lot.gi_security_code)
