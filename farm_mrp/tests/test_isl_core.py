# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import AccessError

class TestISLCore(TransactionCase):
    def setUp(self):
        super(TestISLCore, self).setUp()
        self.Product = self.env['product.product']
        self.Bom = self.env['mrp.bom']
        self.Production = self.env['mrp.production']
        self.Lot = self.env['stock.lot']
        
        # Create a basic product
        self.product_pig = self.Product.create({
            'name': 'Angus Pig',
            'type': 'product',
        })

    def test_01_auto_isl_creation_on_bom(self):
        """ Test that creating a BOM with industry_type automatically creates ISL record. """
        # We use 'livestock' which is added by farm_livestock
        bom = self.Bom.create({
            'product_tmpl_id': self.product_pig.product_tmpl_id.id,
            'product_qty': 1.0,
            'industry_type': 'livestock',
        })
        
        # Check if farm.livestock.bom was created
        isl_bom = self.env['farm.livestock.bom'].search([('bom_id', '=', bom.id)])
        self.assertTrue(isl_bom, "ISL BOM should be created automatically for Livestock industry.")
        self.assertEqual(isl_bom.bom_id, bom)

    def test_02_auto_isl_creation_on_production(self):
        """ Test that creating an MO with industry_type automatically creates ISL record. """
        bom = self.Bom.create({
            'product_tmpl_id': self.product_pig.product_tmpl_id.id,
            'product_qty': 1.0,
            'industry_type': 'livestock',
        })
        
        mo = self.Production.create({
            'product_id': self.product_pig.id,
            'bom_id': bom.id,
            'product_qty': 1.0,
        })
        
        # Check if farm.livestock.production was created
        isl_mo = self.env['farm.livestock.production'].search([('production_id', '=', mo.id)])
        self.assertTrue(isl_mo, "ISL Production should be created automatically for Livestock industry.")
        self.assertEqual(isl_mo.production_id, mo)

    def test_03_lot_summary_hook(self):
        """ Test the decoupled lot summary info hook. """
        lot = self.Lot.create({
            'name': 'LIV-001',
            'product_id': self.product_pig.id,
            'lot_purpose': 'biological_asset',
        })
        
        # Create ISL lot record manually
        isl_lot = self.env['farm.lot.livestock'].create({
            'lot_id': lot.id,
            'gender': 'male',
            'current_weight': 150.5
        })
        
        lot._compute_isl_summary_info()
        self.assertIn("Husbandry: male", lot.isl_summary_info)
        self.assertIn("150.5kg", lot.isl_summary_info)

    def test_04_redirection_logic(self):
        """ Test that get_formview_action returns the ISL model. """
        bom = self.Bom.create({
            'product_tmpl_id': self.product_pig.product_tmpl_id.id,
            'product_qty': 1.0,
            'industry_type': 'livestock',
        })
        
        action = bom.get_formview_action()
        self.assertEqual(action['res_model'], 'farm.livestock.bom')
        self.assertTrue(action['context'].get('isl_active'))
