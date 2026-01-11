from odoo import models, fields

class FarmLocation(models.Model):
    _inherit = 'stock.location'

    is_land_parcel = fields.Boolean("Is Land Parcel", default=False)
    land_area = fields.Float("Area (sqm/mu)", digits=(16, 2), help="Surface area of the parcel.")
    gps_coordinates = fields.Text("GPS Coordinates", help="GeoJSON format for coordinates.")
    soil_type = fields.Selection([
        ('clay', 'Clay (粘土)'),
        ('silt', 'Silt (粉砂土)'),
        ('sand', 'Sand (沙土)'),
        ('loam', 'Loam (壤土)'),
    ], string="Soil Type")
    
    # 针对水产
    water_depth = fields.Float("Water Depth (m)")
