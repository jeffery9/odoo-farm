# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class FarmCropBomLine(models.Model):
    _name = 'farm.crop.bom.line'
    _description = 'Crop BOM Component (ISL Layer)'
    _inherits = {'mrp.bom.line': 'bom_line_id'}

    bom_line_id = fields.Many2one('mrp.bom.line', string='Base BOM Line', required=True, ondelete='cascade')

    # Crop Specifics
    application_rate = fields.Float("Application Rate (per Ha/Liter)")
    spray_volume = fields.Float("Spray Volume (L/Ha)")
    weather_condition = fields.Selection([
        ('sunny', 'Sunny'),
        ('overcast', 'Overcast'),
        ('rain_imminent', 'Rain Imminent'),
        ('windy', 'Windy'),
    ], string="Recommended Weather Condition")
    safety_interval_days = fields.Integer("Safety Interval (Days)")