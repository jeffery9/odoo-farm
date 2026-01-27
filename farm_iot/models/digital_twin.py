from odoo import models, fields, api, _
import json

class FarmLocation(models.Model):
    _inherit = 'farm.location'

    digital_twin_enabled = fields.Boolean("Digital Twin Enabled", default=False)
    digital_twin_scene_id = fields.Many2one('farm.digital.twin.scene', string="3D Scene")

class FarmDigitalTwinScene(models.Model):
    _name = 'farm.digital.twin.scene'
    _description = 'Farm Digital Twin 3D Scene'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Scene Name", required=True)
    location_id = fields.Many2one('farm.location', string="Physical Location")
    
    # Scene Assets
    base_model_url = fields.Char("Base Terrain/Structure Model URL", help="URL to GLB/USDZ file")
    environment_hdr_url = fields.Char("Environment HDR URL")
    
    device_marker_ids = fields.One2many('farm.digital.twin.marker', 'scene_id', string="Device Markers")

    state = fields.Selection([('draft', 'Draft'), ('active', 'Active')], default='draft')

class FarmDigitalTwinMarker(models.Model):
    _name = 'farm.digital.twin.marker'
    _description = 'Digital Twin Device Marker'

    scene_id = fields.Many2one('farm.digital.twin.scene', ondelete='cascade')
    device_id = fields.Many2one('iiot.device', string="Physical Device", required=True)
    
    # 3D Coordinates relative to scene center
    pos_x = fields.Float("X Position")
    pos_y = fields.Float("Y Position")
    pos_z = fields.Float("Z Position")
    
    rotation_y = fields.Float("Y Rotation")
    
    display_telemetry_ids = fields.Many2many('iiot.device.profile.telemetry', string="Telemetries to Display")

class IiotDevice(models.Model):
    _inherit = 'iiot.device'

    digital_twin_model_url = fields.Char("3D Model URL", help="Specific 3D model for this device")
    last_telemetry_json = fields.Text("Last Telemetry JSON", compute='_compute_last_telemetry_json')

    def _compute_last_telemetry_json(self):
        """Used by Digital Twin frontend to get live values"""
        for device in self:
            # Fetch latest telemetry data
            telemetry = self.env['farm.telemetry'].search([
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
