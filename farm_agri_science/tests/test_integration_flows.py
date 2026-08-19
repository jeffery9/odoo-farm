# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestIntegrationFarmAgriScience(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Profile = cls.env['agri.physiology.profile']
        cls.Stage = cls.env['agri.growth.stage']
        cls.VraStrategy = cls.env['agri.intervention.vra.strategy']
        cls.Prescription = cls.env['agri.intervention.vra.prescription']
        
        cls.wheat_profile = cls.Profile.create({
            'name': 'Winter Wheat X1',
            'temp_base': 0.0,
            'temp_opt': 20.0,
            'temp_max': 30.0,
            'logistic_l': 1000.0,
            'response_max_yield': 900.0
        })
        
        cls.stage_v1 = cls.Stage.create({
            'name': 'Vegetative 1',
            'stage_code': 'V1',
            'profile_id': cls.wheat_profile.id,
            'gdd_threshold': 150.0
        })

        # Set up geospatial location and grid cells
        cls.agri_loc = cls.env['agri.location'].create({
            'name': 'Science Field',
            'location_type': 'field'
        })
        cls.parcel = cls.env['farm.location'].create({
            'name': 'Science Parcel',
            'agri_location_id': cls.agri_loc.id,
            'land_area': 5000.0
        })
        cls.grid_cell_1 = cls.env['agri.geospatial.grid.cell'].create({
            'location_id': cls.parcel.id,
            'row': 1,
            'col': 1,
            'ndvi_index': 0.5
        })
        cls.grid_cell_2 = cls.env['agri.geospatial.grid.cell'].create({
            'location_id': cls.parcel.id,
            'row': 1,
            'col': 2,
            'ndvi_index': 0.7
        })

        # Set up product template
        cls.product = cls.env['product.template'].create({
            'name': 'Biological N Fertilizer',
            'type': 'consu'
        })

    def test_01_physiology_profile_creation(self):
        """ Test physiology profile and stages integration """
        self.assertTrue(self.wheat_profile.exists())
        self.assertEqual(len(self.wheat_profile.stage_ids), 1)
        self.assertEqual(self.wheat_profile.stage_ids[0].stage_code, 'V1')

    def test_02_vra_strategy_integration(self):
        """ Test VRA (Variable Rate Application) Strategy properties """
        vra = self.VraStrategy.create({
            'name': 'Wheat N Application',
            'type': 'inverse_ndvi',
            'is_stage_aware': True,
            'target_yield': 800.0
        })
        self.assertTrue(vra.exists())
        self.assertEqual(vra.type, 'inverse_ndvi')
        self.assertTrue(vra.is_stage_aware)
        self.assertEqual(vra.target_yield, 800.0)

    def test_03_vra_prescription_generation(self):
        """ Test full scientific VRA prescription map generation """
        strategy = self.VraStrategy.create({
            'name': 'Spatial Nitrogen strategy',
            'type': 'inverse_ndvi',
            'is_stage_aware': False,
            'target_ndvi': 0.7,
            'correction_slope': 0.5
        })
        
        prescription = self.Prescription.create({
            'location_id': self.parcel.id,
            'product_id': self.product.id,
            'strategy_id': strategy.id,
            'target_type': 'fertilizer',
            'base_rate': 10.0,
            'weather_risk_hedging': False
        })
        
        self.assertEqual(prescription.state, 'draft')
        self.assertEqual(len(prescription.line_ids), 0)
        
        # Generate VRA grid map
        prescription.action_generate_prescription_map()
        
        self.assertEqual(prescription.state, 'generated')
        self.assertEqual(len(prescription.line_ids), 2)
        
        # Verify calculated rates for each cell
        # Cell 1 (NDVI 0.5): 10.0 * (1 + (0.7 - 0.5) * 0.5) = 11.0
        # Cell 2 (NDVI 0.7): 10.0 * (1 + (0.7 - 0.7) * 0.5) = 10.0
        line_1 = prescription.line_ids.filtered(lambda l: l.grid_cell_id == self.grid_cell_1)
        line_2 = prescription.line_ids.filtered(lambda l: l.grid_cell_id == self.grid_cell_2)
        
        self.assertTrue(line_1.exists())
        self.assertTrue(line_2.exists())
        self.assertAlmostEqual(line_1.target_rate, 11.0, places=3)
        self.assertAlmostEqual(line_2.target_rate, 10.0, places=3)
