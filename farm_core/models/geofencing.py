# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AgriGeospatialGeofence(models.Model):
    """
    Agri Domain Level: Virtual Geofencing. [US-23-01, US-104-2026]
    Standard for planning and alert strategies across the Agri domain.
    Refactored from farm.geofence with 100% logic retention.
    """
    _name = 'agri.geospatial.geofence'
    _description = 'Agricultural Geofence Standard'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'farm.core.gis.utils']

    name = fields.Char("Fence Name", required=True, translate=True)
    fence_type = fields.Selection([
        ('grazing', 'Grazing Area'),
        ('no_fly', 'No-fly Zone'),
        ('quarantine', 'Quarantine Zone'),
        ('buffer', 'Buffer Zone')
    ], string="Type", default='grazing', required=True)

    # Coordinate definition: lon,lat;lon,lat...
    coordinates = fields.Text("Polygon Coordinates", required=True,
                              help="GPS coordinates in 'lon,lat;lon,lat' format. Must be closed.")

    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    # Associated asset types
    target_category = fields.Selection([
        ('livestock', 'Livestock'),
        ('drone', 'Drones'),
        ('machinery', 'Machinery')
    ], string="Target Assets", default='livestock')

    # Alert levels
    alert_level = fields.Selection([
        ('info', 'Log Only'),
        ('warning', 'Notification'),
        ('critical', 'Critical (Lock/Shutdown)')
    ], string="Alert Level", default='warning')

    # --- 100% Original Logic Retention (RESTORED) ---
    def is_point_inside(self, lon, lat):
        """Core algorithm: Ray casting method to determine if point is inside polygon."""
        self.ensure_one()
        if not self.coordinates: return False
        try:
            points = [tuple(map(float, p.split(','))) for p in self.coordinates.split(';') if ',' in p]
        except (ValueError, AttributeError): return False

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

    def check_compliance_for_asset(self, asset_id, asset_type='livestock'):
        """Check compliance based on historical telemetry."""
        self.ensure_one()
        telemetries = self.env['iiot.telemetry'].search([
            ('asset_id', '=', asset_id),
            ('gps_lat', '!=', 0),
            ('gps_lng', '!=', 0)
        ])
        total = len(telemetries)
        if total == 0: return {"status": "no_data", "rate": 100.0}

        compliant_count = sum(1 for t in telemetries if self.is_point_inside(t.gps_lng, t.gps_lat))
        compliance_rate = (compliant_count / total) * 100.0
        return {
            "status": "compliant" if compliance_rate > 99.0 else "non_compliant",
            "rate": compliance_rate,
            "total_points": total,
            "out_of_bounds_points": total - compliant_count
        }

    def action_audit_compliance(self, asset_id, asset_type='livestock'):
        """Action hook for generating compliance certificates."""
        return self.check_compliance_for_asset(asset_id, asset_type)
    # --- End of Original Logic ---
