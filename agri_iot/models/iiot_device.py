# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import uuid
import json
import requests
from datetime import datetime
# For logger - needed for error logging in process_telemetry_data
import logging
_logger = logging.getLogger(__name__)

class IiotDevice(models.Model):
    _name = 'iiot.device'
    _description = 'Industrial IoT Device'
    _order = 'serial_number'

    name = fields.Char('Name', compute='_compute_name', store=True, precompute=True)
    serial_number = fields.Char('Serial Number', required=True, copy=False, help='Physical serial number (unique, index=True)')
    device_id = fields.Char('Device ID', required=True, copy=False, help='Logical ID for Topics')
    profile_id = fields.Many2one(
        'iiot.device.profile',
        'Communication Profile',
        required=True,
        help='Associated communication profile'
    )
    business_ref = fields.Reference(
        selection='_get_business_models',
        string='Business Reference',
        help='Associated business entity (equipment/workcenter/location)'
    )
    config_token = fields.Char('Config Token', copy=False, help='One-time configuration download token')
    firmware_version = fields.Char('Firmware Version', help='Current firmware version')

    # Physical Topology [ISA-95 L2/L1]
    parent_id = fields.Many2one('iiot.device', string='Parent Device', help='Physical upstream gateway or controller', ondelete='restrict')
    child_ids = fields.One2many('iiot.device', 'parent_id', string='Sub-devices')
    physical_level = fields.Selection([
        ('gateway', 'Gateway/Edge Server'),
        ('controller', 'Controller/PLC'),
        ('node', 'Sensor Node'),
        ('sensor', 'Sub-sensor/Module')
    ], string='Physical Level', default='node')

    # 设备影子 [US-TECH-04-01]
    shadow_state = fields.Text('Device Shadow', help='Last known state (JSON)')
    shadow_update = fields.Datetime('Shadow Last Update')

    # 视频流集成 [US-039-01]
    is_camera = fields.Boolean("Is Camera", default=False)
    live_stream_url = fields.Char("Live Stream URL", help="HLS/HTTP/RTSP stream URL for the camera")

    # Status fields
    is_active = fields.Boolean('Active', default=True)
    last_telemetry = fields.Datetime('Last Telemetry')
    last_command = fields.Datetime('Last Command')
    connection_status = fields.Selection([
        ('offline', 'Offline'),
        ('online', 'Online'),
        ('error', 'Error')
    ], string='Connection Status', default='offline')

    # Tracking
    created_date = fields.Datetime('Created Date', default=fields.Datetime.now)
    last_update = fields.Datetime('Last Update', default=fields.Datetime.now)

    _serial_number_uniq = models.Constraint(
        'UNIQUE(serial_number)',
        'Serial number must be unique!'
    )
    _device_id_uniq = models.Constraint(
        'UNIQUE(device_id)',
        'Device ID must be unique!'
    )

    @api.model
    def _get_business_models(self):
        # Return a list of models that can be referenced
        # This should be extended by business modules (e.g., via _inherit)
        return []

    @api.depends('serial_number', 'device_id')
    def _compute_name(self):
        for device in self:
            device.name = f"{device.serial_number} ({device.device_id})"

    @api.constrains('device_id')
    def _check_device_id_format(self):
        import re
        for record in self:
            if not re.match(r'^[a-zA-Z0-9_-]+$', record.device_id):
                raise ValidationError(_("Device ID can only contain letters, numbers, underscores and hyphens"))

    def action_generate_config_token(self):
        """Generate pairing token"""
        for device in self:
            device.config_token = str(uuid.uuid4())
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('Configuration download token generated'),
                'type': 'success',
                'sticky': False,
            }
        }

    def get_topic_map(self):
        """Generate complete Topic list"""
        self.ensure_one()
        if not self.profile_id:
            return {}

        profile = self.profile_id
        device_id = self.device_id

        return {
            'telemetry': profile.telemetry_topic_template.format(device=device_id),
            'command': profile.command_topic_template.format(device=device_id),
            'ota_notify': profile.ota_notify_topic_template.format(device=device_id),
            'ota_status': profile.ota_status_topic_template.format(device=device_id),
        }

    def send_command(self, action, **params):
        """Send command via gateway"""
        self.ensure_one()

        if not self.profile_id:
            raise UserError(_("Device not associated with communication profile"))

        # Find gateway managing this device
        gateway = self.env['iiot.gateway'].sudo().search([('device_ids', 'in', self.id)], limit=1)
        
        # Fallback to the first online gateway if not specifically assigned
        if not gateway:
            gateway = self.env['iiot.gateway'].sudo().search([('state', '=', 'online')], limit=1)

        if not gateway or not gateway.url:
            raise UserError(_("No online IoT Gateway found to handle this command"))

        try:
            # Use the unified webhook endpoint on the bridge
            webhook_url = f"{gateway.url.rstrip('/')}/api/v1/webhook"
            
            response = requests.post(
                webhook_url,
                json={
                    'event': 'command',
                    'payload': {
                        'device_id': self.device_id,
                        'action': action,
                        'params': params
                    }
                },
                timeout=10
            )
            
            if response.status_code == 200 and response.json().get('status') == 'success':
                self.last_command = fields.Datetime.now()
                return True
            else:
                error_detail = response.text
                try:
                    error_detail = response.json().get('error', response.text)
                except:
                    pass
                raise UserError(_("Gateway rejected command: %s") % error_detail)
                
        except Exception as e:
            raise UserError(_("Error occurred while sending command to gateway: %s") % str(e))

    def process_telemetry_data(self, telemetry_data):
        """Process incoming telemetry data and update Device Shadow"""
        self.ensure_one()

        # Update last telemetry time
        self.last_telemetry = fields.Datetime.now()
        self.connection_status = 'online'

        # Update Device Shadow [US-TECH-04-01]
        try:
            current_shadow = json.loads(self.shadow_state) if self.shadow_state else {}
            # Merge new telemetry into shadow
            if isinstance(telemetry_data, dict):
                current_shadow.update(telemetry_data)
                self.shadow_state = json.dumps(current_shadow)
                self.shadow_update = fields.Datetime.now()
        except Exception as e:
            _logger.error(f"Failed to update shadow for {self.device_id}: {str(e)}")

        # Process according to telemetry rules
        for rule in self.profile_id.iiot_telemetry_rule_ids:
            if not rule.active:
                continue

            try:
                # Extract value using JSONPath
                import jsonpath_ng
                jsonpath_expr = jsonpath_ng.parse(rule.json_path)
                matches = [match.value for match in jsonpath_expr.find(telemetry_data)]

                if not matches:
                    continue

                value = matches[0]  # Take the first match

                # Find target record
                domain = rule.evaluate_domain(self.id)
                target_model = self.env[rule.target_model]
                target_records = target_model.search(domain)

                if target_records:
                    # Update the field with the extracted value
                    for target_record in target_records:
                        target_record.write({rule.target_field: value})

            except Exception as e:
                # Log error but continue processing other rules
                _logger.error(f"Error processing telemetry rule {rule.name} for device {self.device_id}: {str(e)}")

    def write(self, vals):
        vals['last_update'] = fields.Datetime.now()
        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        if isinstance(vals_list, dict):
            vals_list = [vals_list]
        for vals in vals_list:
            if isinstance(vals, list):
                vals = vals[0]  # Just in case Odoo passes a nested list
            if 'device_id' not in vals:
                serial = vals.get('serial_number', 'device')
                vals['device_id'] = serial.replace(' ', '_').replace('-', '_').lower()
            if 'config_token' not in vals:
                vals['config_token'] = str(uuid.uuid4())
        return super().create(vals_list)

