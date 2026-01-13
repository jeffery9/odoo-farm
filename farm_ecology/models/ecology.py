from odoo import models, fields, api, _

class FarmBiodiversityIndicator(models.Model):
    _name = 'farm.biodiversity.indicator'
    _description = 'Biodiversity Observation Log'
    _order = 'date desc'

    date = fields.Date("Observation Date", default=fields.Date.today)
    location_id = fields.Many2one('stock.location', string="Location", domain=[('is_land_parcel', '=', True)])
    
    indicator_type = fields.Selection([
        ('insect', 'Insects/Pollinators'),
        ('bird', 'Birds'),
        ('plant', 'Wild Vegetation'),
        ('soil_life', 'Soil Life')
    ], required=True)
    
    species_name = fields.Char("Species Name")
    count_observed = fields.Integer("Count/Abundance")
    
    photo = fields.Binary("Photo Evidence")
    notes = fields.Text("Notes")

class FarmEcologicalZone(models.Model):
    _name = 'farm.ecological.zone'
    _description = 'Ecological Infrastructure (Non-productive)'

    name = fields.Char("Zone Name", required=True) # e.g. North Hedge, Buffer Strip
    zone_type = fields.Selection([
        ('hedge', 'Hedge'),
        ('buffer', 'Buffer Strip'),
        ('pond', 'Ecological Pond'),
        ('forest', 'Forest Patch')
    ], required=True)
    
    area = fields.Float("Area (sqm)")
    location_id = fields.Many2one('stock.location', string="Associated Parcel")
