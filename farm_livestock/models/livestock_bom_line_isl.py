# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class FarmLivestockBomLine(models.Model):
    _name = 'agri.isl.livestock.bom.line'
    _description = 'Livestock BOM Component (ISL Layer)'
    _inherits = {'mrp.bom.line': 'bom_line_id'}

    bom_line_id = fields.Many2one('mrp.bom.line', string='Base BOM Line', required=True, ondelete='cascade')

    # Livestock Specifics (moved from farm_operation)
    dilution_ratio = fields.Float(
        "Dilution Ratio (1:N)",
        help="If set, the component quantity will be calculated as (Finished Qty / Ratio). E.g. 1:500."
    )
    feeding_ratio = fields.Float(
        "Feeding Ratio (%)",
        help="Percentage of total biomass (Count * Avg Weight) for daily feeding."
    )
    feed_purpose = fields.Selection([
        ('starter', 'Starter Feed'),
        ('grower', 'Grower Feed'),
        ('finisher', 'Finisher Feed'),
        ('medicated', 'Medicated Feed'),
        ('treatment', 'Treatment'),
    ], string="Feed Purpose")