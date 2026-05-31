# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class IiotGateway(models.Model):
    _name = 'iiot.gateway'
    _description = 'Industrial IoT Gateway/Bridge'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Gateway Name', required=True)
    gateway_id = fields.Char('Gateway ID', required=True, index=True)
    url = fields.Char('Public URL', help="Publicly accessible URL of the gateway")
    state = fields.Selection([
        ('offline', 'Offline'),
        ('online', 'Online'),
    ], default='offline', string='Status', tracking=True)
    
    last_seen = fields.Datetime('Last Heartbeat')
    
    # MQTT Configuration for the Bridge to use
    mqtt_host = fields.Char('MQTT Broker Host')
    mqtt_port = fields.Integer('MQTT Broker Port', default=8883)
    mqtt_user = fields.Char('MQTT Username')
    mqtt_password = fields.Char('MQTT Password')
    mqtt_use_tls = fields.Boolean('Use TLS', default=True)

    device_ids = fields.Many2many('iiot.device', string='Managed Devices')
    
    _sql_constraints = [
        ('gateway_id_uniq', 'unique(gateway_id)', 'Gateway ID must be unique!'),
    ]

    def action_ping(self):
        """Manually check gateway status using webhook ping"""
        self.ensure_one()
        if not self.url:
            raise UserError(_("Gateway URL is not configured"))
            
        try:
            webhook_url = f"{self.url.rstrip('/')}/api/v1/webhook"
            response = requests.post(
                webhook_url,
                json={'event': 'ping'},
                timeout=5
            )
            if response.status_code == 200 and response.json().get('status') == 'pong':
                self.write({
                    'state': 'online',
                    'last_seen': fields.Datetime.now()
                })
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('Success'),
                        'message': _('Gateway is online (Pong received)'),
                        'type': 'success',
                        'sticky': False,
                    }
                }
            else:
                self.write({'state': 'offline'})
                raise UserError(_("Gateway returned invalid response: %s") % response.text)
        except Exception as e:
            self.write({'state': 'offline'})
            raise UserError(_("Gateway is unreachable: %s") % str(e))

    def action_sync_subscriptions(self):
        """Register Odoo webhooks on the bridge"""
        self.ensure_one()
        if not self.url:
            raise UserError(_("Gateway URL is not configured"))
        
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        # Standard Odoo webhook endpoints
        webhook_url = f"{base_url.rstrip('/')}/iiot/webhook"
        
        try:
            webhook_reg_url = f"{self.url.rstrip('/')}/api/v1/webhook"
            response = requests.post(
                webhook_reg_url,
                json={
                    'event': 'subscribe',
                    'payload': {
                        'callback_url': webhook_url,
                        'events': ['telemetry', 'ota_status', 'command_ack']
                    }
                },
                timeout=10
            )
            
            if response.status_code == 200 and response.json().get('status') == 'success':
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('Success'),
                        'message': _('Webhooks registered on the bridge'),
                        'type': 'success',
                        'sticky': False,
                    }
                }
            else:
                raise UserError(_("Bridge rejected subscription: %s") % response.text)
                
        except Exception as e:
            raise UserError(_("Error syncing subscriptions: %s") % str(e))
