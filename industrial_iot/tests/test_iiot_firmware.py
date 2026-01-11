# -*- coding: utf-8 -*-
from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


@tagged('industrial_iot', 'iiot_firmware', 'post_install', '-at_install')
class TestIiotFirmware(TransactionCase):
    """Test suite for the IiotFirmware and IiotUpdate models"""

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

        # Create a device for testing updates
        self.device = self.env['iiot.device'].create({
            'serial_number': 'SN123456',
            'device_id': 'device_123',
            'profile_id': self.device_profile.id,
        })

    def test_firmware_creation_with_valid_data(self):
        """Test creating a firmware with valid data"""
        firmware = self.env['iiot.firmware'].create({
            'version': '1.0.0',
            'profile_code': 'cnc_v1',
            'url': 'https://example.com/firmware.bin',
            'checksum': 'abc123',
            'description': 'Test firmware version 1.0.0',
        })

        self.assertEqual(firmware.version, '1.0.0')
        self.assertEqual(firmware.profile_code, 'cnc_v1')
        self.assertEqual(firmware.url, 'https://example.com/firmware.bin')
        self.assertEqual(firmware.checksum, 'abc123')
        self.assertEqual(firmware.name, 'cnc_v1 v1.0.0')
        self.assertTrue(firmware.is_active)

    def test_firmware_name_compute(self):
        """Test that firmware name is computed correctly"""
        firmware = self.env['iiot.firmware'].create({
            'version': '2.1.3',
            'profile_code': 'plc_v2',
            'url': 'https://example.com/plc_firmware.bin',
        })

        self.assertEqual(firmware.name, 'plc_v2 v2.1.3')

    def test_firmware_version_format_validation(self):
        """Test that firmware version format is validated"""
        # Valid version formats
        valid_versions = ['1.0.0', '2.1.3', 'v1.0', '1_0_0', '1-0-0', 'alpha1.0']
        for version in valid_versions:
            firmware = self.env['iiot.firmware'].create({
                'version': version,
                'profile_code': 'test_v1',
                'url': 'https://example.com/test.bin',
            })
            self.assertEqual(firmware.version, version)
            firmware.unlink()

        # Invalid version format
        with self.assertRaises(ValidationError):
            self.env['iiot.firmware'].create({
                'version': 'invalid version with spaces',  # Contains spaces which is invalid
                'profile_code': 'test_v1',
                'url': 'https://example.com/test.bin',
            })

    def test_firmware_url_format_validation(self):
        """Test that firmware URL format is validated"""
        # Valid URL formats
        valid_urls = [
            'https://example.com/firmware.bin',
            'http://example.com/firmware.bin',
            'ftp://example.com/firmware.bin'
        ]
        for url in valid_urls:
            firmware = self.env['iiot.firmware'].create({
                'version': '1.0.0',
                'profile_code': 'test_v1',
                'url': url,
            })
            self.assertEqual(firmware.url, url)
            firmware.unlink()

        # Invalid URL format
        with self.assertRaises(ValidationError):
            self.env['iiot.firmware'].create({
                'version': '1.0.0',
                'profile_code': 'test_v1',
                'url': 'invalid-url-without-protocol',  # Missing protocol
            })

    def test_firmware_unique_constraint(self):
        """Test that firmware version must be unique for each device type"""
        # Create first firmware
        self.env['iiot.firmware'].create({
            'version': '1.0.0',
            'profile_code': 'cnc_v1',
            'url': 'https://example.com/firmware1.bin',
        })

        # Try to create another firmware with same version and profile code
        with self.assertRaises(ValidationError):
            self.env['iiot.firmware'].create({
                'version': '1.0.0',  # Same version
                'profile_code': 'cnc_v1',  # Same profile code
                'url': 'https://example.com/firmware2.bin',  # Different URL but still should fail
            })

        # Creating with different version should work
        firmware = self.env['iiot.firmware'].create({
            'version': '1.0.1',  # Different version
            'profile_code': 'cnc_v1',  # Same profile code
            'url': 'https://example.com/firmware2.bin',
        })
        self.assertEqual(firmware.version, '1.0.1')

        # Creating with different profile code should work
        firmware2 = self.env['iiot.firmware'].create({
            'version': '1.0.0',  # Same version
            'profile_code': 'plc_v1',  # Different profile code
            'url': 'https://example.com/plc_firmware.bin',
        })
        self.assertEqual(firmware2.profile_code, 'plc_v1')

    def test_firmware_activation_methods(self):
        """Test firmware activation and deactivation methods"""
        firmware = self.env['iiot.firmware'].create({
            'version': '1.0.0',
            'profile_code': 'cnc_v1',
            'url': 'https://example.com/firmware.bin',
        })

        # Firmware should be active by default
        self.assertTrue(firmware.is_active)

        # Test deactivation
        result = firmware.action_deactivate()
        firmware.refresh()
        self.assertFalse(firmware.is_active)
        self.assertTrue(result)  # Should return True

        # Test re-activation
        result = firmware.action_activate()
        firmware.refresh()
        self.assertTrue(firmware.is_active)
        self.assertTrue(result)  # Should return True

    def test_firmware_ordering(self):
        """Test that firmwares are ordered by version (descending)"""
        firmware3 = self.env['iiot.firmware'].create({
            'version': '3.0.0',
            'profile_code': 'test_v1',
            'url': 'https://example.com/firmware3.bin',
        })

        firmware1 = self.env['iiot.firmware'].create({
            'version': '1.0.0',
            'profile_code': 'test_v1',
            'url': 'https://example.com/firmware1.bin',
        })

        firmware2 = self.env['iiot.firmware'].create({
            'version': '2.0.0',
            'profile_code': 'test_v1',
            'url': 'https://example.com/firmware2.bin',
        })

        # Get firmwares ordered by version (descending)
        firmwares = self.env['iiot.firmware'].search([], order='version DESC')
        versions = [f.version for f in firmwares]

        # Note: String comparison for version numbers is used here,
        # so actual ordering might not be semantically correct
        self.assertEqual(versions, ['3.0.0', '2.0.0', '1.0.0'])

    def test_update_creation_with_valid_data(self):
        """Test creating a firmware update with valid data"""
        firmware = self.env['iiot.firmware'].create({
            'version': '1.0.0',
            'profile_code': 'cnc_v1',
            'url': 'https://example.com/firmware.bin',
        })

        update = self.env['iiot.update'].create({
            'device_id': self.device.id,
            'firmware_id': firmware.id,
            'description': 'Test firmware update',
        })

        self.assertEqual(update.device_id, self.device)
        self.assertEqual(update.firmware_id, firmware)
        self.assertEqual(update.status, 'pending')
        self.assertEqual(update.name, 'device_123 -> 1.0.0')
        self.assertIsNotNone(update.update_id)

    def test_update_name_compute(self):
        """Test that update name is computed correctly"""
        firmware = self.env['iiot.firmware'].create({
            'version': '2.0.0',
            'profile_code': 'cnc_v1',
            'url': 'https://example.com/firmware.bin',
        })

        update = self.env['iiot.update'].create({
            'device_id': self.device.id,
            'firmware_id': firmware.id,
        })

        self.assertEqual(update.name, 'device_123 -> 2.0.0')

    def test_update_status_methods(self):
        """Test update status management methods"""
        firmware = self.env['iiot.firmware'].create({
            'version': '1.0.0',
            'profile_code': 'cnc_v1',
            'url': 'https://example.com/firmware.bin',
        })

        update = self.env['iiot.update'].create({
            'device_id': self.device.id,
            'firmware_id': firmware.id,
        })

        # Test initial status
        self.assertEqual(update.status, 'pending')

        # Test updating status from device
        update.update_status_from_device('downloading', progress=25.0)
        update.refresh()
        self.assertEqual(update.status, 'downloading')
        self.assertEqual(update.progress, 25.0)

        # Test success status
        update.update_status_from_device('success', progress=100.0)
        update.refresh()
        self.assertEqual(update.status, 'success')
        self.assertEqual(update.progress, 100.0)
        self.assertIsNotNone(update.end_time)

        # Create a new pending update for cancel test
        update2 = self.env['iiot.update'].create({
            'device_id': self.device.id,
            'firmware_id': firmware.id,
        })

        # Test cancel method
        update2.action_cancel_update()
        update2.refresh()
        self.assertEqual(update2.status, 'cancelled')
        self.assertIsNotNone(update2.end_time)

    def test_update_progress(self):
        """Test update progress tracking"""
        firmware = self.env['iiot.firmware'].create({
            'version': '1.0.0',
            'profile_code': 'cnc_v1',
            'url': 'https://example.com/firmware.bin',
        })

        update = self.env['iiot.update'].create({
            'device_id': self.device.id,
            'firmware_id': firmware.id,
        })

        # Update progress multiple times
        update.update_status_from_device('installing', progress=33.0)
        update.refresh()
        self.assertEqual(update.status, 'installing')
        self.assertEqual(update.progress, 33.0)

        update.update_status_from_device('installing', progress=66.0)
        update.refresh()
        self.assertEqual(update.status, 'installing')
        self.assertEqual(update.progress, 66.0)

        update.update_status_from_device('success', progress=100.0)
        update.refresh()
        self.assertEqual(update.status, 'success')
        self.assertEqual(update.progress, 100.0)