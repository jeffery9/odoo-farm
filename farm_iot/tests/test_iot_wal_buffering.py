# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged
import psycopg2

@tagged('post_install', '-at_install')
class TestIoTWALBuffering(TransactionCase):

    def setUp(self):
        super(TestIoTWALBuffering, self).setUp()
        self.WalLog = self.env['agri.iot.wal.log']

    def test_wal_idempotent_ingestion(self):
        """ Verify exactly-once ingestion guarantee using message_guid unique constraint """
        guid = "uuid-1234-abcd"
        
        # First ingestion should succeed
        log1 = self.WalLog.ingest_telemetry(guid, "TEMP-SENSOR-01", '{"temp": 24.5}')
        self.assertTrue(log1)
        
        # Second ingestion with same GUID should return False softly (idempotency check)
        log2 = self.WalLog.ingest_telemetry(guid, "TEMP-SENSOR-01", '{"temp": 24.5}')
        self.assertFalse(log2, "Ingest telemetry must return False when a duplicate GUID is provided")
