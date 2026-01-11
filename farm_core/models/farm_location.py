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
    
    # 针对水产 [US-02]
    water_depth = fields.Float("Water Depth (m)")
    water_depth_dm = fields.Float("Water Depth (dm)", compute='_compute_water_depth_dm', inverse='_inverse_water_depth_dm')

    @api.depends('water_depth')
    def _compute_water_depth_dm(self):
        for loc in self:
            loc.water_depth_dm = loc.water_depth * 10.0

    def _inverse_water_depth_dm(self):
        for loc in self:
            loc.water_depth = loc.water_depth_dm / 10.0

    # 动态属性 [US-02]
    location_properties_definition = fields.PropertiesDefinition('Location Properties Definition')
    location_properties = fields.Properties(
        'Properties',
        definition='location_properties_definition'
    )
