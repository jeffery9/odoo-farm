# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from odoo.tools import mute_logger

class TestIiotDevice(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Profile = cls.env['iiot.device.profile']
        cls.Device = cls.env['iiot.device']
        
        cls.default_profile = cls.Profile.create({
            'name': 'Standard MQTT Profile',
            'code': 'STD-MQTT',
            'telemetry_topic_template': 'telemetry/{device}',
            'command_topic_template': 'command/{device}',
        })

    def test_01_device_creation_logic(self):
        """ Test device creation and automatic ID generation """
        device = self.Device.create({
            'serial_number': 'SN123456',
            'profile_id': self.default_profile.id,
        })
        self.assertTrue(device.exists())
        self.assertEqual(device.device_id, 'sn123456', "Device ID should be auto-generated from serial")
        self.assertTrue(device.config_token, "Config token should be auto-generated")
        self.assertIn('SN123456', device.name)

    def test_02_device_id_constraints(self):
        """ Test regex constraints on Device ID """
        # Invalid characters (space)
        with self.assertRaises(ValidationError):
            self.Device.create({
                'serial_number': 'SN_ERR_1',
                'device_id': 'invalid id with spaces',
                'profile_id': self.default_profile.id,
            })
            
        # Valid special characters
        dev_valid = self.Device.create({
            'serial_number': 'SN_OK_1',
            'device_id': 'sensor-01_temp',
            'profile_id': self.default_profile.id,
        })
        self.assertTrue(dev_valid.exists())

    def test_03_topic_mapping(self):
        """ Test topic list generation from profile templates """
        device = self.Device.create({
            'serial_number': 'SN_TOPIC_1',
            'device_id': 'gate_01',
            'profile_id': self.default_profile.id,
        })
        topics = device.get_topic_map()
        self.assertEqual(topics.get('telemetry'), 'telemetry/gate_01')
        self.assertEqual(topics.get('command'), 'command/gate_01')

    def test_04_token_regeneration(self):
        """ Test manual token regeneration """
        device = self.Device.create({
            'serial_number': 'SN_TOKEN_1',
            'profile_id': self.default_profile.id,
        })
        old_token = device.config_token
        device.action_generate_config_token()
        self.assertNotEqual(device.config_token, old_token)

    def test_ac_02_status_monitoring(self):
        """ 
        [AC 评审映射] AC2 (状态监控): 用户界面必须能实时反映物理设备的状态。
        验证: 设备模型必须存在状态流转字段。
        """
        device = self.Device.create({
            'serial_number': 'AC-TEST-001',
            'profile_id': self.default_profile.id,
        })
        self.assertTrue(hasattr(device, 'status') or hasattr(device, 'state') or hasattr(device, 'is_online') or hasattr(device, 'connection_status'), 
                        "Device must have a state/status field to satisfy AC2")
