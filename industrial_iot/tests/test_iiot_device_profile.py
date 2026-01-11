# -*- coding: utf-8 -*-
from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


@tagged('industrial_iot', 'iiot_device_profile', 'post_install', '-at_install')
class TestIiotDeviceProfile(TransactionCase):
    """Test suite for the IiotDeviceProfile model"""

    def test_device_profile_creation_with_valid_data(self):
        """Test creating a device profile with valid data"""
        profile = self.env['iiot.device.profile'].create({
            'name': 'Test PLC Profile',
            'code': 'plc_v1',
            'telemetry_topic_template': 'telemetry/{device}/data',
            'command_topic_template': 'cmd/{device}/request',
            'ota_notify_topic_template': 'ota/{device}/notify',
            'ota_status_topic_template': 'ota/{device}/status',
            'command_template': '{"action": "{{ action }}", "params": {{ params | tojson }}}',
        })

        self.assertEqual(profile.name, 'Test PLC Profile')
        self.assertEqual(profile.code, 'plc_v1')
        self.assertEqual(profile.telemetry_topic_template, 'telemetry/{device}/data')
        self.assertEqual(profile.command_topic_template, 'cmd/{device}/request')

    def test_device_profile_code_format_constraint(self):
        """Test that device profile code format is validated"""
        with self.assertRaises(ValidationError):
            self.env['iiot.device.profile'].create({
                'name': 'Test Invalid Profile',
                'code': 'invalid code with spaces',  # Contains space which is invalid
                'telemetry_topic_template': 'telemetry/{device}/data',
                'command_topic_template': 'cmd/{device}/request',
            })

    def test_device_profile_topic_templates_validation(self):
        """Test that topic templates must contain {device} placeholder"""
        with self.assertRaises(ValidationError):
            self.env['iiot.device.profile'].create({
                'name': 'Test Invalid Topic Profile',
                'code': 'invalid_topic_profile',
                'telemetry_topic_template': 'telemetry/data',  # Missing {device} placeholder
                'command_topic_template': 'cmd/{device}/request',
            })

    def test_device_profile_multiple_topic_templates_validation(self):
        """Test that all topic templates are validated"""
        # Test with multiple invalid templates
        with self.assertRaises(ValidationError):
            self.env['iiot.device.profile'].create({
                'name': 'Test Multiple Invalid Topic Profile',
                'code': 'multi_invalid_profile',
                'telemetry_topic_template': 'telemetry/data',  # Missing {device}
                'command_topic_template': 'cmd/request',  # Missing {device}
                'ota_notify_topic_template': 'ota/notify',  # Missing {device}
                'ota_status_topic_template': 'ota/status',  # Missing {device}
            })

    def test_device_profile_valid_templates(self):
        """Test that valid templates with {device} placeholder are accepted"""
        profile = self.env['iiot.device.profile'].create({
            'name': 'Test Valid Profile',
            'code': 'valid_profile',
            'telemetry_topic_template': 'telemetry/{device}/data',
            'command_topic_template': 'cmd/{device}/request',
            'ota_notify_topic_template': 'ota/{device}/notify',
            'ota_status_topic_template': 'ota/{device}/status',
        })

        self.assertEqual(profile.name, 'Test Valid Profile')
        self.assertTrue('{device}' in profile.telemetry_topic_template)
        self.assertTrue('{device}' in profile.command_topic_template)
        self.assertTrue('{device}' in profile.ota_notify_topic_template)
        self.assertTrue('{device}' in profile.ota_status_topic_template)

    def test_device_profile_code_alphanumeric_underscore_hyphen_only(self):
        """Test that device profile code only allows letters, numbers, underscores and hyphens"""
        # Valid codes
        valid_codes = ['abc123', 'ABC-123', 'test_code', 'device_v1_2', 'TEST-CODE_123']
        for code in valid_codes:
            profile = self.env['iiot.device.profile'].create({
                'name': f'Test Profile {code}',
                'code': code,
                'telemetry_topic_template': 'telemetry/{device}/data',
                'command_topic_template': 'cmd/{device}/request',
            })
            self.assertEqual(profile.code, code)
            profile.unlink()  # Clean up

        # Invalid codes
        invalid_codes = ['code with spaces', 'code.with.dots', 'code/with/slashes', 'code@invalid']
        for code in invalid_codes:
            with self.assertRaises(ValidationError):
                self.env['iiot.device.profile'].create({
                    'name': f'Test Invalid Profile {code}',
                    'code': code,
                    'telemetry_topic_template': 'telemetry/{device}/data',
                    'command_topic_template': 'cmd/{device}/request',
                })

    def test_device_profile_ordering(self):
        """Test that device profiles are ordered by code"""
        # Create profiles in non-alphabetical order
        profile_c = self.env['iiot.device.profile'].create({
            'name': 'Profile C',
            'code': 'ccc',
            'telemetry_topic_template': 'telemetry/{device}/data',
            'command_topic_template': 'cmd/{device}/request',
        })

        profile_a = self.env['iiot.device.profile'].create({
            'name': 'Profile A',
            'code': 'aaa',
            'telemetry_topic_template': 'telemetry/{device}/data',
            'command_topic_template': 'cmd/{device}/request',
        })

        profile_b = self.env['iiot.device.profile'].create({
            'name': 'Profile B',
            'code': 'bbb',
            'telemetry_topic_template': 'telemetry/{device}/data',
            'command_topic_template': 'cmd/{device}/request',
        })

        # Get profiles ordered by code (which is the default order)
        profiles = self.env['iiot.device.profile'].search([], order='code')
        profile_codes = [p.code for p in profiles]

        self.assertEqual(profile_codes, ['aaa', 'bbb', 'ccc'])