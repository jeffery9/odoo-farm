# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class IotDeviceMapping(models.Model):
    _name = 'iot.device.mapping'
    _description = 'IoT Device to Business Field Mapper'

    name = fields.Char(string='Mapping Name', required=True)
    device_id = fields.Many2one('iiot.device', string='Source Device', required=True)
    mqtt_topic = fields.Char(string='MQTT Telemetry Topic', required=True, help="Topic to listen for (e.g. farm/meter/01/reading)")
    
    mapping_type = fields.Selection([
        ('field', 'Direct Field Update'),
        ('method', 'Method Execution')
    ], string='Mapping Type', default='field', required=True)

    # Dynamic target mapping
    target_model_id = fields.Many2one('ir.model', string='Target Model', required=True)
    target_field_id = fields.Many2one('ir.model.fields', string='Target Field', 
                                     domain="[('model_id', '=', target_model_id)]")
    
    method_name = fields.Char(string='Method Name', help="Method to call on the target record when telemetry arrives.")
    
    # Matching Logic
    match_record_by = fields.Selection([
        ('context', 'Current Active Record (Context)'),
        ('criteria', 'Domain Criteria (Match Field)')
    ], string='Matching Logic', default='criteria')
    
    match_field_id = fields.Many2one('ir.model.fields', string='Match Record Field',
                                    help="Field on target model to match device identifier (e.g. device_serial)")
    
    active = fields.Boolean(default=True)

    def process_telemetry(self, value, record_id=False):
        """ US-TECH-03-01: Entry point for processing arriving MQTT data. """
        self.ensure_one()
        if self.mapping_type == 'field' and self.target_field_id:
            # Logic to update field
            target_model = self.env[self.target_model_id.model]
            if record_id:
                record = target_model.browse(record_id)
                if record.exists():
                    record.write({self.target_field_id.name: value})
        elif self.mapping_type == 'method' and self.method_name:
            # Logic to call method
            target_model = self.env[self.target_model_id.model]
            if record_id:
                record = target_model.browse(record_id)
                if hasattr(record, self.method_name):
                    getattr(record, self.method_name)(value)
