# -*- coding: utf-8 -*-
from odoo import fields, models

class StockMatterTracking(models.Model):
    _inherit = 'stock.matter.tracking'

    crop_cycle_id = fields.Many2one(
        comodel_name='farm.crop.cycle',
        string="Crop Growth Cycle (作物生长周期)",
        ondelete='set null',
        index=True
    )
