from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_agricultural_chemical = fields.Boolean("Is Agricultural Chemical")
    is_forbidden = fields.Boolean("Forbidden Substance", help="If True, consuming this in an intervention will taint the resulting crop lot.")
    safety_hold_days = fields.Integer("Pre-Harvest Interval (Days)", help="Number of days required before harvest.")
