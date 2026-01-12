from odoo import models, fields, api, _

class FarmBiodiversityIndicator(models.Model):
    _name = 'farm.biodiversity.indicator'
    _description = 'Biodiversity Observation Log'
    _order = 'date desc'

    date = fields.Date("Observation Date", default=fields.Date.today)
    location_id = fields.Many2one('stock.location', string="Location", domain=[('is_land_parcel', '=', True)])
    
    indicator_type = fields.Selection([
        ('insect', 'Insects/Pollinators (昆虫)'),
        ('bird', 'Birds (鸟类)'),
        ('plant', 'Wild Vegetation (野生植物)'),
        ('soil_life', 'Soil Life (土壤生物)')
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
        ('hedge', 'Hedge (树篱)'),
        ('buffer', 'Buffer Strip (缓冲带)'),
        ('pond', 'Ecological Pond (生态塘)'),
        ('forest', 'Forest Patch (小微林地)')
    ], required=True)
    
    area = fields.Float("Area (sqm)")
    location_id = fields.Many2one('stock.location', string="Associated Parcel")
