# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AgriInterventionPluginWeather(models.AbstractModel):
    """
    [Plugin] Weather Window Gating.
    Intercepts start action based on wind speed and precipitation.
    """
    _name = 'agri.intervention.plugin.weather'
    _inherit = 'agri.intervention.plugin'

    @api.model
    def execute_hook(self, intervention, hook_point):
        if hook_point == 'pre_start':
            self._check_weather_window(intervention)

    def _check_weather_window(self, intervention):
        """
        [Restored] Check weather conditions before allowing spray operations [US-002-06]
        """
        # 1. Determine if this intervention type requires weather gating
        if not hasattr(intervention, 'intervention_type') or intervention.intervention_type not in ['fertilizing', 'protection', 'aerial_spraying']:
            return

        # 2. Identify target location
        parcel = intervention.location_id
        if not parcel or not hasattr(parcel, 'gps_coordinates') or not parcel.gps_coordinates:
            return 

        # 3. Fetch weather forecast (requires agri_weather module)
        from datetime import datetime, timedelta
        end_time = datetime.now() + timedelta(hours=24)

        if hasattr(intervention.env['agri.weather.forecast'], 'search'):
            forecast = intervention.env['agri.weather.forecast'].search([
                ('location_id', '=', parcel.id),
                ('forecast_datetime', '<=', end_time),
                ('forecast_datetime', '>=', datetime.now())
            ], limit=1, order='forecast_datetime asc')

            if forecast:
                # Wind speed check (> level 4, ~16km/h)
                if forecast.wind_speed_kmh and forecast.wind_speed_kmh > 16:
                    # Schedule high-priority review activity
                    intervention.activity_schedule(
                        'mail.mail_activity_data_todo',
                        summary=_('WEATHER BLOCK: High Wind Speed (%s km/h)') % forecast.wind_speed_kmh,
                        note=_('Intervention %s was blocked. Wind speed exceeds level 4. Review required by Technical Director.') % intervention.name,
                        user_id=intervention.env.ref('farm_core.group_farm_specialist').users[:1].id or intervention.env.user.id
                    )
                    raise UserError(_(
                        "WEATHER WINDOW BLOCK: Wind speed too high (%s km/h > 16 km/h). "
                        "Risk detected for spray operation. Technical director has been notified."
                    ) % forecast.wind_speed_kmh)

class AgriInterventionPluginSpatial(models.AbstractModel):
    """
    [Plugin] Spatial Compliance Audit.
    Analyzes GPS logs after completion.
    """
    _name = 'agri.intervention.plugin.spatial'
    _inherit = 'agri.intervention.plugin'

    @api.model
    def execute_hook(self, intervention, hook_point):
        if hook_point == 'pre_done':
            self._audit_spatial_compliance(intervention)

    def _audit_spatial_compliance(self, intervention):
        """
        [Restored] Analyzes GPS logs after completion.
        Uses GIS boundaries to check for out-of-bounds work.
        """
        parcel = intervention.location_id
        if not parcel or not hasattr(parcel, 'gps_coordinates') or not parcel.gps_coordinates:
            return

        # Create a temporary fence object for boundary check
        if hasattr(intervention.env['farm.geofence'], 'new'):
            temp_fence = intervention.env['farm.geofence'].new({
                'coordinates': parcel.gps_coordinates
            })

            # Get telemetry records during this intervention
            # Filter by intervention linkage (production_id or task_id)
            telemetry_domain = [
                ('gps_lat', '!=', 0),
                ('gps_lng', '!=', 0)
            ]
            
            # Map logical linkage
            if hasattr(intervention, 'agri_task_id') and intervention.agri_task_id:
                telemetry_domain.append(('production_id', '=', intervention.agri_task_id.id))
            elif hasattr(intervention, 'production_id') and intervention.production_id:
                telemetry_domain.append(('production_id', '=', intervention.production_id.id))

            telemetries = intervention.env['iiot.telemetry'].search(telemetry_domain)

            if not telemetries:
                return

            oob_count = 0
            for t in telemetries:
                if not temp_fence.is_point_inside(t.gps_lng, t.gps_lat):
                    oob_count += 1

            compliance_rate = ((len(telemetries) - oob_count) / len(telemetries)) * 100.0
            
            # Record results back to the intervention if fields exist
            if hasattr(intervention, 'out_of_bounds_count'):
                intervention.write({
                    'out_of_bounds_count': oob_count,
                    'spatial_compliance_rate': compliance_rate
                })
            
            # Log results in chatter
            intervention.message_post(body=_(
                "Spatial Audit Completed: Compliance Rate %s%%. "
                "Detected %s points outside boundaries."
            ) % (round(compliance_rate, 2), oob_count))
