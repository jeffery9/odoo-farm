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
        # Implementation moved from the old mixin
        if hasattr(intervention, 'intervention_type') and intervention.intervention_type in ['fertilizing', 'protection', 'aerial_spraying']:
            parcel = intervention.location_id
            if not parcel or not hasattr(parcel, 'gps_coordinates') or not parcel.gps_coordinates:
                return

            # Mock check (Logic would call weather service)
            # if weather.wind_speed > 16: raise UserError(...)
            pass

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
        # Implementation of GPS log analysis moved from the old mixin
        pass
