# -*- coding: utf-8 -*-
from odoo import models, fields

class EsgEnvironmentalTracker(models.Model):
    _name = 'esg.environmental.tracker'
    _description = 'Environmental Sustainability KPI Tracker'

    name = fields.Char("Metric ID", required=True)
    carbon_offset_value = fields.Float("Carbon Offset (kg Co2e)")
