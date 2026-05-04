# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestCarbonEmissions(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Product = cls.env['product.product']
        cls.Bom = cls.env['mrp.bom']
        cls.Production = cls.env['mrp.production']
        
        # Finished product
        cls.crop = cls.Product.create({
            'name': 'Wheat Harvest',
            'type': 'consu'
        })
        
        # Raw material with high carbon footprint (e.g., Synthetic Fertilizer)
        cls.fertilizer = cls.Product.create({
            'name': 'Urea Fertilizer',
            'type': 'consu',
            'carbon_emission_factor': 2.5 # 2.5 kg CO2e per kg of fertilizer
        })
        
        # Raw material with low carbon footprint
        cls.water = cls.Product.create({
            'name': 'Irrigation Water',
            'type': 'consu',
            'carbon_emission_factor': 0.1 # 0.1 kg CO2e per unit
        })
        
        cls.bom = cls.Bom.create({
            'product_tmpl_id': cls.crop.product_tmpl_id.id,
            'product_qty': 1000.0,
        })
        cls.bom.bom_line_ids.create([
            {
                'bom_id': cls.bom.id,
                'product_id': cls.fertilizer.id,
                'product_qty': 100.0
            },
            {
                'bom_id': cls.bom.id,
                'product_id': cls.water.id,
                'product_qty': 500.0
            }
        ])

    def test_01_carbon_footprint_calculation(self):
        """ Test that production carbon footprint is correctly aggregated from inputs """
        mo = self.Production.create({
            'product_id': self.crop.id,
            'bom_id': self.bom.id,
            'product_qty': 1000.0,
        })
        
        # Force computation
        mo._compute_carbon_emission()
        
        # Expected emission: 
        # Fertilizer: 100 qty * 2.5 factor = 250
        # Water: 500 qty * 0.1 factor = 50
        # Total: 300.0
        self.assertEqual(mo.calculated_carbon_emission, 300.0)
