# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestConvergedLocation(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestConvergedLocation, cls).setUpClass()
        cls.Location = cls.env['stock.location']

    def test_agricultural_and_gis_fields_exist_on_native_location(self):
        """ Verify that standard Odoo stock.location records support GIS and agricultural fields directly """
        loc = self.Location.create({
            'name': 'Test Converged Plot',
            'is_land_parcel': True,
            'land_nature': 'basic_farmland',
            'gps_lat': 31.2304,
            'gps_lng': 121.4737,
            'max_capacity_volume_m3': 500.0,
            'max_stocking_density': 12.5
        })
        self.assertTrue(loc.is_land_parcel)
        self.assertEqual(loc.land_nature, 'basic_farmland')
        self.assertEqual(loc.gps_lat, 31.2304)
        self.assertEqual(loc.gps_lng, 121.4737)
        self.assertEqual(loc.max_capacity_volume_m3, 500.0)
        self.assertEqual(loc.max_stocking_density, 12.5)
