# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, ValidationError
from odoo import fields
from datetime import datetime, timedelta

class TestEpic002(TransactionCase):
    """ BDD Test for Epic 002 Plant Farming """

    def setUp(self):
        super(TestEpic002, self).setUp()
        self.Location = self.env['farm.location']
        self.Campaign = self.env['farm.agricultural.campaign']
        self.Production = self.env['mrp.production']
        self.Weather = self.env['agri.weather.forecast']
        self.Profile = self.env['agri.physiology.profile']
        self.Telemetry = self.env['iiot.telemetry']
        
        # 1. Setup Parcel
        # gps_coordinates format used by farm.geofence: 'lng,lat;lng,lat;...'
        self.parcel = self.Location.create({
            'name': 'Test Parcel A',
            'is_land_parcel': True,
            'location_type': 'field',
            'gps_lat': 30.0,
            'gps_lng': 120.0,
            'gps_coordinates': '120.0,30.0;120.1,30.0;120.1,30.1;120.0,30.1;120.0,30.0'
        })

        # 2. Setup Physiology Profile for GDD (Base Temp 10.0)
        self.profile = self.Profile.create({
            'name': 'Corn Profile',
            'temp_base': 10.0,
            'logistic_l': 100.0,
            'logistic_k': 0.1,
            'logistic_gdd0': 500.0
        })

        # 3. Create a product for production
        self.product = self.env['product.product'].create({
            'name': 'Corn Seed',
            'type': 'product'
        })

    def test_01_production_season_campaign_planning(self):
        """ Scenario: Production Season Campaign planning """
        campaign = self.Campaign.create({
            'name': 'Corn Season 2024',
            'land_parcel_id': self.parcel.id,
            'date_start': fields.Date.today(),
            'date_end': fields.Date.today() + timedelta(days=120),
            'target_gdd': 1600.0,
            'base_temperature': 10.0
        })
        self.assertTrue(campaign.id, "Campaign should have an ID")
        self.assertEqual(campaign.land_parcel_id, self.parcel)

    def test_02_agricultural_intervention_recording_with_gps(self):
        """ Scenario: Agricultural Intervention Recording with GPS """
        intervention = self.Production.create({
            'product_id': self.product.id,
            'product_qty': 1,
            'product_uom_id': self.product.uom_id.id,
            'location_id': self.parcel.id,
            'intervention_type': 'fertilizing'
        })
        
        # Mock telemetry outside the parcel boundaries
        self.Telemetry.create({
            'production_id': intervention.id,
            'gps_lat': 31.0, 
            'gps_lng': 121.0,
        })
        
        # Trigger spatial audit logic from agri.intervention.mixin
        intervention._compute_spatial_audit()
        self.assertGreater(intervention.out_of_bounds_count, 0, "Should have flagged OOB points")
        self.assertLess(intervention.spatial_compliance_rate, 100.0)

    def test_03_weather_window_validation_for_spraying_operations(self):
        """ Scenario: Weather window validation for spraying operations """
        intervention = self.Production.create({
            'name': 'Spraying Task',
            'product_id': self.product.id,
            'product_qty': 1,
            'product_uom_id': self.product.uom_id.id,
            'location_id': self.parcel.id,
            'intervention_type': 'protection'
        })
        
        # Create bad weather forecast (Wind speed > 16 km/h)
        self.Weather.create({
            'location_id': self.parcel.id,
            'forecast_datetime': datetime.now() + timedelta(hours=2),
            'wind_speed_kmh': 20.0
        })
        
        # action_start_work triggers weather plugin 'pre_start' hook
        with self.assertRaises(UserError, msg="Weather plugin should block start due to high wind"):
            intervention.action_start_work()

    def test_04_gdd__growing_degree_days__yield_prediction(self):
        """ Scenario: GDD (Growing Degree Days) yield prediction """
        intervention = self.Production.create({
            'product_id': self.product.id,
            'product_qty': 1,
            'product_uom_id': self.product.uom_id.id,
            'location_id': self.parcel.id,
            'physiology_profile_id': self.profile.id,
            'cumulative_gdd': 0.0
        })
        
        # Day 1: T_max 25, T_min 15 -> Avg 20. Base 10 -> GDD +10
        intervention.record_daily_environmental_data(25.0, 15.0)
        self.assertEqual(intervention.cumulative_gdd, 10.0)
        
        # Day 2: T_max 30, T_min 20 -> Avg 25. Base 10 -> GDD +15
        intervention.record_daily_environmental_data(30.0, 20.0)
        self.assertEqual(intervention.cumulative_gdd, 25.0)
