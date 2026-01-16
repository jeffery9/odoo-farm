from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class QualityBasedPricing(models.Model):
    """
    质量挂钩的采购分级定价 [US-09-11]
    """
    _name = 'quality.based.pricing'
    _description = 'Quality-Based Pricing Rules'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Pricing Rule Name', required=True)
    product_category_id = fields.Many2one('product.category', string='Product Category')
    quality_attribute = fields.Char('Quality Attribute', required=True,
                                  help='e.g., sugar_content, protein_content, fat_content')
    base_price = fields.Float('Base Price', required=True)
    min_value = fields.Float('Minimum Value for Premium')
    max_value = fields.Float('Maximum Value for Premium')
    premium_rate = fields.Float('Premium Rate (%)',
                               help='Percentage to add to base price for each unit above threshold')
    discount_rate = fields.Float('Discount Rate (%)',
                                help='Percentage to subtract from base price for each unit below threshold')
    active = fields.Boolean('Active', default=True)

    def calculate_adjusted_price(self, quality_value, base_unit_price):
        """Calculate adjusted price based on quality attribute value"""
        if not self.active or quality_value is None:
            return base_unit_price

        if quality_value >= self.max_value:
            # Apply premium - for every unit above max_value, add premium
            excess = quality_value - self.max_value
            premium_factor = 1 + (excess * self.premium_rate / 100)
            return base_unit_price * premium_factor
        elif quality_value <= self.min_value:
            # Apply discount - for every unit below min_value, subtract discount
            deficit = self.min_value - quality_value
            discount_factor = 1 - (deficit * self.discount_rate / 100)
            # Ensure price doesn't go below zero
            return max(base_unit_price * discount_factor, 0)
        else:
            # Within normal range
            return base_unit_price