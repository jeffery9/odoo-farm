# -*- coding: utf-8 -*-
from odoo import models, fields, api

class AgriTelemetrySeries(models.Model):
    _name = 'agri.telemetry.series'
    _description = 'Agri Telemetry Time-Series Partitioned Ledger'
    _order = 'timestamp desc'
    _auto = False # Prevent standard Odoo table creation to handle DDL manually

    timestamp = fields.Datetime("Timestamp", required=True)
    sensor_type = fields.Char("Sensor Type", required=True)
    value = fields.Float("Reading Value", required=True)

    def init(self):
        """ Create the range-partitioned base table and simulation partitions """
        self.env.cr.execute("""
            CREATE TABLE IF NOT EXISTS agri_telemetry_series (
                id SERIAL,
                timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                sensor_type VARCHAR NOT NULL,
                value DOUBLE PRECISION NOT NULL
            ) PARTITION BY RANGE (timestamp);
        """)
        
        # Create default partition range for year 2026
        self.env.cr.execute("""
            CREATE TABLE IF NOT EXISTS agri_telemetry_series_2026_08
            PARTITION OF agri_telemetry_series
            FOR VALUES FROM ('2026-08-01 00:00:00') TO ('2026-09-01 00:00:00');
        """)
