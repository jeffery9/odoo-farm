# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class StockMatterTrackingLink(models.Model):
    _name = 'stock.matter.tracking.link'
    _description = 'SFC Genealogy Directed Graph Link / Edge (谱系血缘关系边)'
    _order = 'timestamp desc, id desc'

    parent_id = fields.Many2one(
        'stock.matter.tracking',
        string='Parent / Ancestor SFC (源容器)',
        required=True,
        ondelete='cascade',
        index=True
    )
    child_id = fields.Many2one(
        'stock.matter.tracking',
        string='Child / Descendant SFC (目标容器)',
        required=True,
        ondelete='cascade',
        index=True
    )
    transition_type = fields.Selection([
        ('sequential', 'Sequential Flow / 顺序流转'),
        ('split', 'Fission Split / 裂变分流'),
        ('merge', 'Consolidation Merge / 并合混合')
    ], string='Transition Type', required=True, default='sequential', index=True)

    quantity_transferred = fields.Float(
        string='Quantity Transferred (移转数量)',
        default=0.0
    )
    timestamp = fields.Datetime(
        string='Execution Timestamp',
        default=fields.Datetime.now,
        required=True,
        index=True
    )
