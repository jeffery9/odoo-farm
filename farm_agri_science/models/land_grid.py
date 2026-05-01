# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import json
import math
import logging

_logger = logging.getLogger(__name__)

class AgriGeospatialGridCell(models.Model):
    """
    Agri Domain Level: Spatial Grid Cell. [US-104-2026]
    The atomic physical unit of agricultural space (typically 11m or 1m resolution).
    Refactored from farm.land.grid.cell with 100% logic retention.
    """
    _name = 'agri.geospatial.grid.cell'
    _description = 'Agricultural Spatial Grid Cell'
    _order = 'row, col'

    location_id = fields.Many2one('farm.location', string="Parent Parcel", required=True, ondelete='cascade')
    name = fields.Char("Grid UID", compute='_compute_name', store=True)
    
    row = fields.Integer("Row Index")
    col = fields.Integer("Column Index")
    
    # GIS Anchor Points
    center_lat = fields.Float("Center Latitude", digits=(10, 7))
    center_lng = fields.Float("Center Longitude", digits=(10, 7))
    
    # Raster Attributes (Domain Physics)
    ndvi_index = fields.Float("NDVI (Satellite Index)", digits=(4, 3))
    soil_ph = fields.Float("Soil pH (Interpolated)")
    soil_moisture = fields.Float("Soil Moisture (%)")
    soil_nutrient_n = fields.Float("Soil Nitrogen (N) Level")
    historical_rue = fields.Float("Historical RUE (g/MJ)", default=1.2, help="Historical Radiation Use Efficiency of this cell")
    lai_index = fields.Float("Leaf Area Index (LAI)", digits=(4, 2), default=1.0)
    water_stress = fields.Float("Water Stress Index", help="Simulated from thermal bands")
    
    # Geometry (GeoJSON)
    cell_geojson = fields.Text("Cell Geometry (Polygon)")

    @api.depends('row', 'col')
    def _compute_name(self):
        for rec in self:
            rec.name = f"{rec.location_id.name}-R{rec.row}C{rec.col}"

class FarmLocation(models.Model):
    _inherit = 'farm.location'

    grid_resolution = fields.Selection([
        ('1', '1x1m (Ultra High)'),
        ('5', '5x5m (Standard Agri)'),
        ('10', '10x10m (Extensive)')
    ], string="Grid Resolution", default='5')

    grid_cell_ids = fields.One2many('agri.geospatial.grid.cell', 'location_id', string="Spatial Grid Cells")
    grid_generated = fields.Boolean("Grid Layout Generated", default=False)

    # --- 100% Original Logic Retention (RESTORED) ---
    def action_generate_precision_grid(self):
        """
        Advanced GIS Algorithm: Generates precision inner grids based on parcel boundary.
        1. Extract GeoJSON boundary.
        2. Calculate Bounding Box.
        3. Perform Ray Casting to determine points within the polygon.
        """
        self.ensure_one()
        if not self.boundary_geojson:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {'title': _('Missing Geometry'), 'message': _('Please define the parcel boundary first.'), 'type': 'danger'}
            }

        # Clear existing grid
        self.grid_cell_ids.unlink()
        
        try:
            boundary = json.loads(self.boundary_geojson)
            coords = boundary['coordinates'][0] if boundary['type'] == 'Polygon' else boundary['geometry']['coordinates'][0]
            
            # Calculate Bounding Box
            lons = [c[0] for c in coords]
            lats = [c[1] for c in coords]
            min_lon, max_lon = min(lons), max(lons)
            min_lat, max_lat = min(lats), max(lats)

            # Resolution conversion (meters to degrees)
            res_m = float(self.grid_resolution)
            lat_avg = (min_lat + max_lat) / 2
            step_lat = res_m / 111132.0
            step_lon = res_m / (111132.0 * math.cos(math.radians(lat_avg)))

            grid_data = []
            row = 0
            curr_lat = min_lat + step_lat / 2
            
            while curr_lat < max_lat:
                col = 0
                curr_lon = min_lon + step_lon / 2
                while curr_lon < max_lon:
                    # GIS Logic: Check if point is in polygon
                    coord_str = ";".join([f"{c[0]},{c[1]}" for c in coords])
                    if hasattr(self, 'is_point_in_polygon') and self.is_point_in_polygon(coord_str, curr_lon, curr_lat):
                        grid_data.append({
                            'location_id': self.id,
                            'row': row,
                            'col': col,
                            'center_lat': curr_lat,
                            'center_lng': curr_lon,
                            'cell_geojson': json.dumps({
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
                    col += 1
                curr_lat += step_lat
                row += 1

            self.env['agri.geospatial.grid.cell'].create(grid_data)
            self.grid_generated = True
            
        except Exception as e:
            _logger.error("GIS Grid Generation Failed: %s", str(e))

    def action_interpolate_soil_data(self):
        """
        GIS Business Logic: Spatial Interpolation (Simplified IDW).
        Interpolates pH values for all grid cells based on existing soil analysis samples.
        """
        self.ensure_one()
        samples = self.env['agri.soil.analysis'].search([('location_id', '=', self.id), ('state', '=', 'done')])
        if not samples or not self.grid_cell_ids:
            return

        for cell in self.grid_cell_ids:
            total_weight = 0
            weighted_ph = 0
            for s in samples:
                # Mock distance calculation calling GIS utils
                dist = self.calculate_distance(cell.center_lat, cell.center_lng, self.gps_lat, self.gps_lng)
                weight = 1 / (dist**2) if dist > 0 else 100
                weighted_ph += s.ph_level * weight
                total_weight += weight
            
            cell.soil_ph = weighted_ph / total_weight if total_weight > 0 else 7.0

    def action_sync_iot_telemetry(self):
        """
        [US-78-01] IoT Telemetry Mapping.
        Fetches the latest soil-related telemetry and maps to grid cells by nearest GPS.
        """
        self.ensure_one()
        telemetry_logs = self.env['iiot.telemetry'].search([
            ('land_parcel_id', '=', self.id),
            ('sensor_type', 'in', ['soil_moisture', 'ph'])
        ], order='timestamp desc', limit=50)

        if not telemetry_logs or not self.grid_cell_ids:
            return

        for log in telemetry_logs:
            # Find the nearest grid cell
            best_cell = False
            min_dist = float('inf')
            for cell in self.grid_cell_ids:
                dist = math.sqrt((cell.center_lat - log.gps_lat)**2 + (cell.center_lng - log.gps_lng)**2)
                if dist < min_dist:
                    min_dist = dist
                    best_cell = cell
            
            if best_cell:
                if log.sensor_type == 'ph':
                    best_cell.soil_ph = log.value
                elif log.sensor_type == 'soil_moisture':
                    best_cell.soil_moisture = log.value

    # --- End of Original Logic ---