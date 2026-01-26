from odoo import fields, models, api, _

class FarmGrowthCurve(models.Model):
    """
    Growth curve management for agricultural products
    """
    _name = 'farm.growth.curve'
    _description = 'Agricultural Growth Curve'
    _order = 'age_days'

    product_id = fields.Many2one('product.template', string="Variety", ondelete='cascade')
    age_days = fields.Integer("Age (Days)", required=True)
    target_weight = fields.Float("Target Weight (kg)", required=True)
    daily_feed_rate = fields.Float("Feeding Rate (%)", help="Feed qty as % of body weight")

    def get_expected_weight(self, product, age_days):
        """Get expected weight based on age"""
        curve = self.search([('product_id', '=', product.id), ('age_days', '<=', age_days)], order='age_days DESC', limit=1)
        return curve.target_weight if curve else 0.0