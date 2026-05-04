# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestColdChainLogistics(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Facility = cls.env['cold.storage.facility']
        cls.Zone = cls.env['cold.storage.zone']
        cls.Location = cls.env['farm.location'].create({'name': 'Warehouse Alpha', 'usage': 'internal'})
        
    def test_01_cold_storage_creation(self):
        """ Test cold storage facility parameters and utilization """
        facility = self.Facility.create({
            'name': 'Cold Storage A1',
            'facility_code': 'CSA1',
            'location_id': self.Location.id,
            'capacity_volume': 1000.0,
            'min_temperature': -18.0,
            'max_temperature': -15.0,
        })
        self.assertTrue(facility.exists())
        self.assertEqual(facility.status, 'operational')
        
        # Test unique constraint
        from odoo.tools import mute_logger
        with mute_logger('odoo.sql_db'), self.assertRaises(Exception), self.env.cr.savepoint():
            self.Facility.create({
                'name': 'Cold Storage A2',
                'facility_code': 'CSA1', # duplicate code
            })
            
    def test_02_temperature_impact_forecast(self):
        """ Test shelf life adjustment based on temperature metrics """
        Forecast = self.env['seasonal.stock.forecast']
        Product = self.env['product.product'].create({'name': 'Frozen Berries'})
        
        forecast = Forecast.create({
            'name': 'Summer Berry Forecast',
            'product_id': Product.id,
            'season_period': 'q3',
            'base_shelf_life_days': 180,
            'avg_temperature': -10.0, # Warmer than optimal
            'temperature_impact_factor': 0.8 # Reduces shelf life by 20%
        })
        
        forecast._compute_shelf_life()
        # 180 * 0.8 = 144
        self.assertEqual(forecast.temperature_adjusted_shelf_life, 144)
        self.assertEqual(forecast.shelf_life_reduction_days, 36)
