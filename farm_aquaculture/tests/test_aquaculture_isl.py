# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestAquacultureISL(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Product = cls.env['product.product']
        cls.AquaLot = cls.env['agri.isl.lot.aquaculture']
        cls.AquaBom = cls.env['agri.isl.aquaculture.bom']
        
        cls.fish_product = cls.Product.create({
            'name': 'Atlantic Salmon',
            'type': 'consu'
        })

    def test_01_stocking_density_kpi(self):
        """ Test calculation of stocking density KPI """
        pond_batch = self.AquaLot.create({
            'name': 'POND-A1-2026',
            'product_id': self.fish_product.id,
            'water_volume_m3': 2000.0,
            'total_biomass': 500.0, # 500kg
        })
        
        pond_batch._compute_aquaculture_kpi()
        # Density should be 500 / 2000 = 0.25 kg/m3
        self.assertEqual(pond_batch.current_density, 0.25)
        
        pond_batch.total_biomass = 1000.0
        pond_batch._compute_aquaculture_kpi()
        self.assertEqual(pond_batch.current_density, 0.5)

    def test_02_aquaculture_recipe_setpoints(self):
        """ Test aquaculture specific recipe (BOM) setpoints """
        bom = self.AquaBom.create({
            'product_tmpl_id': self.fish_product.product_tmpl_id.id,
            'product_qty': 1.0,
            'min_dissolved_oxygen': 5.5,
            'max_stocking_density': 15.0
        })
        
        self.assertTrue(bom.exists())
        self.assertEqual(bom.min_dissolved_oxygen, 5.5)
        self.assertEqual(bom.max_stocking_density, 15.0)
        self.assertTrue(bom.bom_id.exists())
