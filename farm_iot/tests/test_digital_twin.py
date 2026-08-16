# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestDigitalTwin(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Scene = cls.env['agri.digital.twin.scene']
        cls.Marker = cls.env['agri.digital.twin.marker']
        cls.Location = cls.env['farm.location'].create({'name': 'Greenhouse 1'})
        cls.Device = cls.env['iiot.device'].create({
            'serial_number': 'TWIN-DEV-001',
            'profile_id': cls.env['iiot.device.profile'].create({
                'name': 'Twin Profile',
                'code': 'twin_profile'
            }).id
        })

    def test_01_scene_and_marker_setup(self):
        """ Test creating a 3D scene and placing a device marker """
        scene = self.Scene.create({
            'name': 'Greenhouse 1 Full View',
            'location_id': self.Location.id,
            'base_model_url': 'https://assets.geninit.ai/models/gh1.glb'
        })
        self.assertTrue(scene.exists())
        self.assertEqual(scene.state, 'draft')
        
        marker = self.Marker.create({
            'scene_id': scene.id,
            'device_id': self.Device.id,
            'pos_x': 10.5,
            'pos_y': 0.0,
            'pos_z': -5.2
        })
        self.assertTrue(marker.exists())
        self.assertEqual(len(scene.device_marker_ids), 1)

    def test_02_location_twin_enablement(self):
        """ Test linking a location to its digital twin scene """
        scene = self.Scene.create({'name': 'Temp Scene'})
        self.Location.write({
            'digital_twin_enabled': True,
            'digital_twin_scene_id': scene.id
        })
        self.assertTrue(self.Location.digital_twin_enabled)
        self.assertEqual(self.Location.digital_twin_scene_id.id, scene.id)
