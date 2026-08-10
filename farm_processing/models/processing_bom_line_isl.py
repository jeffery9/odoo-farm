# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class FarmProcessingBomLine(models.Model):
    _name = 'farm.processing.bom.line'
    _description = 'Processing BOM Component (ISL Layer)'
    _inherits = {'mrp.bom.line': 'bom_line_id'}

    bom_line_id = fields.Many2one('mrp.bom.line', string='Base BOM Line', required=True, ondelete='cascade')

    # Processing Specifics
    blend_ratio = fields.Float("Blend Ratio")
    additive_type = fields.Selection([
        ('preservative', 'Preservative'),
        ('flavoring', 'Flavoring'),
        ('vitamin', 'Vitamin/Supplement'),
        ('processing_aid', 'Processing Aid'),
    ], string="Additive Type")
    processing_role = fields.Selection([
        ('main_ingredient', 'Main Ingredient'),
        ('additive', 'Additive'),
        ('processing_aid', 'Processing Aid'),
        ('packaging', 'Packaging Material'),
    ], string="Processing Role")
class FarmProcessingBomLineExtension(models.Model):    _inherit = 'farm.processing.bom.line'

    ingredient_role = fields.Selection([
        ('main', 'Main Material'),
        ('additive', 'Additive'),
        ('yeast', 'Fermentation Agent'),
        ('packaging', 'Packaging')
    ], string='Ingredient Role', default='main')

