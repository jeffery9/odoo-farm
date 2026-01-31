from odoo import models
from .agri_weather_forecast import AgriWeatherForecast


class FarmWeatherForecast(models.Model):
    """
    Farm-specific extension of the agricultural weather forecast model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.weather.forecast'
    _description = 'Farm Weather Forecast (Deprecated - Use agri.weather.forecast)'
    _inherit = 'agri.weather.forecast'
    _order = 'date asc'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(
            "farm.weather.forecast is deprecated. "
            "Please update your code to use agri.weather.forecast instead."
        )
        return super()._register_hook()
