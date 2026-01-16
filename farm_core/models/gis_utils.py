from odoo import models, fields, api
import math


class GISCoordinateUtils(models.AbstractModel):
    """
    Utility class for GIS coordinate calculations and geofencing
    """
    _name = 'farm.core.gis.utils'
    _description = 'Farm Core GIS Utilities'

    @api.model
    def calculate_area_from_geojson(self, geojson_data, lat_avg=None):
        """
        Calculate area from GeoJSON polygon coordinates using Shoelace formula
        """
        try:
            import json
            if isinstance(geojson_data, str):
                data = json.loads(geojson_data)
            else:
                data = geojson_data

            coords = []
            if data.get('type') == 'Polygon':
                coords = data['coordinates'][0]  # Exterior ring
            elif data.get('type') == 'Feature' and data['geometry']['type'] == 'Polygon':
                coords = data['geometry']['coordinates'][0]  # Exterior ring

            if len(coords) < 3:
                return 0.0

            # Shoelace algorithm for spherical coordinates (simplified to planar)
            area = 0.0
            n = len(coords)
            for i in range(n):
                j = (i + 1) % n
                area += coords[i][0] * coords[j][1]
                area -= coords[j][0] * coords[i][1]

            area = abs(area) / 2.0

            # Calculate average latitude if not provided
            if lat_avg is None:
                lat_avg = sum(c[1] for c in coords) / n

            # Convert from square degrees to square meters using approximate conversion
            meters_per_deg_lat = 111132.0
            meters_per_deg_lng = 111132.0 * math.cos(math.radians(lat_avg))

            real_area_sqm = area * meters_per_deg_lat * meters_per_deg_lng
            area_hectares = real_area_sqm / 10000.0  # Convert to hectares

            return area_hectares

        except Exception as e:
            # Log error but don't crash
            import logging
            _logger = logging.getLogger(__name__)
            _logger.error("Area calculation failed: %s", str(e))
            return 0.0

    @api.model
    def is_point_in_polygon(self, coordinates_str, lon, lat):
        """
        Point-in-polygon test using ray casting algorithm
        coordinates_str: "lon,lat;lon,lat;lon,lat..." format
        """
        try:
            points = [tuple(map(float, p.split(','))) for p in coordinates_str.split(';') if ',' in p]
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

    @api.model
    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculate distance between two GPS points using Haversine formula
        Returns distance in meters
        """
        R = 6371000  # Earth's radius in meters

        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))

        return R * c  # Distance in meters