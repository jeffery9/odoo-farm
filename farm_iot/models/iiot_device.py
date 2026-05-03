from odoo import models, fields, api
import json

class IiotDevice(models.Model):
    _name = 'iiot.device'
    _inherit = 'iiot.device'

    # 地理围栏安全 [US-23-01] - 在业务集成层实现
    geofence_id = fields.Many2one(
        'agri.geospatial.geofence', 
        string="Safety Geofence", 
        help="Assigned virtual fence for boundary monitoring."
    )

    # 业务集成字段：指令日志与告警 [US-23-01, US-14-06]
    command_log_ids = fields.One2many('farm.command.log', 'device_id', string="Command History")
    active_alert_ids = fields.One2many(
        'mail.activity', 
        'res_id', 
        domain=[('res_model', '=', 'iiot.device'), ('state', '!=', 'done')], 
        string="Active Alerts"
    )

    def send_command(self, action, **params):
        """ Overridden to add business logging in farm_iot layer """
        res = super(IiotDevice, self).send_command(action, **params)
        if res:
            self.env['farm.command.log'].create({
                'device_id': self.id,
                'command': action,
                'payload': json.dumps(params) if params else '{}',
                'status': 'dispatched'
            })
        return res
