# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError

@tagged('post_install', '-at_install')
class TestPostGIS3DUAV(TransactionCase):

    def setUp(self):
        super(TestPostGIS3DUAV, self).setUp()
        # Create a restricted flight zone (altitude starts at 10m)
        self.restricted_zone = self.env['farm.location'].create({
            'name': 'RESTRICTED-AIRSPACE (施肥红线空域走廊)',
            'geom_3d_polygon': 'POLYGON Z ((0 0 10, 0 10 10, 10 10 10, 10 0 10, 0 0 10))'
        })

    def test_uav_intersection_intrusion(self):
        """ Verify drone flying through the Z-axis boundary gets detected """
        # Flight path starting at (5,5,5m) and ending at (5,5,15m) -> Intersects the restricted zone at (5,5,10m)
        intrusion_path = 'LINESTRING Z (5 5 5, 5 5 15)'
        has_intersected = self.restricted_zone.check_uav_trajectory_intersection(intrusion_path)
        self.assertTrue(has_intersected, "Drone altitude intrusion must trigger 3D PostGIS intersection!")

    def test_uav_clear_flight(self):
        """ Verify drone flying well below restricted airspace does not trigger intersection """
        # Flight path starting at (5,5,2m) and ending at (5,5,8m) -> Strictly below 10m restricted boundary
        safe_path = 'LINESTRING Z (5 5 2, 5 5 8)'
        has_intersected = self.restricted_zone.check_uav_trajectory_intersection(safe_path)
        self.assertFalse(has_intersected, "Safe drone path below restricted altitude must not trigger intersection.")
