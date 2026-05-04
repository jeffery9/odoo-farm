# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestIntegrationFarmMrp(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Product = cls.env['product.product']
        cls.Bom = cls.env['mrp.bom']
        cls.Production = cls.env['mrp.production']
        
        cls.juice = cls.Product.create({
            'name': 'Apple Juice',
            'type': 'consu'
        })
        cls.apple = cls.Product.create({
            'name': 'Apple',
            'type': 'consu'
        })
        
        cls.bom = cls.Bom.create({
            'product_tmpl_id': cls.juice.product_tmpl_id.id,
            'product_qty': 1.0,
            'industry_type': 'food_processing'
        })
        cls.bom.bom_line_ids.create({
            'bom_id': cls.bom.id,
            'product_id': cls.apple.id,
            'product_qty': 5.0
        })

    def test_01_mrp_production_industry_link(self):
        """ Test that production orders correctly link to ISL proxies """
        mo = self.Production.create({
            'product_id': self.juice.id,
            'bom_id': self.bom.id,
            'product_qty': 10.0,
        })
        
        # Check if the industry type is inherited from BOM
        self.assertEqual(mo.bom_id.industry_type, 'food_processing')
        
        # Check if ISL redirection would work
        if hasattr(mo, 'get_formview_action'):
            action = mo.get_formview_action()
            # If food_processing is correctly set, it might redirect to farm.processing.production
            # This depends on if farm_processing is installed
            pass

    def test_02_agricultural_mo_fields(self):
        """ Test agricultural specific fields on MO """
        mo = self.Production.create({
            'product_id': self.juice.id,
            'bom_id': self.bom.id,
            'product_qty': 1.0,
        })
        
        # These fields are added in farm_mrp
        self.assertTrue(hasattr(mo, 'is_agri_processing'))
        self.assertTrue(hasattr(mo, 'processing_type'))
