# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class FarmLivestockEvent(models.Model):
    _name = 'farm.livestock.event'
    _description = 'Livestock Lifecycle Event'
    _order = 'event_date desc'

    lot_id = fields.Many2one('stock.lot', string='Animal/Group', required=True, ondelete='cascade')
    event_type = fields.Selection([
        ('birth', 'Birth'),
        ('movement', 'Group Movement'),
        ('weaning', 'Weaning'),
        ('breeding', 'Breeding/Insemination'),
        ('pregnancy_check', 'Pregnancy Check'),
        ('farrowing', 'Farrowing/Birth Event'),
        ('vaccination', 'Vaccination'),
        ('treatment', 'Medical Treatment'),
        ('weight', 'Weight Measurement'),
        ('death', 'Death/Mortality'),
        ('slaughter', 'Harvest/Slaughter')
    ], string='Event Type', required=True)
    
    event_date = fields.Datetime('Event Date', default=fields.Datetime.now, required=True)
    location_id = fields.Many2one('stock.location', string='Location')
    responsible_id = fields.Many2one('res.users', string='Responsible', default=lambda self: self.env.user)
    
    notes = fields.Text('Notes')
    
    # Specific data for different events
    measured_weight = fields.Float("Measured Weight (kg)")
    medicine_id = fields.Many2one('product.product', string="Medicine/Vaccine", domain=[('type', '=', 'consu')])
    dosage = fields.Float("Dosage")
    uom_id = fields.Many2one('uom.uom', string="Unit")
    
    # [US-64-02] Anomaly Link
    is_anomaly = fields.Boolean("Anomaly Flag", default=False)
    alert_severity = fields.Selection([('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], string="Alert Severity")

class FarmLivestockHouseEnv(models.Model):
    _name = 'farm.livestock.house.env'
    _description = 'Livestock House Environment Log'
    _order = 'capture_time desc'

    location_id = fields.Many2one('stock.location', string='House/Location', required=True)
    capture_time = fields.Datetime('Capture Time', default=fields.Datetime.now)
    
    temperature = fields.Float("Temperature (℃)")
    humidity = fields.Float("Humidity (%)")
    ammonia_level = fields.Float("Ammonia (ppm)")
    co2_level = fields.Float("CO2 (ppm)")
    
    comfort_index = fields.Float("Comfort Index", compute='_compute_comfort_index')

    @api.depends('temperature', 'humidity')
    def _compute_comfort_index(self):
        for rec in self:
            # Simple THI (Temperature Humidity Index) implementation for comfort
            rec.comfort_index = 0.8 * rec.temperature + (rec.humidity / 100.0) * (rec.temperature - 14.4) + 46.4
