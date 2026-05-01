from odoo.tests.common import TransactionCase
from datetime import date, timedelta
from odoo import fields

class TestWeatherIntegration(TransactionCase):

    def setUp(self):
        super().setUp()
        self.agri_loc = self.env['agri.location'].create({
            'name': 'Weather Station A',
            'location_type': 'field',
            'geo_point': '121.0,31.0'
        })
        self.parcel = self.env['farm.location'].create({
            'name': 'Weather Parcel',
            'agri_location_id': self.agri_loc.id,
            'is_land_parcel': True
        })

    def test_01_forecast_data(self):
        """ Test creating weather forecast data """
        forecast = self.env['agri.weather.forecast'].create({
            'location_id': self.parcel.id,
            'date': fields.Date.today() + timedelta(days=1),
            'temp_max': 25.5,
            'temp_min': 15.0,
            'humidity': 60.0,
            'precipitation': 10.0
        })
        self.assertEqual(forecast.temp_max, 25.5)
        self.assertTrue(forecast.id)
