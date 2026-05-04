# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

class AgriBiologicalGrowthCurve(models.Model):
    """
    Agri Domain Level: Biological Growth Curve. [US-014-2026]
    Universal biological growth standards for the Agri domain.
    Refactored from farm.growth.curve with 100% logic retention.
    """
    _name = 'agri.biological.growth.curve'
    _description = 'Agricultural Biological Growth Curve'
    _order = 'age_days'

    product_id = fields.Many2one('product.template', string="Base Variety", ondelete='cascade', required=True)
    age_days = fields.Integer("Physiological Age (Days)", required=True)
    target_weight = fields.Float("Target Weight (kg)", required=True)
    daily_feed_rate = fields.Float("Daily Feeding Rate (%)", help="Feed quantity as percentage of body weight.")

    # --- 100% Original Logic Retention (RESTORED) ---
    def get_expected_weight(self, product, age_days):
        """Get expected weight based on physiological age via domain registry."""
        curve = self.search([
            ('product_id', '=', product.id), 
            ('age_days', '<=', age_days)
        ], order='age_days DESC', limit=1)
        return curve.target_weight if curve else 0.0
    # --- End of Original Logic ---
