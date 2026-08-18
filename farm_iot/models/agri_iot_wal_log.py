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

    _message_guid_uniq = models.Constraint(
        'unique(message_guid)',
        'Telemetry message GUID must be absolutely unique to guarantee idempotency! (遥测消息GUID必须唯一以保证幂等性！)'
    )

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

    @api.model
    def action_process_pending_wal(self):
        """ Process all pending Write-Ahead Logs into real telemetry and update tracking state """
        pending_logs = self.search([('status', '=', 'pending')], order='timestamp asc', limit=100)
        for log in pending_logs:
            try:
                with self.env.cr.savepoint():
                    # 1. Parse JSON payload safely
                    import json
                    try:
                        payload = json.loads(log.telemetry_payload or '{}')
                    except Exception:
                        log.write({'status': 'failed'})
                        continue

                    # 2. Lookup IIoT Device by device_id or serial_number
                    device = self.env['iiot.device'].search([('device_id', '=', log.device_identifier)], limit=1)
                    if not device:
                        device = self.env['iiot.device'].search([('serial_number', '=', log.device_identifier)], limit=1)
                    
                    if not device:
                        # Create fallback node to prevent dropping telemetry
                        profile = self.env['iiot.device.profile'].search([], limit=1)
                        if not profile:
                            profile = self.env['iiot.device.profile'].create({
                                'name': 'Default Profile',
                                'code': 'default'
                            })
                        device = self.env['iiot.device'].create({
                            'device_id': log.device_identifier,
                            'serial_number': log.device_identifier,
                            'profile_id': profile.id,
                            'physical_level': 'node'
                        })

                    # 3. Create real physical Telemetry record
                    sensor_type = payload.get('sensor_type', 'temperature')
                    val = float(payload.get('value', payload.get('temp', 0.0)))
                    lat = float(payload.get('gps_lat', 0.0))
                    lng = float(payload.get('gps_lng', 0.0))

                    telemetry = self.env['iiot.telemetry'].create({
                        'name': f"{device.name or device.device_id} - {sensor_type}",
                        'sensor_type': sensor_type,
                        'value': val,
                        'device_id': device.id,
                        'gps_lat': lat,
                        'gps_lng': lng,
                        'timestamp': log.timestamp
                    })

                    # 4. Update Device Shadow State (JSON Cache)
                    device.write({
                        'shadow_state': json.dumps(payload),
                        'shadow_update': fields.Datetime.now()
                    })

                    # 5. Integrate with associated Carrier & post Chatter Card
                    carrier = log.target_matter_id
                    if carrier:
                        carrier_updates = {}
                        if 'weight' in payload or 'current_weight' in payload:
                            carrier_updates['current_weight'] = float(payload.get('weight', payload.get('current_weight')))
                        if lat and lng:
                            carrier_updates['last_gps_lat'] = lat
                            carrier_updates['last_gps_lng'] = lng
                            carrier_updates['last_location_update'] = log.timestamp
                        
                        if carrier_updates:
                            carrier.with_context(bypass_carrier_transition_rules=True).write(carrier_updates)

                        # Trigger the Messaging-first Colocation Chatter Event
                        body_payload = f"Device Reading: {val} {sensor_type} / 遥测读数: {val} {sensor_type}"
                        carrier.log_iot_event(device.device_id, body_payload, level=payload.get('level', 'info'))

                    # 6. Flag log as successfully processed
                    log.write({'status': 'processed'})
                    self.flush_model()
            except Exception as e:
                import logging
                _logger = logging.getLogger(__name__)
                _logger.exception("WAL Ingestion Failed! Error: %s", e)
                log.write({'status': 'failed'})
                self.flush_model()
        return True
