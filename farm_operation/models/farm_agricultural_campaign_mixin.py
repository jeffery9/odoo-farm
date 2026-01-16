from odoo import models, fields, api
from odoo.exceptions import ValidationError


class FarmAgriculturalCampaignMixin(models.AbstractModel):
    """
    Abstract base model for agricultural campaign functionality.
    This mixin provides shared logic across different agricultural campaign implementations.
    """
    _name = 'farm.agricultural.campaign.mixin'
    _description = 'Farm Agricultural Campaign Shared Logic'

    # Campaign basic information
    name = fields.Char("Season Name", required=True)
    date_start = fields.Date("Start Date")
    date_end = fields.Date("End Date")
    is_active = fields.Boolean("Active", default=True)
    description = fields.Text("Description")

    # GDD (Growing Degree Days) growth model
    base_temperature = fields.Float(
        "Base Temp (℃)",
        default=10.0,
        help="Lower threshold for crop growth."
    )
    target_gdd = fields.Float(
        "Target GDD",
        help="GDD required for harvest."
    )
    accumulated_gdd = fields.Float(
        "Current GDD",
        compute='_compute_gdd',
        store=True
    )
    predicted_harvest_date = fields.Float(
        "Predicted Harvest",
        compute='_compute_gdd',
        store=True
    )

    land_parcel_id = fields.Many2one(
        'stock.location',
        string="Land Parcel",
        domain="[('is_land_parcel', '=', True)]"
    )

    @api.depends('date_start', 'base_temperature', 'target_gdd', 'land_parcel_id')
    def _compute_gdd(self):
        """Compute Growing Degree Days based on weather telemetry"""
        for record in self:
            # This is a simplified implementation - in practice,
            # this would integrate with IoT/weather services
            record.accumulated_gdd = 0.0
            record.predicted_harvest_date = 0.0

    def action_calculate_gdd(self):
        """Calculate GDD based on actual weather data"""
        # Implementation would connect to weather API or IoT sensors
        pass

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        """Validate that campaign dates are logical"""
        for record in self:
            if record.date_start and record.date_end and record.date_start > record.date_end:
                raise ValidationError("Campaign start date must be before end date.")