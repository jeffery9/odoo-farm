# -*- coding: utf-8 -*-
from odoo import models, fields

class ProductCategory(models.Model):
    _inherit = 'product.category'

    matter_enforcement_level = fields.Selection([
        ('guidance', 'Guidance'),
        ('strict', 'Strict')
    ], string="Matter Enforcement Level", default='guidance')

    consolidation_strategy = fields.Selection([
        ('strict_isolation', 'Strict Isolation (Single-Lot Only)'),
        ('weighted_average', 'Weighted Average (Bulk & Liquid Mixing)'),
        ('multi_lot_package', 'Multi-Lot Pack (Co-existence in Package)')
    ], string="Consolidation Strategy", default='strict_isolation', required=True)

    allow_cross_quality_mix = fields.Boolean(
        string="Allow Cross-Quality Mixing", default=False)
