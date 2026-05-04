# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestCropISL(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Product = cls.env['product.product']
        cls.CropBom = cls.env['farm.crop.bom']
        cls.CropProduction = cls.env['farm.crop.production']
        cls.Location = cls.env['farm.location']
        
        cls.wheat_product = cls.Product.create({
            'name': 'Winter Wheat v1',
            'type': 'consu'
        })
        
        cls.field_a = cls.Location.create({
            'name': 'Block A1',
            'usage': 'internal'
        })

    def test_01_crop_recipe_setup(self):
        """ Test crop-specific recipe (BOM) attributes """
        bom = self.CropBom.create({
            'product_tmpl_id': self.wheat_product.product_tmpl_id.id,
            'product_qty': 1.0,
            'target_yield_mu': 550.0,
            'growing_season': 'winter',
            'phi_days': 14
        })
        
        self.assertTrue(bom.exists())
        self.assertEqual(bom.target_yield_mu, 550.0)
        self.assertEqual(bom.growing_season, 'winter')
        self.assertEqual(bom.phi_days, 14)
        # Check parent link
        self.assertTrue(bom.bom_id.exists())

    def test_02_crop_production_vra(self):
        """ Test crop production VRA (Variable Rate Application) integration """
        mo = self.CropProduction.create({
            'product_id': self.wheat_product.id,
            'product_qty': 100.0,
            'is_vra_enabled': True,
            'prescription_json': '{"N": 15.5, "P": 10.0, "K": 8.0}'
        })
        
        self.assertTrue(mo.exists())
        self.assertTrue(mo.is_vra_enabled)
        self.assertIn('"N": 15.5', mo.prescription_json)
        # Check standard MO link
        self.assertTrue(mo.production_id.exists())
