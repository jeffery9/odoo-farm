# -*- coding: utf-8 -*-
from odoo import fields, models

class StockMatterTracking(models.Model):
    _inherit = 'stock.matter.tracking'

    livestock_asset_id = fields.Many2one(
        comodel_name='farm.livestock.asset',
        string="Livestock Biological Asset (畜牧生物资产)",
        ondelete='set null',
        index=True
    )
