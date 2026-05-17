from odoo import models, fields, api, _
from .gis_utils import GISCoordinateUtils
from .common_fields import CommonAgriculturalFields
import json
import logging

_logger = logging.getLogger(__name__)


class FarmLocation(models.Model):
    """
    Core Land & Location Management - fundamental agricultural location properties.
    Level 4: Agri-Farm Semantic Refactoring [US-014-2026]
    Architecture: Mixin + ISL Implementation.
    
    US-001-03: Land Parcel Management
    US-TECH-04-01: GIS Core Fields
    US-062-01: Terroir Profiling
    US-063-01: Vertical Farming / High-density Storage
    """
    _name = 'farm.location'
    _description = 'Farm Location & Land Parcel'
    
    # [Semantic Refactoring] Inherit domain standards from agri.location
    _inherits = {'agri.location': 'agri_location_id'}
    
    _inherit = [
        'mail.thread', 
        'mail.activity.mixin', 
        'stock.location', 
        'farm.core.gis.utils',
        'agri.industry.planting.mixin', # [Mixin Injection] Sector Specific Capability
        'agri.certification.status.mixin' # [NEW] Level 2: Compliance DNA
    ]

    # Link to the Domain Model
    agri_location_id = fields.Many2one('agri.location', required=True, ondelete="cascade", 
                                      string="Agri Domain Entity", help="The underlying physical entity in the Agri domain.")

    # Extend stock.location with essential agricultural properties only
    is_land_parcel = fields.Boolean("Is Land Parcel", default=False)

    # Basic land nature classification
    land_nature = fields.Selection([
        ('basic_farmland', 'Permanent Basic Farmland (永久基本农田)'),
        ('general_farmland', 'General Farmland (一般耕地)'),
        ('garden_land', 'Garden Land (园地)'),
        ('forest_land', 'Forest Land (林地)'),
        ('other_agri_land', 'Other Agricultural Land (其他农用地)'),
        ('construction_land', 'Construction Land (建设用地)'),
    ], string="Land Nature", help="Classification based on national land use guidelines.")

    land_area = fields.Float("Area (sqm/mu)", digits=(16, 2), help="Surface area of the parcel.")
    land_area_uom_id = fields.Many2one('uom.uom', string="Area Unit")

    # Core GIS Fields [US-001-03, US-TECH-04-01]
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

    # Basic soil classification
    soil_type = fields.Selection([
        ('clay', 'Clay'),
        ('silt', 'Silt'),
        ('sand', 'Sand'),
        ('loam', 'Loam'),
    ], string="Soil Type")

    # Basic terroir attributes [US-062-01]
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

    # US-063-01: Vertical Farming / High-density Storage (立体库位管理)
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

    # Basic aquaculture fields [US-001-02]
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

    # Multi-farm collaboration [US-040-09] - Using Odoo's native Company mechanism
    farm_id = fields.Many2one('res.company', string="Belonging Farm", default=lambda self: self.env.company)

    @api.depends('water_depth')
    def _compute_water_depth_dm(self):
        for loc in self:
            loc.water_depth_dm = loc.water_depth * 10.0

    def _inverse_water_depth_dm(self):
        for loc in self:
            loc.water_depth = loc.water_depth_dm / 10.0

    # Dynamic attributes [US-001-02]
    location_properties_definition = fields.PropertiesDefinition('Location Properties Definition')
    location_properties = fields.Properties(
        'Properties',
        definition='location_properties_definition'
    )