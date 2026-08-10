from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class FarmLocation(models.Model):    _inherit = 'stock.location'

    camera_device_id = fields.Many2one(
        'iiot.device',
        string="Field Camera",
        domain=[('is_camera', '=', True)],
        help="The camera assigned to monitor this specific plot or pond."
    )

class FarmTelemetry(models.Model):
    """
    Farm-specific extension of the agricultural telemetry model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.telemetry'
    _description = 'Agricultural Telemetry Data (Deprecated - Use agri.telemetry)'
    _inherit = 'agri.telemetry'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(
            "farm.telemetry is deprecated. "
            "Please update your code to use agri.telemetry instead."
        )
        return super()._register_hook()
