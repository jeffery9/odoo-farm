# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class IotTelemetryBuffer(models.Model):
    _name = 'iot.telemetry.buffer'
    _description = 'IoT Raw Telemetry Buffer'
    _order = 'create_date desc'

    mqtt_topic = fields.Char(string='MQTT Topic', required=True, index=True)
    raw_value = fields.Char(string='Raw Value', required=True)
    processed = fields.Boolean(string='Is Processed', default=False, index=True)
    processed_date = fields.Datetime(string='Processed On')
    
    mapping_id = fields.Many2one('iot.device.mapping', string='Applied Mapping', compute='_compute_mapping', store=True)

    @api.depends('mqtt_topic')
    def _compute_mapping(self):
        """ US-TECH-03-02: Link buffer to mapping rule based on topic matching. """
        for rec in self:
            mapping = self.env['iot.device.mapping'].search([
                ('mqtt_topic', '=', rec.mqtt_topic),
                ('active', '=', True)
            ], limit=1)
            rec.mapping_id = mapping

    def cron_process_buffer(self):
        """ US-TECH-03-02: Scheduled action to process telemetry batches asynchronously. """
        buffers = self.search([('processed', '=', False)], limit=1000) # Process in chunks
        _logger.info("IoT Async: Processing %d telemetry records from buffer.", len(buffers))
        
        for buf in buffers:
            if buf.mapping_id:
                try:
                    # Execute logic defined in US-TECH-03-01
                    # Note: We need a strategy to find the right Record ID.
                    # For MOs, we might match by 'state=progress' and device mapping.
                    target_model = buf.mapping_id.target_model_id.model
                    match_field = buf.mapping_id.match_field_id.name if buf.mapping_id.match_field_id else False
                    
                    domain = [('state', '=', 'progress')] # Default to active orders
                    if match_field:
                        # Find records where target field matches device/topic context
                        domain.append((match_field, '=', buf.mqtt_topic))
                    
                    target_records = self.env[target_model].search(domain)
                    for rec in target_records:
                        buf.mapping_id.process_telemetry(buf.raw_value, record_id=rec.id)
                    
                    buf.write({
                        'processed': True,
                        'processed_date': fields.Datetime.now()
                    })
                except Exception as e:
                    _logger.error("IoT Async Error: Failed to process buffer %d: %s", buf.id, str(e))
            else:
                # No mapping found, mark as processed anyway to avoid clogging the buffer
                buf.processed = True
