from odoo import models, fields, api

class CarbonAsset(models.Model):
    """ US-30-02: Carbon Sequestration Assets (e.g., Orchards, Forests) """
    _name = 'farm.carbon.asset'
    _description = 'Carbon Sequestration Asset'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Asset Name", required=True)
    location_id = fields.Many2one('farm.location', string="Location/Parcel", domain=[('is_land_parcel', '=', True)])
    asset_type = fields.Selection([
        ('orchard', 'Orchard'),
        ('forest', 'Forest'),
        ('pasture', 'Permanent Pasture'),
        ('tillage', 'Conservation Tillage')
    ], string="Type", required=True)

    initial_carbon_stock = fields.Float("Initial Carbon Stock (t CO2e)")
    annual_sequestration_rate = fields.Float("Annual Sequestration Rate (t CO2e / mu / year)")

    current_carbon_value = fields.Float("Current Carbon Balance (t CO2e)", compute='_compute_carbon_balance')

    def _compute_carbon_balance(self):
        for asset in self:
            # Simplified calculation based on age
            asset.current_carbon_value = asset.initial_carbon_stock + (asset.annual_sequestration_rate * (asset.location_id.land_area or 0.0))