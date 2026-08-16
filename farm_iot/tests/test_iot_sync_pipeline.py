# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged
import json

@tagged('post_install', '-at_install')
class TestIoTSyncPipeline(TransactionCase):

    def setUp(self):
        super(TestIoTSyncPipeline, self).setUp()
        self.WalLog = self.env['agri.iot.wal.log']
        self.Device = self.env['iiot.device']
        self.Package = self.env['stock.package']
        self.Tracking = self.env['stock.matter.tracking']

        # Scaffold sample entities
        self.package = self.Package.create({'name': 'PKG-ASYNC-99'})
        self.carrier = self.Tracking.create({
            'name': 'LPN-ASYNC-99',
            'package_id': self.package.id
        })

    def test_01_asynchronous_ingestion_and_chatter_sync(self):
        """ Verify raw pending WAL log resolves to physical telemetry, updates carrier weight, and posts chatter card """
        payload_data = {
            'sensor_type': 'temperature',
            'value': 28.5,
            'current_weight': 420.5,
            'gps_lat': 31.2304,
            'gps_lng': 121.4737,
            'level': 'warning'
        }
        
        # 1. Ingest raw log into buffer queue
        log = self.WalLog.ingest_telemetry(
            guid="uuid-async-99",
            device_id="TEMP-SENSOR-01",
            payload=json.dumps(payload_data),
            target_id=self.carrier.id
        )
        self.assertTrue(log)
        self.assertEqual(log.status, 'pending')

        # 2. Trigger the asynchronous sync pipeline action
        self.WalLog.action_process_pending_wal()

        # 3. Assert WAL log transitioned to processed status
        self.assertEqual(log.status, 'processed')

        # 4. Verify iiot.telemetry record was created
        telemetry = self.env['iiot.telemetry'].search([('device_id.device_id', '=', 'TEMP-SENSOR-01')])
        self.assertTrue(telemetry)
        self.assertEqual(telemetry.value, 28.5)
        self.assertEqual(telemetry.sensor_type, 'temperature')

        # 5. Verify target carrier physical property was reactive-synced
        self.assertAlmostEqual(self.carrier.current_weight, 420.5, delta=0.1)
        self.assertAlmostEqual(self.carrier.last_gps_lat, 31.2304, delta=0.0001)

        # 6. Verify device shadow JSON was cached
        device = self.Device.search([('device_id', '=', 'TEMP-SENSOR-01')], limit=1)
        self.assertTrue(device.shadow_state)
        self.assertIn('"value": 28.5', device.shadow_state)

        # 7. Verify messaging-first chatter cards are successfully logged
        messages = self.env['mail.message'].search([
            ('res_id', '=', self.carrier.id),
            ('model', '=', 'stock.matter.tracking'),
            ('subtype_id', '=', self.env.ref('farm_core.mt_subtype_iot_telemetry').id)
        ])
        self.assertTrue(len(messages) >= 1)
        self.assertIn('TEMP-SENSOR-01', messages[0].body)
