from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    weather_api_key = fields.Char(
        string="Weather API Key (OpenWeatherMap)",
        config_parameter='farm_weather.api_key'
    )
