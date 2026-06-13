# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
import json

class TestIiotRefactoring(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Profile = cls.env['iiot.device.profile']
        cls.Device = cls.env['iiot.device']
        cls.Gateway = cls.env['iiot.gateway']
        cls.Location = cls.env['farm.location']
        
        cls.mqtt_profile = cls.Profile.create({
            'name': 'Refactoring Test Profile',
            'code': 'REF-MQTT',
            'telemetry_topic_template': 'telemetry/{device}',
            'command_topic_template': 'command/{device}',
        })

    def test_01_physical_hierarchy(self):
        """ Test ISA-95 Physical Topology in agri_iot """
        gateway = self.Device.create({
            'serial_number': 'GATE-001',
            'profile_id': self.mqtt_profile.id,
            'physical_level': 'gateway',
        })
        
        node = self.Device.create({
            'serial_number': 'NODE-001',
            'profile_id': self.mqtt_profile.id,
            'physical_level': 'node',
            'parent_id': gateway.id,
        })
        
        sensor = self.Device.create({
            'serial_number': 'SENS-001',
            'profile_id': self.mqtt_profile.id,
            'physical_level': 'sensor',
            'parent_id': node.id,
        })

        self.assertEqual(node.parent_id, gateway)
        self.assertIn(node, gateway.child_ids)
        self.assertEqual(sensor.parent_id, node)
        self.assertIn(sensor, node.child_ids)

    def test_02_logical_hierarchy_isa95(self):
        """ Test ISA-95 Logical Hierarchy in farm_iot """
        site = self.Location.create({
            'name': 'Main Farm',
            'isa95_level': 'site',
        })
        
        area = self.Location.create({
            'name': 'Greenhouse A',
            'isa95_level': 'area',
            'parent_id': site.id,
        })
        
        unit = self.Location.create({
            'name': 'Rack 1',
            'isa95_level': 'unit',
            'parent_id': area.id,
        })

        device = self.Device.create({
            'serial_number': 'DEV-L-001',
            'profile_id': self.mqtt_profile.id,
            'location_id': unit.id,
        })

        self.assertEqual(device.site_id, site, "Site should be automatically resolved via hierarchy")

    def test_03_device_shadow(self):
        """ Test Device Shadow state merging """
        device = self.Device.create({
            'serial_number': 'SHADOW-001',
            'profile_id': self.mqtt_profile.id,
        })
        
        # Simulate first telemetry
        device.process_telemetry_data({'temp': 25.5, 'humidity': 60})
        shadow = json.loads(device.shadow_state)
        self.assertEqual(shadow.get('temp'), 25.5)
        self.assertEqual(shadow.get('humidity'), 60)
        
        # Simulate second telemetry with partial update
        device.process_telemetry_data({'temp': 26.0, 'battery': 95})
        shadow = json.loads(device.shadow_state)
        self.assertEqual(shadow.get('temp'), 26.0)
        self.assertEqual(shadow.get('humidity'), 60, "Old values should be preserved if not in update")
        self.assertEqual(shadow.get('battery'), 95)

    def test_04_gateway_registration_and_config(self):
        """ Test Gateway auto-registration logic via controller/model """
        # Directly test the model logic used by the controller
        gateway = self.Gateway.create({
            'gateway_id': 'bridge-test-01',
            'name': 'Test Bridge',
            'url': 'http://127.0.0.1:8000',
            'mqtt_host': 'mqtt.test.com',
            'mqtt_port': 1883
        })
        
        self.assertEqual(gateway.state, 'offline')
        
        # Simulate registration update
        gateway.write({'state': 'online', 'last_seen': self.env.cr.now()})
        self.assertEqual(gateway.state, 'online')

    def test_05_event_correlation_business_logic(self):
        """ Test Farm Event Correlation logic """
        correlation = self.env['farm.event.correlation'].create({
            'name': 'High Heat and Dry',
            'rule_type': 'all',
            'time_window': 600,
            'action_type': 'notification',
        })
        
        self.env['farm.event.correlation.condition'].create({
            'correlation_id': correlation.id,
            'sensor_type': 'temperature',
            'operator': '>',
            'threshold': 35.0,
        })
        
        self.env['farm.event.correlation.condition'].create({
            'correlation_id': correlation.id,
            'sensor_type': 'humidity',
            'operator': '<',
            'threshold': 20.0,
        })

        device = self.Device.create({
            'serial_number': 'CORR-001',
            'profile_id': self.mqtt_profile.id,
        })

        # 1. Post humidity (should not trigger yet)
        self.env['iiot.telemetry'].create({
            'name': 'H-Sens',
            'sensor_type': 'humidity',
            'value': 15.0,
            'device_id': device.id,
        })
        
        # 2. Post temperature (should trigger)
        # Note: We expect the action to be called. In Odoo tests, we can check side effects like chatter messages.
        temp_telemetry = self.env['iiot.telemetry'].create({
            'name': 'T-Sens',
            'sensor_type': 'temperature',
            'value': 40.0,
            'device_id': device.id,
        })
        
        # Check if notification was posted to device chatter
        messages = self.env['mail.message'].search([('res_id', '=', device.id), ('model', '=', 'iiot.device')])
        self.assertTrue(any("Correlation detected" in m.body for m in messages))
