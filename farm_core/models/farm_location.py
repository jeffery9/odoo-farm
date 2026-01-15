from odoo import models, fields, api, _

class FarmLocation(models.Model):
    _inherit = 'stock.location'

    is_land_parcel = fields.Boolean("Is Land Parcel", default=False)
    land_nature = fields.Selection([
        ('basic_farmland', 'Permanent Basic Farmland (永久基本农田)'),
        ('general_farmland', 'General Farmland (一般耕地)'),
        ('garden_land', 'Garden Land (园地)'),
        ('forest_land', 'Forest Land (林地)'),
        ('other_agri_land', 'Other Agricultural Land (其他农用地)'),
        ('construction_land', 'Construction Land (建设用地)'),
    ], string="Land Nature", help="Classification based on national land use guidelines.")
    land_area = fields.Float("Area (sqm/mu)", digits=(16, 2), help="Surface area of the parcel.")
    land_area_uom_id = fields.Many2one('uom.uom', string="Area Unit", domain="[('category_id.measure_type', '=', 'area')]")
    
    # GIS Core Fields [US-01-03, US-TECH-04-01]
    gps_lat = fields.Float("Latitude", digits=(10, 7))
    gps_lng = fields.Float("Longitude", digits=(10, 7))
    boundary_geojson = fields.Text("Boundary Coordinates (GeoJSON)", help="GeoJSON Polygon for the land parcel boundary.")
    calculated_area_ha = fields.Float("Calculated Area (Ha)", digits=(16, 4), readonly=True, help="Area calculated from GeoJSON coordinates.")
    
    def action_calculate_area(self):
        """ US-TECH-04-01: Calculate area using Shoelace formula from GeoJSON. """
        import json
        import math

        for loc in self:
            if not loc.boundary_geojson:
                continue
            try:
                data = json.loads(loc.boundary_geojson)
                # Assuming simple Polygon: {"type": "Polygon", "coordinates": [[[lng, lat], ...]]}
                coords = []
                if data.get('type') == 'Polygon':
                    coords = data['coordinates'][0]
                elif data.get('type') == 'Feature' and data['geometry']['type'] == 'Polygon':
                    coords = data['geometry']['coordinates'][0]
                
                if len(coords) < 3:
                    continue

                # Shoelace algorithm for spherical coordinates (simplified to planar for small parcels)
                area = 0.0
                n = len(coords)
                for i in range(n):
                    j = (i + 1) % n
                    # Conversion constant: approx 111.3km per degree. mu/sqm logic.
                    # Simplified planar area in square degrees then converted to Ha
                    area += coords[i][0] * coords[j][1]
                    area -= coords[j][0] * coords[i][1]
                
                area = abs(area) / 2.0
                # Roughly convert sq degrees to Ha (Value varies by latitude, this is a baseline)
                # Correct way involves Haversine or projected CRS. 
                # For this prototype, we'll store the logic placeholder.
                lat_avg = sum(c[1] for c in coords) / n
                meters_per_deg_lat = 111132.0
                meters_per_deg_lng = 111132.0 * math.cos(math.radians(lat_avg))
                
                real_area_sqm = area * meters_per_deg_lat * meters_per_deg_lng
                loc.calculated_area_ha = real_area_sqm / 10000.0
                loc.land_area = real_area_sqm # Sync with generic field
            except Exception as e:
                _logger.error("Area calculation failed for %s: %s", loc.name, str(e))

    gis_map_url = fields.Char("Map Link", compute='_compute_gis_map_url')
    
    soil_type = fields.Selection([
        ('clay', 'Clay'),
        ('silt', 'Silt'),
        ('sand', 'Sand'),
        ('loam', 'Loam'),
    ], string="Soil Type")
    
    # US-32-01: Terroir Profiling (产地风土数字化)
    slope = fields.Float("Slope Gradient (%)", help="Slope of the land parcel.")
    aspect = fields.Selection([
        ('n', 'North'), ('ne', 'North-East'), ('e', 'East'), ('se', 'South-East'),
        ('s', 'South'), ('sw', 'South-West'), ('w', 'West'), ('nw', 'North-West')
    ], string="Aspect / Orientation")
    water_source = fields.Selection([
        ('river', 'River/Stream'),
        ('well', 'Groundwater Well'),
        ('reservoir', 'Reservoir'),
        ('rain', 'Rain-fed')
    ], string="Primary Water Source")
    
    micro_climate_notes = fields.Text("Micro-climate Characteristics", help="Description of local climate factors.")
    soil_mineral_composition = fields.Text("Mineral Composition", help="Key minerals present in the soil.")

    # US-32-01: Terroir Profiling (产地风土数字化)
    slope = fields.Float("Slope Gradient (%)", help="Slope of the land parcel.")
    aspect = fields.Selection([
        ('n', 'North'), ('ne', 'North-East'), ('e', 'East'), ('se', 'South-East'),
        ('s', 'South'), ('sw', 'South-West'), ('w', 'West'), ('nw', 'North-West')
    ], string="Aspect / Orientation")
    water_source = fields.Selection([
        ('river', 'River/Stream'),
        ('well', 'Groundwater Well'),
        ('reservoir', 'Reservoir'),
        ('rain', 'Rain-fed')
    ], string="Primary Water Source")
    
    micro_climate_notes = fields.Text("Micro-climate Characteristics", help="Description of local climate factors.")
    soil_mineral_composition = fields.Text("Mineral Composition", help="Key minerals present in the soil.")

    # US-33-01: Vertical Farming / High-density Storage (立体库位管理)
    is_vertical_location = fields.Boolean("Is Vertical / Shelf", default=False)
    shelf_id = fields.Char("Shelf ID")
    shelf_level = fields.Integer("Level / Row")
    shelf_slot = fields.Char("Slot / Position")

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

    # 容器管理 [酿造]
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
        """ 汇总该地块所有任务的养分投入，并包含粪污还田贡献 [US-27-01] """
        for loc in self:
            # 1. 生产任务投入
            tasks = self.env['project.task'].search([('land_parcel_id', '=', loc.id)])
            interventions = self.env['mrp.production'].search([('agri_task_id', 'in', tasks.ids), ('state', '=', 'done')])
            
            total_n = sum(interventions.mapped('pure_n_qty'))
            total_p = sum(interventions.mapped('pure_p_qty'))
            total_k = sum(interventions.mapped('pure_k_qty'))

            # 2. 粪污还田贡献 [US-27-01]
            if hasattr(self.env['farm.manure.batch'], 'search'):
                manure_batches = self.env['farm.manure.batch'].search([
                    ('destination_location_id', '=', loc.id),
                    ('disposal_method', '=', 'direct_field_use')
                ])
                total_n += sum(manure_batches.mapped('pure_n_qty'))
                total_p += sum(manure_batches.mapped('pure_p_qty'))
                total_k += sum(manure_batches.mapped('pure_k_qty'))

            loc.total_n_input = total_n
            loc.total_p_input = total_p
            loc.total_k_input = total_k
