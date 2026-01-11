# -*- coding: utf-8 -*-
from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
import json


@tagged('industrial_iot', 'iiot_telemetry_rule', 'post_install', '-at_install')
class TestIiotTelemetryRule(TransactionCase):
    """Test suite for the IiotTelemetryRule model"""

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

    def test_telemetry_rule_creation_with_valid_data(self):
        """Test creating a telemetry rule with valid data"""
        rule = self.env['iiot.telemetry.rule'].create({
            'name': 'Temperature Monitoring Rule',
            'profile_id': self.device_profile.id,
            'json_path': '$.temperature',
            'target_model': 'maintenance.equipment',
            'target_domain': "[('id', '=', {{ device_id }})]",
            'target_field': 'x_temperature',
        })

        self.assertEqual(rule.name, 'Temperature Monitoring Rule')
        self.assertEqual(rule.profile_id, self.device_profile)
        self.assertEqual(rule.json_path, '$.temperature')
        self.assertEqual(rule.target_model, 'maintenance.equipment')
        self.assertEqual(rule.target_field, 'x_temperature')

    def test_json_path_validation(self):
        """Test that JSON path format is validated"""
        # Valid JSON path
        rule = self.env['iiot.telemetry.rule'].create({
            'name': 'Valid Rule',
            'profile_id': self.device_profile.id,
            'json_path': '$.sensor.value',
            'target_model': 'maintenance.equipment',
            'target_domain': "[('id', '=', 1)]",
            'target_field': 'x_data',
        })
        self.assertEqual(rule.json_path, '$.sensor.value')

        # Invalid JSON path should raise ValidationError
        with self.assertRaises(ValidationError):
            self.env['iiot.telemetry.rule'].create({
                'name': 'Invalid Rule',
                'profile_id': self.device_profile.id,
                'json_path': '$.sensor.[invalid]',  # Invalid syntax
                'target_model': 'maintenance.equipment',
                'target_domain': "[('id', '=', 1)]",
                'target_field': 'x_data',
            })

    def test_target_domain_validation(self):
        """Test that target domain format is validated"""
        # Valid domain
        rule = self.env['iiot.telemetry.rule'].create({
            'name': 'Valid Domain Rule',
            'profile_id': self.device_profile.id,
            'json_path': '$.value',
            'target_model': 'maintenance.equipment',
            'target_domain': "[('id', '=', 1), ('name', '=', 'test')]",
            'target_field': 'x_data',
        })
        self.assertEqual(rule.target_domain, "[('id', '=', 1), ('name', '=', 'test')]")

        # Invalid domain should raise ValidationError
        with self.assertRaises(ValidationError):
            self.env['iiot.telemetry.rule'].create({
                'name': 'Invalid Domain Rule',
                'profile_id': self.device_profile.id,
                'json_path': '$.value',
                'target_model': 'maintenance.equipment',
                'target_domain': "[('id', '=', 1",  # Missing closing bracket
                'target_field': 'x_data',
            })

    def test_evaluate_domain_method(self):
        """Test the evaluate_domain method"""
        rule = self.env['iiot.telemetry.rule'].create({
            'name': 'Domain Eval Rule',
            'profile_id': self.device_profile.id,
            'json_path': '$.value',
            'target_model': 'maintenance.equipment',
            'target_domain': "[('id', '=', {{ device_id }})]",
            'target_field': 'x_data',
        })

        # Test domain evaluation with device ID
        expected_domain = "[('id', '=', 123)]"
        evaluated = rule.evaluate_domain(123)

        # The evaluated domain should replace {{ device_id }} with actual ID
        self.assertIn('123', str(evaluated))

    def test_telemetry_rule_sequence(self):
        """Test that telemetry rules can be ordered by sequence"""
        rule3 = self.env['iiot.telemetry.rule'].create({
            'name': 'Rule 3',
            'profile_id': self.device_profile.id,
            'json_path': '$.value',
            'target_model': 'maintenance.equipment',
            'target_domain': "[('id', '=', 1)]",
            'target_field': 'x_data',
            'sequence': 30,
        })

        rule1 = self.env['iiot.telemetry.rule'].create({
            'name': 'Rule 1',
            'profile_id': self.device_profile.id,
            'json_path': '$.value',
            'target_model': 'maintenance.equipment',
            'target_domain': "[('id', '=', 1)]",
            'target_field': 'x_data',
            'sequence': 10,
        })

        rule2 = self.env['iiot.telemetry.rule'].create({
            'name': 'Rule 2',
            'profile_id': self.device_profile.id,
            'json_path': '$.value',
            'target_model': 'maintenance.equipment',
            'target_domain': "[('id', '=', 1)]",
            'target_field': 'x_data',
            'sequence': 20,
        })

        # Get rules ordered by sequence
        rules = self.env['iiot.telemetry.rule'].search(
            [('profile_id', '=', self.device_profile.id)],
            order='sequence, id'
        )

        rule_names = [r.name for r in rules]
        self.assertEqual(rule_names, ['Rule 1', 'Rule 2', 'Rule 3'])

    def test_telemetry_rule_active_field(self):
        """Test the active field functionality"""
        rule = self.env['iiot.telemetry.rule'].create({
            'name': 'Inactive Rule',
            'profile_id': self.device_profile.id,
            'json_path': '$.status',
            'target_model': 'maintenance.equipment',
            'target_domain': "[('id', '=', 1)]",
            'target_field': 'x_status',
            'active': False,
        })

        self.assertFalse(rule.active)

        # Test activating the rule
        rule.active = True
        self.assertTrue(rule.active)

    def test_telemetry_rule_required_fields(self):
        """Test that required fields are validated"""
        # Name is required
        with self.assertRaises(Exception):  # Should raise a validation error
            self.env['iiot.telemetry.rule'].create({
                # 'name': missing
                'profile_id': self.device_profile.id,
                'json_path': '$.value',
                'target_model': 'maintenance.equipment',
                'target_domain': "[('id', '=', 1)]",
                'target_field': 'x_data',
            })

        # Profile ID is required
        with self.assertRaises(Exception):  # Should raise a validation error
            self.env['iiot.telemetry.rule'].create({
                'name': 'Missing Profile Rule',
                # 'profile_id': missing
                'json_path': '$.value',
                'target_model': 'maintenance.equipment',
                'target_domain': "[('id', '=', 1)]",
                'target_field': 'x_data',
            })

        # JSON path is required
        with self.assertRaises(Exception):  # Should raise a validation error
            self.env['iiot.telemetry.rule'].create({
                'name': 'Missing JSON Path Rule',
                'profile_id': self.device_profile.id,
                # 'json_path': missing
                'target_model': 'maintenance.equipment',
                'target_domain': "[('id', '=', 1)]",
                'target_field': 'x_data',
            })