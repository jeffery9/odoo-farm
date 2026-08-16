# -*- coding: utf-8 -*-
from odoo import fields, models

class StockMatterTracking(models.Model):
    _inherit = 'stock.matter.tracking'

    aquaculture_asset_id = fields.Many2one(
        comodel_name='agri.isl.lot.aquaculture',
        string="Aquaculture Asset Batch (水产养殖资产批次)",
        ondelete='set null',
        index=True
    )

    lss_unit_id = fields.Many2one(
        comodel_name='farm.aquaculture.lss',
        string="Life Support System (生命支持系统设备)",
        ondelete='set null',
        index=True
    )
