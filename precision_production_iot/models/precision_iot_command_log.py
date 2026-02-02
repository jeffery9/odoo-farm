# -*- coding: utf-8 -*-
from odoo import models, fields, api

class PrecisionIotCommandLog(models.Model):
    """ [US-201-IOT] 配方边缘：专用生产指令审计日志（独立存储） """
    _name = 'precision.iot.command.log'
    _description = 'Precision Production IoT Command Log'
    _order = 'create_date desc'

    device_id = fields.Many2one('precision.iot.device', string="Edge Device", required=True)
    command = fields.Char("Action", required=True)
    payload = fields.Text("Payload")
    
    status = fields.Selection([
        ('dispatched', 'Dispatched'),
        ('success', 'Success'),
        ('failed', 'Failed')
    ], default='dispatched', string="Status")

    # [Level 2 Traceability]
    production_id = fields.Many2one('mrp.production', string="Production Order (MO)")
    phase_id = fields.Many2one('precision.recipe.phase', string="Recipe Phase")
    
    user_id = fields.Many2one('res.users', string="Triggered By", default=lambda self: self.env.user)
    create_date = fields.Datetime("Timestamp", readonly=True, default=fields.Datetime.now)
