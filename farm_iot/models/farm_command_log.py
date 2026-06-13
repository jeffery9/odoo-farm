# -*- coding: utf-8 -*-
from odoo import models, fields, api

class FarmCommandLog(models.Model):
    """ [US-047-04] 管理中心：通用物联命令审计中心 """
    _name = 'farm.command.log'
    _description = 'Global IoT Command Audit Log'
    _order = 'create_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    device_id = fields.Many2one('iiot.device', string="Target Device", required=True)
    command = fields.Char("Action/Command", required=True)
    payload = fields.Text("Payload (JSON)")
    
    # 核心状态生命周期
    status = fields.Selection([
        ('draft', 'Draft'),
        ('dispatched', 'Dispatched to Framework'),
        ('ack', 'Edge Acknowledged'),
        ('success', 'Execution Success'),
        ('failed', 'Execution Failed'),
        ('timeout', 'Response Timeout')
    ], default='dispatched', string="Status", tracking=True)
    
    execution_latency = fields.Integer("Latency (ms)")
    error_log = fields.Text("Error Traceback")
    
    # 响应追踪 [US-TECH-05-01]
    ack_timestamp = fields.Datetime("ACK Timestamp")
    retry_count = fields.Integer("Retries", default=0)
    max_retries = fields.Integer("Max Retries", default=3)
    
    # 通用关联 (不绑定特定业务模块)
    res_model = fields.Char("Originating Model")
    res_id = fields.Integer("Originating ID")
    
    user_id = fields.Many2one('res.users', string="Operator", default=lambda self: self.env.user)
    create_date = fields.Datetime("Timestamp", readonly=True, default=fields.Datetime.now)
