from odoo import models, fields, api, _
from .gis_utils import GISCoordinateUtils
from .common_fields import CommonAgriculturalFields
import json
import logging

_logger = logging.getLogger(__name__)


class FarmLocation(models.Model):
    """
    Land & Location Management - replacing the functionality from farm_location.py
    US-01-03: Land Parcel Management
    US-TECH-04-01: GIS Core Fields
    US-32-01: Terroir Profiling
    US-33-01: Vertical Farming / High-density Storage
    US-02-03: Accumulated Nutrient Balance
    """
    _name = 'farm.location'
    _description = 'Farm Location & Land Parcel'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'stock.location', 'farm.core.gis.utils']

    # Extend stock.location with agricultural properties
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

    @api.model
    def calculate_area(self):
        """Calculate area using GIS utilities from GeoJSON boundary"""
        for location in self:
            if location.boundary_geojson:
                lat_avg = location.gps_lat if location.gps_lat else None
                area_ha = self.calculate_area_from_geojson(location.boundary_geojson, lat_avg)
                location.calculated_area_ha = area_ha
                # Sync with generic land_area field
                location.land_area = area_ha * 10000.0  # Ha to sqm

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

    # US-33-01: Vertical Farming / High-density Storage (立体库位管理)
    is_vertical_location = fields.Boolean("Is Vertical / Shelf", default=False)
    shelf_id = fields.Char("Shelf ID")
    shelf_level = fields.Integer("Level / Row")
    shelf_slot = fields.Char("Slot / Position")

    @api.depends('gps_lat', 'gps_lng')
    def _compute_gis_map_url(self):
        for loc in self:
            if loc.gps_lat and loc.gps_lng:
                # Generate OpenStreetMap link
                loc.gis_map_url = f"https://www.openstreetmap.org/?mlat={loc.gps_lat}&mlon={loc.gps_lng}#map=17/{loc.gps_lat}/{loc.gps_lng}"
            else:
                loc.gis_map_url = False

    # Soil analysis integration
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

    # Aquaculture specific fields [US-01-02]
    water_depth = fields.Float("Water Depth (m)")
    water_depth_dm = fields.Float("Water Depth (dm)", compute='_compute_water_depth_dm', inverse='_inverse_water_depth_dm')

    # Container management
    is_vessel = fields.Boolean("Is Vessel/Tank", default=False)
    vessel_capacity = fields.Float("Vessel Capacity (L)")
    vessel_material = fields.Selection([
        ('stainless', 'Stainless Steel'),
        ('oak', 'Oak Barrel'),
        ('ceramic', 'Ceramic')
    ], string="Material")

    # Multi-farm collaboration [US-17-09] - Using Odoo's native Company mechanism
    farm_id = fields.Many2one('res.company', string="Belonging Farm", default=lambda self: self.env.company)

    @api.depends('water_depth')
    def _compute_water_depth_dm(self):
        for loc in self:
            loc.water_depth_dm = loc.water_depth * 10.0

    def _inverse_water_depth_dm(self):
        for loc in self:
            loc.water_depth = loc.water_depth_dm / 10.0

    # Dynamic attributes [US-01-02]
    location_properties_definition = fields.PropertiesDefinition('Location Properties Definition')
    location_properties = fields.Properties(
        'Properties',
        definition='location_properties_definition'
    )

    # US-02-03: Accumulated Nutrient Balance
    total_n_input = fields.Float("Accumulated Nitrogen (kg)", compute='_compute_nutrient_balance')
    total_p_input = fields.Float("Accumulated Phosphorus (kg)", compute='_compute_nutrient_balance')
    total_k_input = fields.Float("Accumulated Potassium (kg)", compute='_compute_nutrient_balance')

    # Nutrient targets and balances
    target_n_per_mu = fields.Float("Target N (kg/mu)", help="Optimal nitrogen for the current crop")
    target_p_per_mu = fields.Float("Target P (kg/mu)")
    target_k_per_mu = fields.Float("Target K (kg/mu)")

    n_balance_status = fields.Float("N Surplus/Deficit", compute='_compute_balance_status')
    p_balance_status = fields.Float("P Surplus/Deficit", compute='_compute_balance_status')
    k_balance_status = fields.Float("K Surplus/Deficit", compute='_compute_balance_status')

    def _compute_balance_status(self):
        for loc in self:
            area = loc.land_area or 1.0  # Avoid division by 0
            loc.n_balance_status = loc.total_n_input - (loc.target_n_per_mu * area)
            loc.p_balance_status = loc.total_p_input - (loc.target_p_per_mu * area)
            loc.k_balance_status = loc.total_k_input - (loc.target_k_per_mu * area)

    def _compute_nutrient_balance(self):
        """Sum all nutrient inputs to this location from tasks and other sources"""
        for loc in self:
            # 1. Production task inputs
            tasks = self.env['project.task'].search([('land_parcel_id', '=', loc.id)])
            interventions = self.env['mrp.production'].search([('agri_task_id', 'in', tasks.ids), ('state', '=', 'done')])

            total_n = sum(interventions.mapped('pure_n_qty'))
            total_p = sum(interventions.mapped('pure_p_qty'))
            total_k = sum(interventions.mapped('pure_k_qty'))

            # 2. Manure application [US-27-01] - if the model exists
            manure_model = self.env['farm.manure.batch']
            if hasattr(manure_model, 'search'):
                manure_batches = manure_model.search([
                    ('destination_location_id', '=', loc.id),
                    ('disposal_method', '=', 'direct_field_use')
                ])
                total_n += sum(manure_batches.mapped('pure_n_qty'))
                total_p += sum(manure_batches.mapped('pure_p_qty'))
                total_k += sum(manure_batches.mapped('pure_k_qty'))

            loc.total_n_input = total_n
            loc.total_p_input = total_p
            loc.total_k_input = total_k


class SoilAnalysis(models.Model):
    """
    Soil Analysis Management - replacing the functionality from soil_analysis.py
    """
    _name = 'farm.soil.analysis'
    _description = 'Soil Analysis Report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'analysis_date desc'

    name = fields.Char("Report Reference", required=True, default=lambda self: _('New'))
    location_id = fields.Many2one('farm.location', string="Land Parcel", required=True)
    analysis_date = fields.Date("Analysis Date", default=fields.Date.today, required=True)
    laboratory_id = fields.Many2one('res.partner', string="Laboratory", domain=[('is_company', '=', True)])

    # Nutrient indicators
    ph_level = fields.Float("pH Level", digits=(10, 2))
    organic_matter = fields.Float("Organic Matter (%)")
    nitrogen_content = fields.Float("Nitrogen (mg/kg)")
    phosphorus_content = fields.Float("Phosphorus (mg/kg)")
    potassium_content = fields.Float("Potassium (mg/kg)")

    # Trace elements
    magnesium = fields.Float("Magnesium (mg/kg)")
    calcium = fields.Float("Calcium (mg/kg)")

    # Recommendations
    recommendation = fields.Text("Fertilization Recommendations")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Validated'),
        ('cancel', 'Cancelled')
    ], string="Status", default='draft', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.soil.analysis') or _('SOIL')
        return super().create(vals_list)

    def action_validate(self):
        self.write({'state': 'done'})