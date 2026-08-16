# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import hashlib
from datetime import datetime

class AgriAgentToolRequest(models.Model):
    _name = 'agri.agent.tool.request'
    _description = 'GxP AI Agent Tool Request / GxP 智能体工具请求'
    _inherit = ['mail.thread']

    name = fields.Char(string='Request Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    agent_identifier = fields.Char(string='Agent Identifier', required=True, readonly=True, index=True)
    target_action = fields.Char(string='Target Action', required=True, readonly=True)
    payload = fields.Text(string='Execution Payload', required=True, readonly=True)
    risk_tier = fields.Selection([
        ('green', 'Green (Read/Retrieve)'),
        ('yellow', 'Yellow (Low-Risk Config)'),
        ('red', 'Red (Physical/Critical Control)')
    ], string='Risk Tier', required=True, default='green', readonly=True, index=True)
    
    state = fields.Selection([
        ('pending', 'Pending / 待审批'),
        ('approved', 'Approved / 已批准'),
        ('rejected', 'Rejected / 已拒绝'),
        ('executed', 'Executed / 已执行')
    ], string='Status', default='pending', tracking=True, index=True)

    approver_id = fields.Many2one('res.users', string='Approver', readonly=True)
    digital_signature = fields.Char(string='Digital Signature (SHA-256)', readonly=True)
    approval_timestamp = fields.Datetime(string='Approval Timestamp', readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('agri.agent.tool.request') or _('New')
        return super().create(vals_list)

    def action_approve(self):
        """ GxP Human-in-the-loop approval generating an immutable SHA-256 signature """
        if any(req.state != 'pending' for req in self):
            raise ValidationError(_('Only pending requests can be approved. (仅能批准待处理请求。)'))
            
        timestamp = fields.Datetime.now()
        for req in self:
            signature_base = f"{req.id}-{self.env.user.id}-{timestamp}-{req.payload}"
            signature = hashlib.sha256(signature_base.encode('utf-8')).hexdigest()
            
            req.write({
                'state': 'approved',
                'approver_id': self.env.user.id,
                'approval_timestamp': timestamp,
                'digital_signature': signature
            })
            req.message_post(body=_("GxP Request Approved. Signature: %s (GxP 请求已批准。数字签名：%s)") % (signature, signature))

    def action_reject(self):
        if any(req.state != 'pending' for req in self):
            raise ValidationError(_('Only pending requests can be rejected. (仅能拒绝待处理请求。)'))
        self.write({'state': 'rejected'})
        for req in self:
            req.message_post(body=_("GxP Request Rejected by operator. (GxP 请求已被操作员拒绝。)"))
