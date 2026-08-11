# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class StockMove(models.Model):
    _inherit = 'stock.move'

    # US-TECH-05-07: Industry Context Tag
    industry_context = fields.Selection([
        ('standard', 'General'),
        ('livestock', 'Livestock'),
        ('winemaking', 'Winemaking'),
        ('food_processing', 'Food Processing'),
        ('crop', 'Crop Farming')
    ], string='Industry Context', index=True, help="Categorizes inventory value by industry.")
