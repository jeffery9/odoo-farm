# -*- coding: utf-8 -*-
from odoo import fields, models

class FarmLocation(models.Model):
    _inherit = 'farm.location'

    geom_3d_polygon = fields.Char(
        string='3D Airspace Polygon WKT (三维领空多边形 WKT)',
        help='WKT representation of Polygon Z, e.g., POLYGON Z ((0 0 10, 0 5 10, 5 5 20, 0 0 10)) (CN: WKT 格式的三维多边形，包含高度Z轴)',
        default=''
    )

    def check_uav_trajectory_intersection(self, uav_trajectory_wkt):
        """ 
        Perform a 3D physical intersection test using ST_3DIntersects under PostgreSQL PostGIS.
        Takes a UAV Linestring Z trajectory and checks if it intersects this airspace boundary.
        """
        self.ensure_one()
        if not self.geom_3d_polygon:
            return False
            
        # Ensure PostGIS extension is loaded in the PostgreSQL database
        self.env.cr.execute("CREATE EXTENSION IF NOT EXISTS postgis CASCADE;")

        query = """
            SELECT ST_3DIntersects(
                ST_GeomFromText(%s::text, 4326),
                ST_GeomFromText(%s::text, 4326)
            ) as intersects;
        """
        self.env.cr.execute(query, (uav_trajectory_wkt, self.geom_3d_polygon))
        res = self.env.cr.fetchone()
        return res[0] if res else False
