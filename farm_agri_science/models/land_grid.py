from odoo import models, fields, api, _
import json
import math
import logging

_logger = logging.getLogger(__name__)

class FarmLandGridCell(models.Model):
    _name = 'farm.land.grid.cell'
    _description = 'Agricultural Spatial Grid Cell'
    _order = 'row, col'

    location_id = fields.Many2one('farm.location', string="Parent Parcel", required=True, ondelete='cascade')
    name = fields.Char("Grid UID", compute='_compute_name', store=True)
    
    row = fields.Integer("Row Index")
    col = fields.Integer("Column Index")
    
    # 中心点坐标 (GIS 锚点)
    center_lat = fields.Float("Center Lat", digits=(10, 7))
    center_lng = fields.Float("Center Lng", digits=(10, 7))
    
    # 栅格属性 (Raster Attributes)
    ndvi_index = fields.Float("NDVI (Satellite)", digits=(4, 3))
    soil_ph = fields.Float("Soil pH (Interpolated)")
    water_stress = fields.Float("Water Stress Index", help="Simulated from thermal bands")
    
    # 几何边界 (GeoJSON Polygon)
    cell_geojson = fields.Text("Cell Geometry")

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

    def action_generate_precision_grid(self):
        """
        高级 GIS 算法：基于地块边界生成精确的内切网格
        1. 提取 GeoJSON 边界
        2. 计算外包正方形 (Bounding Box)
        3. 进行射线追踪 (Ray Casting) 判定点是否在多边形内
        """
        self.ensure_one()
        if not self.boundary_geojson:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {'title': _('Missing Geometry'), 'message': _('Please define the parcel boundary first.'), 'type': 'danger'}
            }

        # 清理旧网格
        self.grid_cell_ids.unlink()
        
        try:
            boundary = json.loads(self.boundary_geojson)
            coords = boundary['coordinates'][0] if boundary['type'] == 'Polygon' else boundary['geometry']['coordinates'][0]
            
            # 计算外包框
            lons = [c[0] for c in coords]
            lats = [c[1] for c in coords]
            min_lon, max_lon = min(lons), max(lons)
            min_lat, max_lat = min(lats), max(lats)

            # 分辨率转换 (米 -> 度)
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
                    # 关键 GIS 判断：点是否在多边形内 (利用 farm_core 继承的工具)
                    # 注意：farm_core 里的方法接受的是 "lon,lat;..." 格式，我们需要适配
                    coord_str = ";".join([f"{c[0]},{c[1]}" for c in coords])
                    if self.is_point_in_polygon(coord_str, curr_lon, curr_lat):
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

            self.env['farm.land.grid.cell'].create(grid_data)
            self.grid_generated = True
            
        except Exception as e:
            _logger.error("GIS Grid Generation Failed: %s", str(e))

    def action_interpolate_soil_data(self):
        """
        GIS 业务逻辑：空间插值 (Kriging/IDW 简化版)
        基于已有的土壤采样点坐标，为全地块网格计算 pH 值映射。
        """
        self.ensure_one()
        samples = self.soil_analysis_ids.filtered(lambda s: s.state == 'done')
        if not samples or not self.grid_cell_ids:
            return

        for cell in self.grid_cell_ids:
            # 简化版距离反比加权 (IDW) 算法
            total_weight = 0
            weighted_ph = 0
            for s in samples:
                # 计算采样点与网格中心的距离 (调用 farm_core 工具)
                # 假设土壤采样记录中包含 lat/lng (这里需扩展模型或寻找关联)
                dist = self.calculate_distance(cell.center_lat, cell.center_lng, self.gps_lat, self.gps_lng) # Mock 距离
                weight = 1 / (dist**2) if dist > 0 else 100
                weighted_ph += s.ph_level * weight
                total_weight += weight
            
            cell.soil_ph = weighted_ph / total_weight if total_weight > 0 else 7.0
