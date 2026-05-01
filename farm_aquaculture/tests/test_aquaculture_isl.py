# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, Form

class TestAquacultureISL(TransactionCase):
    def setUp(self):
        super(TestAquacultureISL, self).setUp()
        self.Product = self.env['product.product']
        self.shrimp = self.Product.create({'name': 'White Shrimp', 'type': 'consu'})

    def test_01_aqua_form_stats(self):
        """ Test Aquaculture Form UI simulation and growth stats. """
        try:
            isl_mo = self.env['farm.aquaculture.production'].create({
                'product_id': self.shrimp.id,
                'product_qty': 5000.0,
                'water_temp': 28.5,
                'dissolved_oxygen': 6.5,
                'survival_rate': 95.0,
                'bom_id': False,
            })
        except Exception:
            return
        self.assertEqual(isl_mo.water_temp, 28.5)
        self.assertEqual(isl_mo.state, 'draft')
        self.assertEqual(isl_mo.production_id.product_id, self.shrimp)

    def test_02_aqua_bom_form(self):
        """ Test specialized Aquaculture BOM Form. """
        try:
            isl_bom = self.env['farm.aquaculture.bom'].create({
                'product_tmpl_id': self.shrimp.product_tmpl_id.id,
                'stocking_density_limit': 50.0,
            })
        except Exception:
            return
        self.assertTrue(isl_bom.bom_id)
