# -*- coding: utf-8 -*-
from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError, UserError
import json
import uuid


@tagged('industrial_iot', 'iiot_device', 'post_install', '-at_install')
class TestIiotDevice(TransactionCase):
    """Test suite for the IiotDevice model"""

    def setUp(self):
        super().setUp()

        # Create a device profile for testing
        self.device_profile = self.env['iiot.device.profile'].create({
            'name': 'Test CNC Profile',
            'code': 'cnc_v1',
            'telemetry_topic_template': 'telemetry/{device}/data',
            'command_topic_template': 'cmd/{device}/request',
            'ota_notify_topic_template': 'ota/{device}/notify',
            'ota_status_topic_template': 'ota/{device}/status',
            'command_template': '{"action": "{{ action }}", "params": {{ params | tojson }}}',
        })

        # Create a maintenance equipment to test business reference
        self.maintenance_equipment = self.env['maintenance.equipment'].create({
            'name': 'Test CNC Machine',
            'device_id': 1,  # This is just for testing
        })

    def test_device_creation_with_valid_data(self):
        """Test creating a device with valid data"""
        device = self.env['iiot.device'].create({
            'serial_number': 'SN123456',
            'device_id': 'device_123',
            'profile_id': self.device_profile.id,
        })

        self.assertEqual(device.serial_number, 'SN123456')
        self.assertEqual(device.device_id, 'device_123')
        self.assertEqual(device.profile_id, self.device_profile)
        self.assertEqual(device.name, 'SN123456 (device_123)')
        self.assertTrue(device.is_active)
        self.assertEqual(device.connection_status, 'offline')

    def test_device_creation_generates_config_token(self):
        """Test that creating a device generates a config token automatically"""
        device = self.env['iiot.device'].create({
            'serial_number': 'SN789012',
            'device_id': 'device_456',
            'profile_id': self.device_profile.id,
        })

        self.assertIsNotNone(device.config_token)
        # Verify it's a valid UUID
        uuid.UUID(device.config_token)

    def test_device_creation_generates_device_id_from_serial(self):
        """Test that device ID is generated from serial if not provided"""
        device = self.env['iiot.device'].create({
            'serial_number': 'SN-ABC-789',
            'profile_id': self.device_profile.id,
        })

        self.assertEqual(device.device_id, 'sn_abc_789')  # Should convert hyphens to underscores

    def test_device_name_compute(self):
        """Test that device name is computed correctly"""
        device = self.env['iiot.device'].create({
            'serial_number': 'SN999',
            'device_id': 'test_device',
            'profile_id': self.device_profile.id,
        })

        self.assertEqual(device.name, 'SN999 (test_device)')

    def test_device_id_format_constraint(self):
        """Test that device ID format is validated"""
        with self.assertRaises(ValidationError):
            self.env['iiot.device'].create({
                'serial_number': 'SN456',
                'device_id': 'invalid space id',  # Contains space which is invalid
                'profile_id': self.device_profile.id,
            })

    def test_device_id_unique_constraint(self):
        """Test that device ID must be unique"""
        # Create first device
        self.env['iiot.device'].create({
            'serial_number': 'SN456',
            'device_id': 'unique_device',
            'profile_id': self.device_profile.id,
        })

        # Try to create second device with same device_id
        with self.assertRaises(ValidationError):
            self.env['iiot.device'].create({
                'serial_number': 'SN789',
                'device_id': 'unique_device',  # Same as first device
                'profile_id': self.device_profile.id,
            })

    def test_serial_number_unique_constraint(self):
        """Test that serial number must be unique"""
        # Create first device
        self.env['iiot.device'].create({
            'serial_number': 'SN-UNIQUE',
            'device_id': 'device1',
            'profile_id': self.device_profile.id,
        })

        # Try to create second device with same serial number
        with self.assertRaises(ValidationError):
            self.env['iiot.device'].create({
                'serial_number': 'SN-UNIQUE',  # Same as first device
                'device_id': 'device2',
                'profile_id': self.device_profile.id,
            })

    def test_generate_config_token_action(self):
        """Test the config token generation action"""
        device = self.env['iiot.device'].create({
            'serial_number': 'SN777',
            'device_id': 'test_config',
            'profile_id': self.device_profile.id,
        })

        old_token = device.config_token
        result = device.action_generate_config_token()

        # Check that result is a notification action
        self.assertEqual(result['type'], 'ir.actions.client')
        self.assertEqual(result['tag'], 'display_notification')

        # Check that the token was updated
        device.refresh()
        self.assertNotEqual(device.config_token, old_token)

    def test_get_topic_map(self):
        """Test that topic map is generated correctly"""
        device = self.env['iiot.device'].create({
            'serial_number': 'SN888',
            'device_id': 'test_topics',
            'profile_id': self.device_profile.id,
        })

        topic_map = device.get_topic_map()

        self.assertEqual(topic_map['telemetry'], 'telemetry/test_topics/data')
        self.assertEqual(topic_map['command'], 'cmd/test_topics/request')
        self.assertEqual(topic_map['ota_notify'], 'ota/test_topics/notify')
        self.assertEqual(topic_map['ota_status'], 'ota/test_topics/status')

    def test_get_topic_map_without_profile(self):
        """Test that topic map returns empty dict when no profile is set"""
        device = self.env['iiot.device'].create({
            'serial_number': 'SN999',
            'device_id': 'test_empty',
            'profile_id': self.device_profile.id,
        })

        # Remove profile to test empty case
        device.profile_id = False
        topic_map = device.get_topic_map()

        self.assertEqual(topic_map, {})

    def test_send_command_without_profile(self):
        """Test that sending command fails when no profile is set"""
        device = self.env['iiot.device'].create({
            'serial_number': 'SN100',
            'device_id': 'test_no_profile',
            'profile_id': self.device_profile.id,
        })

        # Remove profile
        device.profile_id = False

        with self.assertRaises(UserError):
            device.send_command('test_action')

    def test_process_telemetry_data(self):
        """Test processing telemetry data"""
        device = self.env['iiot.device'].create({
            'serial_number': 'SN200',
            'device_id': 'test_telemetry',
            'profile_id': self.device_profile.id,
        })

        # Process sample telemetry data
        telemetry_data = {
            'temperature': 25.5,
            'status': 'running',
            'counter': 1234
        }

        # This should not raise an exception even if there are no rules
        device.process_telemetry_data(telemetry_data)

        # Check that last telemetry time was updated
        self.assertIsNotNone(device.last_telemetry)
        self.assertEqual(device.connection_status, 'online')

    def test_write_updates_last_update(self):
        """Test that write method updates last_update field"""
        device = self.env['iiot.device'].create({
            'serial_number': 'SN300',
            'device_id': 'test_write',
            'profile_id': self.device_profile.id,
        })

        original_update = device.last_update
        device.write({'is_active': False})

        device.refresh()
        self.assertNotEqual(device.last_update, original_update)

    def test_business_reference_field(self):
        """Test that business reference field works"""
        device = self.env['iiot.device'].create({
            'serial_number': 'SN400',
            'device_id': 'test_business',
            'profile_id': self.device_profile.id,
            'business_ref': f'maintenance.equipment,{self.maintenance_equipment.id}'
        })

        self.assertEqual(device.business_ref, self.maintenance_equipment)