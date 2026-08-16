# -*- coding: utf-8 -*-
from odoo import fields, models

class StockMatterTracking(models.Model):
    _inherit = 'stock.matter.tracking'

    carbon_ledger_id = fields.Many2one(
        comodel_name='agri.carbon.ledger',
        string="Associated Carbon ESG Ledger (关联碳中和资产账本)",
        ondelete='set null',
        index=True
    )
