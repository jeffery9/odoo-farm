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

    name = fields.Char('Name', compute='_compute_name', store=True)
    serial_number = fields.Char('Serial Number', required=True, copy=False, help='Physical serial number (unique)')
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

    # 视频流集成 [US-16-01]
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

    # Integrations for Farm IIoT
    command_log_ids = fields.One2many('farm.command.log', 'device_id', string="Command History")
    active_alert_ids = fields.One2many('mail.activity', 'res_id', domain=[('res_model', '=', 'iiot.device'), ('state', '!=', 'done')], string="Active Alerts") # Assuming mail.activity for alerts

    # Tracking
    created_date = fields.Datetime('Created Date', default=fields.Datetime.now)
    last_update = fields.Datetime('Last Update', default=fields.Datetime.now)

    _sql_constraints = [
        ('serial_number_uniq', 'UNIQUE(serial_number)', 'Serial number must be unique!'),
        ('device_id_uniq', 'UNIQUE(device_id)', 'Device ID must be unique!'),
    ]

    @api.model
    def _get_business_models(self):
        # Return a list of models that can be referenced
        # This can be extended based on actual business needs
        return [
            ('maintenance.equipment', 'Maintenance Equipment'),
            ('mrp.workcenter', 'Work Center'),
            ('stock.location', 'Stock Location'),
            ('product.product', 'Product'),
            ('project.task', 'Project Task'),
        ]

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
        """
        Generate complete Topic list with SaaS isolation [company_id prefix]
        """
        self.ensure_one()
        if not self.profile_id:
            return {}

        profile = self.profile_id
        device_id = self.device_id
        # 强制增加公司前缀，确保 SaaS 多租户隔离
        prefix = f"company_{self.env.company.id}/"

        return {
            'telemetry': prefix + profile.telemetry_topic_template.format(device=device_id),
            'command': prefix + profile.command_topic_template.format(device=device_id),
            'ota_notify': prefix + profile.ota_notify_topic_template.format(device=device_id),
            'ota_status': prefix + profile.ota_status_topic_template.format(device=device_id),
        }

    def send_command(self, action, **params):
        """Send command with SaaS isolation"""
        self.ensure_one()

        if not self.profile_id:
            raise UserError(_("Device not associated with communication profile"))

        # Get command topic with prefix
        prefix = f"company_{self.env.company.id}/"
        command_topic = prefix + self.profile_id.command_topic_template.format(device=self.device_id)

        # Render command message using Jinja2 template
        try:
            from jinja2 import Template
            template = Template(self.profile_id.command_template)
            message = template.render(action=action, params=params)
            command_payload = json.loads(message)
        except Exception as e:
            raise UserError(_("Command template rendering failed: %s") % str(e))

        # Send command via HTTP-to-MQTT bridge
        # This would call the HTTP gateway that forwards to MQTT
        mqtt_bridge_url = self.env['ir.config_parameter'].sudo().get_param('iiot.mqtt_bridge_url')

        if not mqtt_bridge_url:
            raise UserError(_("MQTT gateway URL not configured"))

        try:
            response = requests.post(
                f"{mqtt_bridge_url}/publish",
                json={
                    'topic': command_topic,
                    'payload': command_payload
                },
                timeout=10
            )
            if response.status_code == 200:
                self.last_command = fields.Datetime.now()
                # Log the command in farm.command.log
                self.env['farm.command.log'].create({
                    'device_id': self.id,
                    'command': action,
                    'params': json.dumps(params),
                    'status': 'success',
                })
                return True
            else:
                # Log failed command
                self.env['farm.command.log'].create({
                    'device_id': self.id,
                    'command': action,
                    'params': json.dumps(params),
                    'status': 'failed',
                })
                raise UserError(_("Failed to send command: %s") % response.text)
        except Exception as e:
            # Log error command
            self.env['farm.command.log'].create({
                'device_id': self.id,
                'command': action,
                'params': json.dumps(params),
                'status': 'failed',
            })
            raise UserError(_("Error occurred while sending command: %s") % str(e))

    def process_telemetry_data(self, telemetry_data):
        """Process incoming telemetry data based on rules"""
        self.ensure_one()

        # Update last telemetry time
        self.last_telemetry = fields.Datetime.now()
        self.connection_status = 'online'

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

    @api.model
    def create(self, vals):
        if 'device_id' not in vals:
            # Generate device ID from serial number or use default
            serial = vals.get('serial_number', 'device')
            vals['device_id'] = serial.replace(' ', '_').replace('-', '_').lower()

        if 'config_token' not in vals:
            # Generate initial config token
            vals['config_token'] = str(uuid.uuid4())

        record = super().create(vals)
        return record

