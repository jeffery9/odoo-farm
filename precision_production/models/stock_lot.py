# -*- coding: utf-8 -*-
from odoo import models, fields

class StockLot(models.Model):
    _inherit = ['stock.lot', 'precision.production.mixin']
    quality_grade = fields.Selection([
        ('premium', 'Premium'), ('standard', 'Standard'), ('fail', 'Rejected')
    ], string="Precision Grade", default='standard')