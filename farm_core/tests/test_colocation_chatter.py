# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestColocationChatter(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Package = cls.env['stock.package']
        cls.Tracking = cls.env['stock.matter.tracking']
        
        cls.package = cls.Package.create({'name': 'PKG-TEST-COLOCATION'})
        cls.tracking = cls.Tracking.create({
            'name': 'LPN-TEST-COLOCATION',
            'package_id': cls.package.id
        })

    def test_01_log_iot_event(self):
        """Verify IoT telemetry correctly posts a message with the correct subtype."""
        self.tracking.log_iot_event('TEMP-SENSOR-01', '{"temp": 25.5}', level='critical')
        
        messages = self.env['mail.message'].search([
            ('res_id', '=', self.tracking.id),
            ('model', '=', 'stock.matter.tracking'),
            ('subtype_id', '=', self.env.ref('farm_core.mt_subtype_iot_telemetry').id)
        ])
        
        self.assertTrue(len(messages) >= 1)
        self.assertIn('TEMP-SENSOR-01', messages[0].body)
        self.assertIn('red', messages[0].body)

    def test_02_log_ai_decision(self):
        """Verify AI Agent decision correctly posts a message with the correct subtype."""
        self.tracking.log_ai_decision('Yield-Agent', 'Adjust Density', 92.5, 'Based on high sunlight hours.')
        
        messages = self.env['mail.message'].search([
            ('res_id', '=', self.tracking.id),
            ('model', '=', 'stock.matter.tracking'),
            ('subtype_id', '=', self.env.ref('farm_core.mt_subtype_ai_decision').id)
        ])
        
        self.assertTrue(len(messages) >= 1)
        self.assertIn('Yield-Agent', messages[0].body)
        self.assertIn('92.5', messages[0].body)
