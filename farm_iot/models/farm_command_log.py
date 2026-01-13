from odoo import models, fields, api

class FarmCommandLog(models.Model):
    _name = 'farm.command.log'
    _description = 'IOT Command Audit Log'
    _order = 'create_date desc'

    device_id = fields.Many2one('iiot.device', string="Device", required=True)
    command = fields.Char("Command", required=True)
    params = fields.Text("Parameters")
    
    status = fields.Selection([
        ('sent', 'Sent'),
        ('success', 'Success'),
        ('failed', 'Failed')
    ], default='sent')
    
    execution_time_ms = fields.Integer("Latency (ms)", help="Response latency in milliseconds")
    user_id = fields.Many2one('res.users', string="Triggered By", default=lambda self: self.env.user)
    create_date = fields.Datetime("Timestamp", readonly=True)