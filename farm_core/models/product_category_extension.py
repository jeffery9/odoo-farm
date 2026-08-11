# -*- coding: utf-8 -*-
from odoo import models, fields

class ProductCategory(models.Model):
    _inherit = 'product.category'

    matter_enforcement_level = fields.Selection([
        ('guidance', 'Lightweight Guidance / 轻量级指引'),
        ('strict', 'Strict GxP Enforcement / 强合规卡控')
    ], string="Matter Enforcement Level", default="guidance", required=True, help="Risk level for physical matter tracking in this category.")

    consolidation_strategy = fields.Selection([
        ('strict_isolation', 'Strict Isolation (Single-Lot Only)'),
        ('weighted_average', 'Weighted Average (Bulk & Liquid Mixing)'),
        ('multi_lot_package', 'Multi-Lot Pack (Co-existence in Package)')
    ], string="Consolidation Strategy", default='strict_isolation', required=True)

    allow_cross_quality_mix = fields.Boolean(
        string="Allow Cross-Quality Mixing", default=False)
