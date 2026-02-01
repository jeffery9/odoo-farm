# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import json
import jsonpath_ng


from odoo.tools.safe_eval import safe_eval








class IiotTelemetryRule(models.Model):


    _name = 'iiot.telemetry.rule'


    _description = 'Industrial IoT Telemetry Rule'


    _order = 'profile_id, sequence'





    name = fields.Char('Name', required=True)


    sequence = fields.Integer('Sequence', default=10)


    active = fields.Boolean('Active', default=True)





    profile_id = fields.Many2one(


        'iiot.device.profile',


        'Profile',


        required=True,


        help='Associated device profile'


    )





    json_path = fields.Char(


        'JSON Path',


        required=True,


        help='Path to extract value from telemetry payload, e.g. $.temperature',


        default='$.value'


    )





    target_model = fields.Char(


        'Target Model',


        required=True,


        help='Target model, e.g. maintenance.equipment'


    )





    target_domain = fields.Char(


        'Target Domain',


        required=True,


        help='Domain to find target records, e.g. [(\'iot_device_id\', \'=\', \'{{ device_id }}\')]',


        default="[('id', '!=', 0)]"


    )





    target_field = fields.Char(


        'Target Field',


        required=True,


        help='Target field to write to, e.g. x_temperature'


    )





    @api.constrains('json_path')


    def _check_json_path(self):


        for record in self:


            if record.json_path:


                try:


                    # Test if the JSONPath is valid


                    jsonpath_ng.parse(record.json_path)


                except Exception:


                    raise ValidationError(_("Invalid JSON Path format: %s") % record.json_path)





    @api.constrains('target_domain')


    def _check_target_domain(self):


        for record in self:


            if record.target_domain:


                try:


                    # Test if the domain is valid by evaluating it (in a safe way)


                    # Just check if it's valid syntax


                    domain_str = record.target_domain.replace('{{', '').replace('}}', '').replace('device_id', '1')


                    safe_eval(domain_str)


                except Exception:


                    raise ValidationError(_("Invalid domain format: %s") % record.target_domain)





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

