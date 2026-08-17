# -*- coding: utf-8 -*-
from odoo import models, fields, api

class AgriTelemetrySeries(models.Model):
    _name = 'agri.telemetry.series'
    _description = 'Agri Telemetry Time-Series Partitioned Ledger'
    _order = 'timestamp desc'
    _auto = True # Let Odoo manage table creation directly to make registry validator happy

    timestamp = fields.Datetime("Timestamp", required=True)
    sensor_type = fields.Char("Sensor Type", required=True)
    value = fields.Float("Reading Value", required=True)

