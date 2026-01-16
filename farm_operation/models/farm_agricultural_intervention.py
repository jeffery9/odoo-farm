from odoo import models, fields


class FarmAgriculturalIntervention(models.Model):
    """
    Concrete ISL model for Agricultural Interventions using _inherits.
    This model inherits from the base mrp.production model and includes the shared logic from the mixin.
    """
    _name = 'farm.agricultural.intervention'
    _description = 'Agricultural Intervention (ISL Layer)'
    _inherits = {'mrp.production': 'production_id'}  # Inherit from base Odoo model
    _inherit = ['farm.agricultural.intervention.mixin']  # Include shared logic

    # Link to the base model (this field is required for _inherits)
    production_id = fields.Many2one(
        'mrp.production',
        string="Base Production Order",
        required=True,
        ondelete="cascade"
    )

    # Add any agricultural-specific fields that extend beyond the base model
    # The mixin already provides most agricultural-specific functionality