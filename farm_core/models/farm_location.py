from odoo import models, fields, api, _

class FarmLocation(models.Model):
    _inherit = 'stock.location'

    is_land_parcel = fields.Boolean("Is Land Parcel", default=False)
    land_area = fields.Float("Area (sqm/mu)", digits=(16, 2), help="Surface area of the parcel.")
    land_area_uom_id = fields.Many2one('uom.uom', string="Area Unit", domain="[('category_id.measure_type', '=', 'area')]")
    
    # GIS Core Fields [US-01-03]
    gps_lat = fields.Float("Latitude", digits=(10, 7))
    gps_lng = fields.Float("Longitude", digits=(10, 7))
    gps_coordinates = fields.Text("GPS Coordinates (GeoJSON)", help="GeoJSON format for boundaries/polygons.")
    
    gis_map_url = fields.Char("Map Link", compute='_compute_gis_map_url')
    
    soil_type = fields.Selection([
        ('clay', 'Clay'),
        ('silt', 'Silt'),
        ('sand', 'Sand'),
        ('loam', 'Loam'),
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

    # 针对水产 [US-01-02]
    water_depth = fields.Float("Water Depth (m)")
    water_depth_dm = fields.Float("Water Depth (dm)", compute='_compute_water_depth_dm', inverse='_inverse_water_depth_dm')

    # 容器管理 [酿酒/酿造]
    is_vessel = fields.Boolean("Is Vessel/Tank", default=False)
    vessel_capacity = fields.Float("Vessel Capacity (L)")
    vessel_material = fields.Selection([
        ('stainless', 'Stainless Steel'),
        ('oak', 'Oak Barrel'),
        ('ceramic', 'Ceramic')
    ], string="Material")
    
    # 多农场协同 [US-17-09]
    # 使用 Odoo 原生 Company 机制，但在 UI 上强化 Farm 概念
    farm_id = fields.Many2one('res.company', string="Belonging Farm", default=lambda self: self.env.company)

    @api.depends('water_depth')
    def _compute_water_depth_dm(self):
        for loc in self:
            loc.water_depth_dm = loc.water_depth * 10.0

    def _inverse_water_depth_dm(self):
        for loc in self:
            loc.water_depth = loc.water_depth_dm / 10.0

    # 动态属性 [US-01-02]
    location_properties_definition = fields.PropertiesDefinition('Location Properties Definition')
    location_properties = fields.Properties(
        'Properties',
        definition='location_properties_definition'
    )

    # US-02-03: Accumulated Nutrient Balance
    total_n_input = fields.Float("Accumulated Nitrogen (kg)", compute='_compute_nutrient_balance')
    total_p_input = fields.Float("Accumulated Phosphorus (kg)", compute='_compute_nutrient_balance')
    total_k_input = fields.Float("Accumulated Potassium (kg)", compute='_compute_nutrient_balance')

    # 养分目标与盈亏
    target_n_per_mu = fields.Float("Target N (kg/mu)", help="Optimal nitrogen for the current crop")
    target_p_per_mu = fields.Float("Target P (kg/mu)")
    target_k_per_mu = fields.Float("Target K (kg/mu)")

    n_balance_status = fields.Float("N Surplus/Deficit", compute='_compute_balance_status')
    p_balance_status = fields.Float("P Surplus/Deficit", compute='_compute_balance_status')
    k_balance_status = fields.Float("K Surplus/Deficit", compute='_compute_balance_status')

    def _compute_balance_status(self):
        for loc in self:
            area = loc.land_area or 1.0 # 避免除以0
            loc.n_balance_status = loc.total_n_input - (loc.target_n_per_mu * area)
            loc.p_balance_status = loc.total_p_input - (loc.target_p_per_mu * area)
            loc.k_balance_status = loc.total_k_input - (loc.target_k_per_mu * area)

    def _compute_nutrient_balance(self):
        """ 汇总该地块所有任务的养分投入 """
        for loc in self:
            # 找到所有关联该地块的生产任务
            tasks = self.env['project.task'].search([('land_parcel_id', '=', loc.id)])
            interventions = self.env['mrp.production'].search([('agri_task_id', 'in', tasks.ids), ('state', '=', 'done')])
            
            loc.total_n_input = sum(interventions.mapped('pure_n_qty'))
            loc.total_p_input = sum(interventions.mapped('pure_p_qty'))
            loc.total_k_input = sum(interventions.mapped('pure_k_qty'))
