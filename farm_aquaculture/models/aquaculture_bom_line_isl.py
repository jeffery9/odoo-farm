# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class FarmAquacultureBomLine(models.Model):
    _name = 'farm.aquaculture.bom.line'
    _description = 'Aquaculture BOM Component (ISL Layer)'
    _inherits = {'mrp.bom.line': 'bom_line_id'}

    bom_line_id = fields.Many2one('mrp.bom.line', string='Base BOM Line', required=True, ondelete='cascade')

    # Aquaculture Specifics
    dose_rate_ppm = fields.Float("Dose Rate (ppm)")
    application_method = fields.Selection([
        ('direct', 'Direct Application'),
        ('water_dissolved', 'Dissolved in Water'),
        ('feed_mixed', 'Mixed with Feed'),
        ('topical', 'Topical Application'),
    ], string="Application Method")
    water_condition = fields.Selection([
        ('freshwater', 'Freshwater'),
        ('saltwater', 'Saltwater'),
        ('brackish', 'Brackish Water'),
    ], string="Water Condition", default='freshwater')