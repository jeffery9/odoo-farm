# -*- coding: utf-8 -*-
import json
from odoo.tests.common import TransactionCase, tagged

@tagged('post_install', '-at_install')
class TestIoTWALBuffering(TransactionCase):

    def setUp(self):
        super(TestIoTWALBuffering, self).setUp()
        self.WalLog = self.env['agri.iot.wal.log']
        self.Device = self.env['iiot.device']
        self.Package = self.env['stock.package']
        self.Tracking = self.env['stock.matter.tracking']

        # Scaffold standard SFC entities
        self.package = self.Package.create({'name': 'PKG-TEST-WAL-01'})
        self.carrier = self.Tracking.create({
            'name': 'LPN-TEST-WAL-01',
            'package_id': self.package.id
        })

    def test_wal_idempotent_ingestion(self):
        """ Verify exactly-once ingestion guarantee using message_guid unique constraint """
        guid = "uuid-1234-abcd"
        
        # First ingestion should succeed
        log1 = self.WalLog.ingest_telemetry(guid, "TEMP-SENSOR-01", '{"temp": 24.5}')
        self.assertTrue(log1)
        
        # Second ingestion with same GUID should return False softly (idempotency check)
        log2 = self.WalLog.ingest_telemetry(guid, "TEMP-SENSOR-01", '{"temp": 24.5}')
        self.assertFalse(log2, "Ingest telemetry must return False when a duplicate GUID is provided")

    def test_wal_processing_invalid_json(self):
        """ Verify that WAL process gracefully fails and flags 'failed' on malformed JSON payload """
        invalid_payload = "{this-is-not-valid-json: 42"
        log = self.WalLog.ingest_telemetry(
            guid="uuid-err-json",
            device_id="ERR-DEVICE-01",
            payload=invalid_payload,
            target_id=self.carrier.id
        )
        self.assertTrue(log)
        self.assertEqual(log.status, 'pending')

        # Run process action
        self.WalLog.action_process_pending_wal()
        self.assertEqual(log.status, 'failed', "WAL processing must mark logs as 'failed' when JSON is corrupted")

    def test_wal_processing_fallback_device_creation(self):
        """ Verify that WAL process automatically spawns a fallback iiot.device Node when the sender doesn't exist """
        unique_device_id = "NON-EXISTENT-DEVICE-99"
        
        # Ensure device doesn't exist initially
        device_pre = self.Device.search([('device_id', '=', unique_device_id)])
        self.assertFalse(device_pre)

        # Ingest and process
        payload_data = {'temp': 22.8, 'sensor_type': 'temperature'}
        log = self.WalLog.ingest_telemetry(
            guid="uuid-fallback-99",
            device_id=unique_device_id,
            payload=json.dumps(payload_data)
        )
        self.assertTrue(log)
        
        # Run process action
        self.WalLog.action_process_pending_wal()
        self.assertEqual(log.status, 'processed')

        # Assert fallback device was automatically spawned in Odoo IoT Registry
        device_post = self.Device.search([('device_id', '=', unique_device_id)], limit=1)
        self.assertTrue(device_post, "SOP Step 3: Device Registry must automatically create a fallback node on unknown telemetry")
        self.assertEqual(device_post.physical_level, 'node')

        # Verify real telemetry record exists and is correctly associated
        telemetry = self.env['iiot.telemetry'].search([('device_id', '=', device_post.id)], limit=1)
        self.assertTrue(telemetry)
        self.assertEqual(telemetry.value, 22.8)

    def test_wal_processing_carrier_state_propagation(self):
        """ Verify GPS geolocation and LPN physical weight are correctly propagated to SFC carrier """
        payload_data = {
            'sensor_type': 'scale',
            'weight': 850.5,
            'gps_lat': 31.5002,
            'gps_lng': 120.6004,
            'level': 'info'
        }
        log = self.WalLog.ingest_telemetry(
            guid="uuid-propagation-101",
            device_id="SCALE-NODE-01",
            payload=json.dumps(payload_data),
            target_id=self.carrier.id
        )
        self.assertTrue(log)

        # Process the telemetry WAL log
        self.WalLog.action_process_pending_wal()
        self.assertEqual(log.status, 'processed')

        # Verify that carrier's physical state updated in real-time
        self.assertEqual(self.carrier.current_weight, 850.5)
        self.assertAlmostEqual(self.carrier.last_gps_lat, 31.5002)
        self.assertAlmostEqual(self.carrier.last_gps_lng, 120.6004)
        self.assertEqual(self.carrier.last_location_update, log.timestamp)

    def test_wal_processing_exception_recovery(self):
        """ Verify exception safety: non-float telemetry values must flag the log as 'failed' instead of raising a database block """
        bad_payload = {
            'sensor_type': 'temperature',
            'temp': 'NOT_A_FLOAT_VALUE_COLLISION'
        }
        log = self.WalLog.ingest_telemetry(
            guid="uuid-exc-recovery-202",
            device_id="TEMP-SENSOR-01",
            payload=json.dumps(bad_payload)
        )
        self.assertTrue(log)

        # Process should gracefully fail and update state to 'failed' rather than locking the transaction
        self.WalLog.action_process_pending_wal()
        self.assertEqual(log.status, 'failed', "WAL processing must softly flag 'failed' when payload data type conversion errors occur")
