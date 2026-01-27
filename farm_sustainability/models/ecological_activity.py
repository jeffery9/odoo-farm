from odoo import models, fields, api

class FarmEcologicalActivity(models.Model):
    _name = 'farm.ecological.activity'
    _description = 'Ecological Maintenance Activity'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Activity Name", required=True) # e.g., Buffer zone weeding, Hedge planting
    date = fields.Date("Date", default=fields.Date.today)
    location_id = fields.Many2one('farm.location', string="Land Parcel/Zone", domain=[('is_land_parcel', '=', True)])
    description = fields.Text("Description")
    impact_category = fields.Selection([
        ('biodiversity', 'Biodiversity'),
        ('soil_health', 'Soil Health'),
        ('water_protection', 'Water Protection')
    ], string="Impact Category", required=True)