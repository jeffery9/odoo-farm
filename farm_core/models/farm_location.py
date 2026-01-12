from odoo import models, fields, api, _

class FarmLocation(models.Model):
    _inherit = 'stock.location'

    is_land_parcel = fields.Boolean("Is Land Parcel", default=False)
    land_area = fields.Float("Area (sqm/mu)", digits=(16, 2), help="Surface area of the parcel.")
    land_area_uom_id = fields.Many2one('uom.uom', string="Area Unit", domain="[('category_id.measure_type', '=', 'area')]")
    
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

    soil_analysis_ids = fields.One2many('farm.soil.analysis', 'location_id', string="Soil Analyses")
    latest_ph = fields.Float("Latest pH", compute='_compute_latest_soil_stats', store=True)
    latest_organic_matter = fields.Float("Organic Matter (%)", compute='_compute_latest_soil_stats', store=True)

    @api.depends('soil_analysis_ids.state', 'soil_analysis_ids.ph_level')
    def _compute_latest_soil_stats(self):
        for loc in self:
            latest = self.env['farm.soil.analysis'].search([
                ('location_id', '=', loc.id),
                ('state', '=', 'done')
            ], order='analysis_date desc', limit=1)
            loc.latest_ph = latest.ph_level if latest else 0.0
            loc.latest_organic_matter = latest.organic_matter if latest else 0.0

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
    
    # 多农场协同 [US-63]
    # 使用 Odoo 原生 Company 机制，但在 UI 上强化 Farm 概念
    farm_id = fields.Many2one('res.company', string="Belonging Farm", default=lambda self: self.env.company)

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
