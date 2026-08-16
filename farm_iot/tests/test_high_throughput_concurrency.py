# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError
import psycopg2

@tagged('post_install', '-at_install')
class TestHighThroughputConcurrency(TransactionCase):

    def setUp(self):
        super(TestHighThroughputConcurrency, self).setUp()
        self.Package = self.env['stock.package']
        self.Tracking = self.env['stock.matter.tracking']
        self.Telemetry = self.env['iiot.telemetry']
        
        self.package = self.Package.create({'name': 'PKG-CONCURRENCY-99'})
        self.carrier = self.Tracking.create({
            'name': 'LPN-CONCURRENCY-99',
            'package_id': self.package.id
        })

    def test_01_non_blocking_row_lock_nowait(self):
        """ Verify action_lock_for_write aborts immediately with a ValidationError when blocked """
        # Open parallel database cursor to handle creation, commit, and lock
        new_cr = self.registry.cursor()
        
        # 1. Insert packages and matter tracking via parallel cursor and commit so others can see it
        new_cr.execute("INSERT INTO stock_package (name) VALUES ('MAT-LOCK-777') RETURNING id")
        pkg_id = new_cr.fetchone()[0]
        new_cr.execute(
            "INSERT INTO stock_matter_tracking (id, package_id, vessel_phase, carrier_state) VALUES (%s, %s, 'idle', 'idle')",
            (pkg_id, pkg_id)
        )
        new_cr.commit()

        # 2. Re-acquire lock on the created row in the parallel cursor
        new_cr.execute("SELECT id FROM stock_matter_tracking WHERE id = %s FOR UPDATE", (pkg_id,))
        
        # 3. Open another parallel cursor representing our active session
        active_cr = self.registry.cursor()
        
        try:
            # Bind the Environment to active_cr so it can see the committed record and test the model method
            active_env = self.env(cr=active_cr)
            tracking = active_env['stock.matter.tracking'].browse(pkg_id)
            
            from odoo.exceptions import ValidationError
            with self.assertRaises(ValidationError) as context:
                # This must fail instantly because new_cr holds the row lock!
                tracking.action_lock_for_write()
            self.assertIn("CARRIER_ROW_LOCKED_TRY_AGAIN", str(context.exception))
        finally:
            active_cr.close()
            # 4. Rollback the lock, delete the row, and commit via the parallel cursor
            new_cr.rollback()
            new_cr.execute("DELETE FROM stock_matter_tracking WHERE id = %s", (pkg_id,))
            new_cr.execute("DELETE FROM stock_package WHERE id = %s", (pkg_id,))
            new_cr.commit()
            new_cr.close()

    def test_02_orm_bypass_bulk_insert(self):
        """ Verify psycopg2 execute_values bulk inserts bypass ORM overhead and write records correctly """
        vals = []
        for i in range(100):
            vals.append({
                'name': f'Bulk-Temp-{i}',
                'sensor_type': 'temperature',
                'value': 20.0 + i,
                'gps_lat': 31.0,
                'gps_lng': 121.0
            })
            
        self.Telemetry.action_bulk_insert_telemetry(vals)
        
        # Verify 100 records were successfully written
        records = self.Telemetry.search([('name', '=like', 'Bulk-Temp-%')])
        self.assertEqual(len(records), 100)

    def test_03_time_series_partitioning(self):
        """ Verify range partition insertion works and physical routing is correct """
        # Ingest record into partitioned range
        self.env.cr.execute("""
            INSERT INTO agri_telemetry_series (timestamp, sensor_type, value)
            VALUES ('2026-08-16 12:00:00', 'ph', 7.2)
        """)
        
        # Verify insertion routed to partitioned range
        self.env.cr.execute("SELECT count(*) FROM agri_telemetry_series_2026_08")
        count = self.env.cr.fetchone()[0]
        self.assertTrue(count >= 1)
