from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class FarmGeofence(models.Model):
    """
    US-23-01: 虚拟围栏规划与告警策略
    """
    _name = 'farm.geofence'
    _description = 'Agricultural Geofence'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Fence Name", required=True)
    fence_type = fields.Selection([
        ('grazing', 'Grazing Area'),
        ('no_fly', 'No-fly Zone'),
        ('quarantine', 'Quarantine Zone'),
        ('buffer', 'Buffer Zone')
    ], string="Type", default='grazing', required=True)

    # 坐标定义: lon,lat;lon,lat...
    coordinates = fields.Text("Polygon Coordinates", required=True, 
                             help="GPS coordinates in 'lon,lat;lon,lat' format. Must be closed (first and last same).")
    
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    # 关联资产类型
    target_category = fields.Selection([
        ('livestock', 'Livestock'),
        ('drone', 'Drones'),
        ('machinery', 'Machinery')
    ], string="Target Assets", default='livestock')

    # 告警级别
    alarm_level = fields.Selection([
        ('info', 'Log Only'),
        ('warning', 'Notification'),
        ('critical', 'Critical (Lock/Shutdown)')
    ], string="Alarm Level", default='warning')

    def is_point_inside(self, lon, lat):
        """ 
        核心算法：射线法判定点是否在多边形内 [US-23-02]
        """
        self.ensure_one()
        if not self.coordinates:
            return False
            
        try:
            points = [tuple(map(float, p.split(','))) for p in self.coordinates.split(';') if ',' in p]
        except:
            return False

        n = len(points)
        inside = False
        p1x, p1y = points[0]
        for i in range(n + 1):
            p2x, p2y = points[i % n]
            if lat > min(p1y, p2y):
                if lat <= max(p1y, p2y):
                    if lon <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (lat - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or lon <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def action_audit_lot_compliance(self, lot_id):
        """ 
        审计特定批次在过去一段时间内的地理合规性。
        用于生成“走地鸡”或“有机放牧”证明。
        """
        self.ensure_one()
        lot = self.env['stock.lot'].browse(lot_id)
        # 获取该批次关联的所有设备遥测记录
        telemetries = self.env['farm.telemetry'].search([
            ('drone_id.business_ref', '=', f"stock.lot,{lot.id}"),
            ('gps_lat', '!=', 0),
            ('gps_lng', '!=', 0)
        ])
        
        total = len(telemetries)
        if total == 0:
            return {"status": "no_data", "rate": 100.0}
            
        compliant_count = 0
        for t in telemetries:
            if self.is_point_inside(t.gps_lng, t.gps_lat):
                compliant_count += 1
        
        compliance_rate = (compliant_count / total) * 100.0
        return {
            "status": "success" if compliance_rate > 99.0 else "failed",
            "rate": compliance_rate,
            "total_points": total,
            "oob_points": total - compliant_count
        }
