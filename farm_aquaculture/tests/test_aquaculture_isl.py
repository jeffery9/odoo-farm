# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, Form

class TestAquacultureISL(TransactionCase):
    def setUp(self):
        super(TestAquacultureISL, self).setUp()
        self.Product = self.env['product.product']
        self.shrimp = self.Product.create({'name': 'White Shrimp', 'type': 'product'})

    def test_01_aqua_form_stats(self):
        """ Test Aquaculture Form UI simulation and growth stats. """
        with Form(self.env['farm.aquaculture.production']) as f:
            f.product_id = self.shrimp
            f.product_qty = 5000.0
            f.water_temp = 28.5
            f.dissolved_oxygen = 6.5
            f.survival_rate = 95.0
            
        isl_mo = f.save()
        self.assertEqual(isl_mo.water_temp, 28.5)
        self.assertEqual(isl_mo.state, 'draft')
        self.assertEqual(isl_mo.production_id.product_id, self.shrimp)

    def test_02_aqua_bom_form(self):
        """ Test specialized Aquaculture BOM Form. """
        with Form(self.env['farm.aquaculture.bom']) as f:
            f.product_tmpl_id = self.shrimp.product_tmpl_id
            f.pond_type = 'concrete'
            f.stocking_density_limit = 50.0
            
        isl_bom = f.save()
        self.assertEqual(isl_bom.pond_type, 'concrete')
        self.assertTrue(isl_bom.bom_id)
