# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class StorageEnvironment(models.Model):
    """US-037-06: Storage Environment Monitoring"""
    _name = 'farm.storage.env'
    _description = 'Storage Environment Log'
    _order = 'timestamp desc'

    location_id = fields.Many2one('stock.location', string='Storage Location', required=True)
    timestamp = fields.Datetime('Timestamp', default=fields.Datetime.now, required=True)
    temperature = fields.Float('Temperature (℃)')
    humidity = fields.Float('Humidity (%)')
    co2_level = fields.Float('CO2 Level (ppm)')
    
    is_alert = fields.Boolean('Is Alert', default=False)
    alert_message = fields.Char('Alert Message')
