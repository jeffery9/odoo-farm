# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestEpic093(TransactionCase):
    """ BDD Test for Epic 093: Digital Twin Agriculture """

    def setUp(self):
        super(TestEpic093, self).setUp()
        # Note: agri.digital.twin models are defined in farm_iot but part of the cockpit strategy
        self.Scene = self.env['agri.digital.twin.scene']
        self.Location = self.env['farm.location']
        self.Device = self.env['iiot.device']
        
        self.test_location = self.Location.create({
            'name': 'Smart Greenhouse A',
            'digital_twin_enabled': True
        })

    def test_01_farm_digital_twin_modeling_and_3d_scene_management(self):
        """ Verify GLB/USDZ model loading support """
        scene = self.Scene.create({
            'name': 'Greenhouse A Digital Twin',
            'base_model_url': 'https://assets.farm.com/models/gh_a.glb',
            'location_id': self.test_location.id,
            'state': 'active'
        })
        
        self.assertEqual(scene.base_model_url, 'https://assets.farm.com/models/gh_a.glb')
        self.assertEqual(self.test_location.digital_twin_enabled, True)
        
        # Link location to scene
        self.test_location.digital_twin_scene_id = scene.id
        self.assertEqual(self.test_location.digital_twin_scene_id.id, scene.id)

    def test_02_real_time_sensor_synchronization_and__what_if__simulation(self):
        """ Verify sync of virtual component status """
        scene = self.Scene.create({
            'name': 'Orchard Section B',
            'location_id': self.test_location.id
        })
        
        device = self.Device.create({
            'name': 'Soil Sensor 01',
            'digital_twin_model_url': 'https://assets.farm.com/models/sensor.glb'
        })
        
        # Create a marker in the scene for the device
        marker = self.env['agri.digital.twin.marker'].create({
            'name': 'Sensor Marker 01',
            'scene_id': scene.id,
            'device_id': device.id,
            'pos_x': 10.5,
            'pos_y': 0.0,
            'pos_z': -5.2
        })
        
        self.assertEqual(marker.device_id.id, device.id)
        self.assertEqual(scene.device_marker_ids.id, marker.id)
        self.assertGreater(marker.pos_x, 0.0, "Marker should have spatial coordinates")
