# -*- coding: utf-8 -*-
from odoo import models, fields, api

class AgriIoTWalLog(models.Model):
    _name = 'agri.iot.wal.log'
    _description = 'Agri-IoT Write-Ahead Log Buffer / 遥测预写日志缓冲'
    _order = 'timestamp desc'

    message_guid = fields.Char(string='Message GUID', required=True, index=True)
    device_identifier = fields.Char(string='Device Identifier', required=True, index=True)
    target_matter_id = fields.Many2one('stock.matter.tracking', string='Target Carrier', index=True)
    telemetry_payload = fields.Text(string='JSON Payload')
    timestamp = fields.Datetime(string='Telemetry Timestamp', default=fields.Datetime.now, required=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('processed', 'Processed'),
        ('failed', 'Failed')
    ], string='Processing Status', default='pending', index=True)

    _sql_constraints = [
        ('message_guid_uniq', 'unique(message_guid)', 'Telemetry message GUID must be absolutely unique to guarantee idempotency! (遥测消息GUID必须唯一以保证幂等性！)')
    ]

    @api.model
    def ingest_telemetry(self, guid, device_id, payload, target_id=None):
        """ Safe, idempotent ingestion entrypoint bypassing ORM errors on duplicates """
        try:
            with self.env.cr.savepoint():
                record = self.create({
                    'message_guid': guid,
                    'device_identifier': device_id,
                    'telemetry_payload': payload,
                    'target_matter_id': target_id
                })
                self.flush_model()
                return record
        except Exception as e:
            # On conflict do nothing essentially (catching unique constraint violations softly)
            pass
        return False
