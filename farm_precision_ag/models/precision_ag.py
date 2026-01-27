from odoo import models, fields, api, _
import json
import math

class FarmLocation(models.Model):
    _inherit = 'farm.location'

    grid_ids = fields.One2many('farm.location.grid', 'location_id', string="Grid Cells")
    grid_count = fields.Integer("Grid Count", compute='_compute_grid_count')

    @api.depends('grid_ids')
    def _compute_grid_count(self):
        for loc in self:
            loc.grid_count = len(loc.grid_ids)

    def action_generate_grid(self):
        """
        US-46-01: Spatial Grid Engine
        Generates 10x10m (approx) grid cells within the location boundary
        """
        self.ensure_one()
        if not self.boundary_geojson:
            return

        # Clear existing grid
        self.grid_ids.unlink()

        try:
            data = json.loads(self.boundary_geojson)
            coords = []
            if data.get('type') == 'Polygon':
                coords = data['coordinates'][0]
            elif data.get('type') == 'Feature' and data['geometry']['type'] == 'Polygon':
                coords = data['geometry']['coordinates'][0]

            if not coords:
                return

            lons = [c[0] for c in coords]
            lats = [c[1] for c in coords]
            min_lon, max_lon = min(lons), max(lons)
            min_lat, max_lat = min(lats), max(lats)

            # 10m in degrees (approx)
            # 1 deg lat ~ 111,132m
            # 1 deg lng ~ 111,132m * cos(lat)
            lat_avg = sum(lats) / len(lats)
            step_lat = 10.0 / 111132.0
            step_lon = 10.0 / (111132.0 * math.cos(math.radians(lat_avg)))

            grid_vals = []
            count = 0
            curr_lat = min_lat + step_lat / 2
            while curr_lat < max_lat:
                curr_lon = min_lon + step_lon / 2
                while curr_lon < max_lon:
                    # Use utility from farm_core
                    if self.is_point_in_polygon(self.boundary_geojson, curr_lon, curr_lat):
                        count += 1
                        grid_vals.append({
                            'location_id': self.id,
                            'name': f"G-{count:04d}",
                            'center_lat': curr_lat,
                            'center_lng': curr_lon,
                            'boundary_geojson': json.dumps({
                                'type': 'Polygon',
                                'coordinates': [[
                                    [curr_lon - step_lon/2, curr_lat - step_lat/2],
                                    [curr_lon + step_lon/2, curr_lat - step_lat/2],
                                    [curr_lon + step_lon/2, curr_lat + step_lat/2],
                                    [curr_lon - step_lon/2, curr_lat + step_lat/2],
                                    [curr_lon - step_lon/2, curr_lat - step_lat/2]
                                ]]
                            })
                        })
                    curr_lon += step_lon
                curr_lat += step_lat

            self.env['farm.location.grid'].create(grid_vals)

        except Exception as e:
            _logger = self.env['logging.logger']._get_logger(__name__) if hasattr(self.env['logging.logger'], '_get_logger') else None
            if _logger:
                _logger.error("Grid generation failed: %s", str(e))

    def action_fetch_ndvi(self):
        """
        US-46-02: 卫星 NDVI 栅格自动映射 (Remote Sensing Mapping)
        Simulates fetching NDVI data from a satellite API (e.g. Sentinel-2)
        and mapping it to the spatial grid cells.
        """
        self.ensure_one()
        import random
        for grid in self.grid_ids:
            # Simulate NDVI values between 0.3 and 0.8
            grid.ndvi = random.uniform(0.3, 0.8)


class FarmLocationGrid(models.Model):
    _name = 'farm.location.grid'
    _description = 'Farm Location Grid Cell'

    location_id = fields.Many2one('farm.location', string="Land Parcel", ondelete='cascade')
    name = fields.Char("Cell ID", required=True)
    center_lat = fields.Float("Center Latitude", digits=(10, 7))
    center_lng = fields.Float("Center Longitude", digits=(10, 7))
    boundary_geojson = fields.Text("Cell Boundary")
    
    # Sensor / Remote Sensing Data (US-46-02)
    ndvi = fields.Float("NDVI Value", digits=(10, 4), default=0.0)
    soil_fertility = fields.Float("Soil Fertility (mg/kg)", digits=(10, 2), default=0.0)

class FarmVraStrategy(models.Model):
    _name = 'farm.vra.strategy'
    _description = 'VRA Decision Strategy'

    name = fields.Char("Strategy Name", required=True)
    type = fields.Selection([
        ('linear', 'Linear Correction'),
        ('step', 'Threshold Stepping')
    ], string="Logic Type", default='linear', required=True)

    # Linear parameters
    target_ndvi = fields.Float("Target NDVI", default=0.7)
    slope = fields.Float("Correction Slope", default=0.5)

    # Step parameters
    step_threshold_low = fields.Float("Low Threshold", default=0.3)
    step_threshold_high = fields.Float("High Threshold", default=0.6)
    step_multiplier_low = fields.Float("Low Multiplier", default=1.3)
    step_multiplier_high = fields.Float("High Multiplier", default=0.8)

class FarmVraPrescription(models.Model):
    _name = 'farm.vra.prescription'
    _description = 'VRA Prescription Map'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Prescription Ref", required=True, default=lambda self: _('New'))
    location_id = fields.Many2one('farm.location', string="Land Parcel", required=True)
    strategy_id = fields.Many2one('farm.vra.strategy', string="Applied Strategy", required=True)
    base_rate = fields.Float("Base Application Rate (kg/mu)", default=10.0)
    
    line_ids = fields.One2many('farm.vra.prescription.line', 'prescription_id', string="Prescription Details")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('calculated', 'Calculated'),
        ('exported', 'Exported'),
        ('cancel', 'Cancelled')
    ], string="Status", default='draft', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.vra.prescription') or _('VRA')
        return super().create(vals_list)

    def action_calculate(self):
        """
        US-46-03: VRA Prescription Engine
        Implements the logic from VRA_PRESCRIPTION_ALGORITHM.md
        """
        self.ensure_one()
        grids = self.location_id.grid_ids
        if not grids:
            return

        # Clear old lines
        self.line_ids.unlink()

        lines = []
        strategy = self.strategy_id
        
        for grid in grids:
            rate = self.base_rate
            if strategy.type == 'linear':
                # Rate = Base * (1 + (Target_NDVI - Current_NDVI) * Slope)
                rate = self.base_rate * (1 + (strategy.target_ndvi - grid.ndvi) * strategy.slope)
            elif strategy.type == 'step':
                if grid.ndvi < strategy.step_threshold_low:
                    rate *= strategy.step_multiplier_low
                elif grid.ndvi > strategy.step_threshold_high:
                    rate *= strategy.step_multiplier_high
            
            # Physical limits (50% - 150% of base)
            rate = max(self.base_rate * 0.5, min(self.base_rate * 1.5, rate))
            
            lines.append({
                'prescription_id': self.id,
                'grid_id': grid.id,
                'target_rate': rate
            })

        self.env['farm.vra.prescription.line'].create(lines)
        self.state = 'calculated'

class FarmVraPrescriptionLine(models.Model):
    _name = 'farm.vra.prescription.line'
    _description = 'VRA Prescription Detail'

    prescription_id = fields.Many2one('farm.vra.prescription', ondelete='cascade')
    grid_id = fields.Many2one('farm.location.grid', string="Grid Cell", required=True)
    target_rate = fields.Float("Target Rate (kg/mu)", digits=(10, 2))
