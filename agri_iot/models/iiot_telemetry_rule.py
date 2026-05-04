# -*- coding: utf-8 -*-
import json
import logging

import jsonpath_ng

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)


class IiotTelemetryRule(models.Model):
    _name = 'iiot.telemetry.rule'
    _description = 'Industrial IoT Telemetry Rule'
    _order = 'profile_id, sequence'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    active = fields.Boolean(string='Active', default=True)

    profile_id = fields.Many2one(
        comodel_name='iiot.device.profile',
        string='Profile',
        required=True,
        help="Associated device profile"
    )
    json_path = fields.Char(
        string='JSON Path',
        required=True,
        default='$.value',
        help="Path to extract value from telemetry payload, e.g. $.temperature"
    )
    target_model = fields.Char(
        string='Target Model',
        required=True,
        help="Target model, e.g. maintenance.equipment"
    )
    target_domain = fields.Char(
        string='Target Domain',
        required=True,
        default="[('id', '!=', 0)]",
        help="Domain to find target records, e.g. [('iot_device_id', '=', '{{ device_id }}')]"
    )
    target_field = fields.Char(
        string='Target Field',
        required=True,
        help="Target field to write to, e.g. x_temperature"
    )

    @api.constrains('json_path')
    def _check_json_path(self):
        for record in self:
            if record.json_path:
                try:
                    # Test if the JSONPath is valid
                    jsonpath_ng.parse(record.json_path)
                except Exception as e:
                    raise ValidationError(_("Invalid JSON Path format: %s\nError: %s") % (record.json_path, str(e)))

    @api.constrains('target_domain')
    def _check_target_domain(self):
        for record in self:
            if record.target_domain:
                try:
                    # Test if the domain is valid by evaluating it (in a safe way)
                    # Just check if it's valid syntax
                    domain_str = record.target_domain.replace('{{', '').replace('}}', '').replace('device_id', '1')
                    safe_eval(domain_str)
                except Exception as e:
                    raise ValidationError(_("Invalid domain format: %s\nError: %s") % (record.target_domain, str(e)))

    def evaluate_domain(self, device_id):
        """Evaluate the target domain with device_id context"""
        self.ensure_one()
        domain_str = self.target_domain.replace('{{ device_id }}', str(device_id))
        try:
            return safe_eval(domain_str)
        except Exception:
            # If evaluation fails, return the original domain
            try:
                return safe_eval(self.target_domain)
            except Exception:
                return []
