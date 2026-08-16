# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AgriAgentTaskDelegation(models.Model):
    """
    Multi-Agent Task Delegation and Escrow Clearing Contract (智能体任务委派与托管清算合同)
    Think in Odoo: Leveraging native document lifecycle and ledger states.
    """
    _name = 'agri.agent.task.delegation'
    _description = 'Agricultural Agent Task Delegation'
    _inherit = ['mail.thread']

    name = fields.Char("Contract Reference (合同编号)", required=True, copy=False, readonly=True, default=lambda self: _('New'))
    
    # Linked Odoo Tasks (Single execution truth via project.task delegate)
    parent_task_id = fields.Many2one('farm.task', string="Parent Task (主任务)", required=True, ondelete='restrict')
    sub_task_id = fields.Many2one('farm.task', string="Subcontracted Task (外包子任务)", required=True, ondelete='restrict')

    # Counterparties (Odoo Partners)
    delegator_id = fields.Many2one('res.partner', string="Delegator Owner (委托方智能体)", required=True, index=True)
    delegatee_id = fields.Many2one('res.partner', string="Delegatee Owner (受托方智能体)", required=True, index=True)

    # Multi-Company Context Isolation
    delegator_company_id = fields.Many2one('res.company', string="Delegator Company", related='parent_task_id.company_id', store=True)
    delegatee_company_id = fields.Many2one('res.company', string="Delegatee Company", related='sub_task_id.company_id', store=True)

    # Escrow Value and Cleared State
    escrow_credits = fields.Float("Escrow Credits (锁仓额度)", required=True, default=0.0)
    merkle_proof = fields.Char("SFC Merkle Verification Proof (密码学履约证明)", readonly=True)

    # Lifecycle State Machine
    state = fields.Selection([
        ('draft', 'Draft (草拟)'),
        ('escrow', 'Escrow Locked (信用资金锁仓托管)'),
        ('approved', 'Approved / Executing (已批准执行)'),
        ('completed', 'Completed & Cleared (已履约清算)'),
        ('cancelled', 'Cancelled & Refunded (已撤销退款)')
    ], default='draft', tracking=True, string="Contract State")

    # Link to the Escrow double-entry Ledger Line
    ledger_id = fields.Many2one('agri.clearing.ledger', string="Escrow Ledger Line", readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('agri.agent.task.delegation') or '/'
        return super(AgriAgentTaskDelegation, self).create(vals_list)
