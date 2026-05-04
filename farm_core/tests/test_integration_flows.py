# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from datetime import date, timedelta

class TestIntegrationFarmCore(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Asset = cls.env['agri.biological.asset']
        cls.Stage = cls.env['agri.industry.physio.stage']
        
        cls.stage_early = cls.Stage.create({
            'name': 'Seedling',
            'code': 'S1'
        })
        
    def test_01_biological_asset_lifecycle(self):
        """ Test the creation and basic attributes of a biological asset """
        birth = date.today() - timedelta(days=10)
        asset = self.Asset.create({
            'name': 'Test Apple Tree 001',
            'agricultural_type': 'plant',
            'birth_date': birth,
            'growth_stage_id': self.stage_early.id,
            'dna_marker': 'DNA-APL-001'
        })
        
        self.assertTrue(asset.exists())
        self.assertEqual(asset.agricultural_type, 'plant')
        self.assertEqual(asset.birth_date, birth)
        
    def test_02_asset_sustainability_integration(self):
        """ Test if sustainability mixin is working on biological assets """
        asset = self.Asset.create({
            'name': 'Sustainable Cow',
            'agricultural_type': 'animal',
        })
        
        # Check if sustainability fields exist (inherited from agri.sustainability.mixin)
        self.assertTrue(hasattr(asset, 'carbon_footprint'))
        asset.carbon_footprint = 150.5
        self.assertEqual(asset.carbon_footprint, 150.5)

    def test_03_location_gis_integration(self):
        """ Test land location creation and basic GIS data """
        location = self.env['farm.location'].create({
            'name': 'North Field A',
            'usage': 'internal',
            'land_area': 5000.0,
            'gps_latitude': 34.0522,
            'gps_longitude': -118.2437
        })
        self.assertTrue(location.exists())
        self.assertEqual(location.land_area, 5000.0)
