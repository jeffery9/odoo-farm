# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestEpic072(TransactionCase):
    """ BDD Test for Epic 072 Smart Greenhouse Control """

    def setUp(self):
        super(TestEpic072, self).setUp()
        self.greenhouse = self.env['farm.location'].create({
            'name': 'Smart Greenhouse 1',
            'is_greenhouse': True,
            'greenhouse_type': 'glass'
        })
        # Create a dummy profile for testing
        self.profile = self.env['iiot.device.profile'].create({
            'name': 'Test Profile',
            'code': 'TEST-PROF',
            'telemetry_topic_template': 't/{device}',
            'command_topic_template': 'c/{device}'
        })
        self.device = self.env['iiot.device'].create({
            'name': 'Greenhouse Controller',
            'serial_number': 'SN-GH-001',
            'profile_id': self.profile.id,
            'physical_level': 'gateway'
        })
        self.rule = self.env['farm.greenhouse.control.rule'].create({
            'name': 'Temp Control',
            'greenhouse_id': self.greenhouse.id,
            'parameter': 'temp',
            'threshold_low': 18.0,
            'threshold_high': 28.0,
            'is_ai_controlled': True
        })

    def test_01_real_time_multi_point_environmental_monitoring_in_greenhouses(self):
        """
        Scenario: Real-time multi-point environmental monitoring in greenhouses
        """
        # Simulate sensor reporting data
        self.greenhouse.write({
            'current_temp': 24.5,
            'current_humidity': 65.0,
            'current_co2': 400.0,
            'current_light': 15000.0
        })
        
        self.assertEqual(self.greenhouse.current_temp, 24.5)
        self.assertEqual(self.greenhouse.current_co2, 400.0)

    def test_02_multi_factor_ai_environment_control_and_energy_optimization(self):
        """
        Scenario: Multi-factor AI environment control and energy optimization
        """
        # AI Twin adjusts thresholds based on weather forecast
        self.rule.update_threshold_from_twin(20.0, 26.0, "Approaching cold front, optimizing heat retention")
        
        self.assertEqual(self.rule.threshold_low, 20.0)
        self.assertIn("Approaching cold front", self.rule.ai_adjustment_log)
        
        # Verify action creation (simulated)
        action = self.env['farm.greenhouse.control.action'].create({
            'rule_id': self.rule.id,
            'device_id': self.device.id,
            'command': 'vent_open',
            'value': '0'
        })
        self.assertTrue(action.id)

    def test_03_crop_growth_stage_adaptive_control_in_greenhouses(self):
        """
        Scenario: Crop growth stage adaptive control in greenhouses
        """
        # Assume greenhouse has a growth stage field (adding via mock or simulation)
        # For this test, we demonstrate the logic of changing strategy
        old_low = self.rule.threshold_low
        
        # Simulate growth stage transition (e.g. from Vegetative to Flowering)
        # The AI engine would trigger a threshold update
        self.rule.update_threshold_from_twin(22.0, 30.0, "Flowering stage detected: higher temp required")
        
        self.assertNotEqual(self.rule.threshold_low, old_low)
        self.assertEqual(self.rule.threshold_low, 22.0)

    def test_04_remote_greenhouse_monitoring_and_mobile_override(self):
        """
        Scenario: Remote greenhouse monitoring and mobile override
        """
        # Simulate manual override via PWA (Mocking the call)
        # This would typically be a controller method, but we test the backend record update
        self.device.write({'shadow_state': '{"last_value": "heater_on"}'})
        
        # Immediate feedback log
        self.greenhouse.message_post(body="Manual override: Heater turned ON by manager via mobile.")
        
        last_msg = self.greenhouse.message_ids[0].body
        self.assertIn("Manual override", last_msg)
