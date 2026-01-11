# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re


class IiotDeviceProfile(models.Model):
    _name = 'iiot.device.profile'
    _description = 'Industrial IoT Device Profile'
    _order = 'code'

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True, help='Device type code, e.g. cnc_v1')
    telemetry_topic_template = fields.Char(
        'Telemetry Topic Template',
        default='telemetry/{device}/data',
        help='Telemetry topic template, e.g. telemetry/{device}/data'
    )
    command_topic_template = fields.Char(
        'Command Topic Template',
        default='cmd/{device}/request',
        help='Command topic template, e.g. cmd/{device}/request'
    )
    ota_notify_topic_template = fields.Char(
        'OTA Notify Topic Template',
        default='ota/{device}/notify',
        help='OTA notify topic template, e.g. ota/{device}/notify'
    )
    ota_status_topic_template = fields.Char(
        'OTA Status Topic Template',
        default='ota/{device}/status',
        help='OTA status topic template, e.g. ota/{device}/status'
    )
    command_template = fields.Text(
        'Command Template',
        default='{"action": "{{ action }}", "params": {{ params | tojson }}}',
        help='Command message template (Jinja2), e.g. {"action": "{{ action }}", "params": {{ params | tojson }}}'
    )

    # Validation for templates to ensure they have required placeholders
    @api.constrains('telemetry_topic_template', 'command_topic_template',
                    'ota_notify_topic_template', 'ota_status_topic_template')
    def _check_topic_templates(self):
        for record in self:
            templates = [
                record.telemetry_topic_template,
                record.command_topic_template,
                record.ota_notify_topic_template,
                record.ota_status_topic_template,
            ]
            for topic_template in templates:
                if topic_template and '{device}' not in topic_template:
                    raise ValidationError(_("Topic template must contain {device} placeholder"))

    @api.constrains('code')
    def _check_code(self):
        for record in self:
            if not re.match(r'^[a-zA-Z0-9_-]+$', record.code):
                raise ValidationError(_("Device type code can only contain letters, numbers, underscores and hyphens"))