from odoo import models, fields


class FarmAgriculturalCampaign(models.Model):
    """
    Concrete ISL model for Agricultural Campaigns using _inherits.
    In a proper ISL architecture, this would inherit from an Odoo base model,
    but for the farm_operation module context, we're creating a specialized model.
    """
    _name = 'farm.agricultural.campaign'
    _description = 'Agricultural Campaign (ISL Layer)'
    # Since agricultural.campaign is already a standalone model,
    # we'll make this a separate specialized model for ISL purposes
    _inherit = ['farm.agricultural.campaign.mixin']

    # Add any ISL-specific fields that extend beyond the mixin
    # ISL models typically add industry-specific logic while maintaining compatibility
    isl_campaign_code = fields.Char("ISL Campaign Code", help="ISL-specific campaign identifier")

    # Link to farm_core location for ISL architecture compatibility
    farm_location_id = fields.Many2one(
        'farm.location',
        string="ISL Farm Location",
        help="Link to standardized farm location model"
    )