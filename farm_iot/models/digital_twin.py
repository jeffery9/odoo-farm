from odoo import models, fields, api, _
import logging
import json

_logger = logging.getLogger(__name__)

class FarmLocation(models.Model):
    _name = 'farm.location'
    _inherit = 'farm.location'

    digital_twin_enabled = fields.Boolean("Digital Twin Enabled", default=False)
    digital_twin_scene_id = fields.Many2one('agri.digital.twin.scene', string="3D Scene")

class FarmDigitalTwinScene(models.Model):
    """
    Farm-specific extension of the agricultural digital twin scene model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.digital.twin.scene'
    _description = 'Digital Twin 3D Scene (Deprecated - Use agri.digital.twin.scene)'
    _inherit = 'agri.digital.twin.scene'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(
            "farm.digital.twin.scene is deprecated. "
            "Please update your code to use agri.digital.twin.scene instead."
        )
        return super()._register_hook()

class FarmDigitalTwinMarker(models.Model):
    """
    Farm-specific extension of the agricultural digital twin marker model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.digital.twin.marker'
    _description = 'Digital Twin Device Marker (Deprecated - Use agri.digital.twin.marker)'
    _inherit = 'agri.digital.twin.marker'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(
            "farm.digital.twin.marker is deprecated. "
            "Please update your code to use agri.digital.twin.marker instead."
        )
        return super()._register_hook()

# Note: FarmLocation and IiotDevice remain as is since they're only inheritance extensions
class IiotDevice(models.Model):
    _name = 'iiot.device'
    _inherit = 'iiot.device'

    digital_twin_model_url = fields.Char("3D Model URL", help="Specific 3D model for this device")
    last_telemetry_json = fields.Text("Last Telemetry JSON", compute='_compute_last_telemetry_json')

    def _compute_last_telemetry_json(self):
        """Used by Digital Twin frontend to get live values"""
        for device in self:
            # Fetch latest telemetry data
            telemetry = self.env['iiot.telemetry'].search([
                ('device_id', '=', device.id)
            ], order='timestamp desc', limit=1)
            if telemetry:
                # Assuming data is stored in a JSON field or multiple fields
                # This is a simplified version
                data = {
                    'status': device.connection_status,
                    'timestamp': telemetry.timestamp.isoformat() if telemetry.timestamp else None,
                    # Add more fields based on farm_telemetry.py
                }
                device.last_telemetry_json = json.dumps(data)
            else:
                device.last_telemetry_json = "{}"
