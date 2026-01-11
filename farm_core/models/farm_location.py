from odoo import models, fields, api, _

class FarmLocation(models.Model):
    _inherit = 'stock.location'

    is_land_parcel = fields.Boolean("Is Land Parcel", default=False)
    land_area = fields.Float("Area (sqm/mu)", digits=(16, 2), help="Surface area of the parcel.")
    
    # GIS Core Fields [US-03]
    gps_lat = fields.Float("Latitude", digits=(10, 7))
    gps_lng = fields.Float("Longitude", digits=(10, 7))
    gps_coordinates = fields.Text("GPS Coordinates (GeoJSON)", help="GeoJSON format for boundaries/polygons.")
    
    gis_map_url = fields.Char("Map Link", compute='_compute_gis_map_url')
    
    soil_type = fields.Selection([
        ('clay', 'Clay (粘土)'),
        ('silt', 'Silt (粉砂土)'),
        ('sand', 'Sand (沙土)'),
        ('loam', 'Loam (壤土)'),
    ], string="Soil Type")
    
    @api.depends('gps_lat', 'gps_lng')
    def _compute_gis_map_url(self):
        for loc in self:
            if loc.gps_lat and loc.gps_lng:
                # 默认生成 OpenStreetMap 链接
                loc.gis_map_url = f"https://www.openstreetmap.org/?mlat={loc.gps_lat}&mlon={loc.gps_lng}#map=17/{loc.gps_lat}/{loc.gps_lng}"
            else:
                loc.gis_map_url = False

    # 针对水产 [US-02]
    water_depth = fields.Float("Water Depth (m)")
    water_depth_dm = fields.Float("Water Depth (dm)", compute='_compute_water_depth_dm', inverse='_inverse_water_depth_dm')

    # 容器管理 [酿酒/酿造]
    is_vessel = fields.Boolean("Is Vessel/Tank", default=False)
    vessel_capacity = fields.Float("Vessel Capacity (L)")
    vessel_material = fields.Selection([
        ('stainless', 'Stainless Steel (不锈钢)'),
        ('oak', 'Oak Barrel (橡木桶)'),
        ('ceramic', 'Ceramic (陶瓷)')
    ], string="Material")

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
