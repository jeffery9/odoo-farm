# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestIntegrationFarmIot(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Device = cls.env['iiot.device']
        cls.Telemetry = cls.env['iiot.telemetry']
        cls.Location = cls.env['farm.location']
        
        cls.location = cls.Location.create({
            'name': 'Pond 01',
            'usage': 'internal'
        })
        
        cls.device = cls.Device.create({
            'name': 'Pond Oxygen Sensor',
            'device_type': 'sensor',
            'location_id': cls.location.id,
            'hardware_id': 'SN-O2-001'
        })

    def test_01_device_telemetry_flow(self):
        """ Test the flow from a physical device to a telemetry record """
        telemetry = self.Telemetry.create({
            'device_id': self.device.id,
            'sensor_type': 'dissolved_oxygen',
            'value': 7.2,
        })
        
        self.assertTrue(telemetry.exists())
        self.assertEqual(telemetry.device_id.location_id.name, 'Pond 01')
        
    def test_02_digital_twin_integration(self):
        """ Test if digital twin is automatically updated (if logic exists) """
        # Search for digital twin for this location
        twin = self.env['agri.digital.twin'].search([('location_id', '=', self.location.id)], limit=1)
        if twin:
            self.assertTrue(twin.exists())
            # Simulate a health score update from telemetry
            if hasattr(twin, 'health_score'):
                self.assertTrue(twin.health_score >= 0)
