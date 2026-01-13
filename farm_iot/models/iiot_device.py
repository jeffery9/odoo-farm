from odoo import models, fields

class IiotDevice(models.Model):
    _inherit = 'iiot.device'

    # 地理围栏安全 [US-23-01] - 在业务集成层实现
    geofence_id = fields.Many2one(
        'farm.geofence', 
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
