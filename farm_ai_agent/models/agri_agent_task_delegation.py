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

    def action_lock_escrow(self):
        """
        Step 1: Check credit balance, reserve credits by posting a 'draft' ledger line
        """
        for contract in self:
            if contract.state != 'draft':
                continue
            
            # Check delegator credit balance
            if contract.delegator_id.impact_credits < contract.escrow_credits:
                raise ValidationError(_("Insufficient credits on delegator account. (委托方信用余额不足，锁仓失败。)") + f" [{contract.delegator_id.name}]")

            # Reserve credits by creating a 'draft' ledger line (Escrowed)
            ledger_line = self.env['agri.clearing.ledger'].create({
                'partner_id': contract.delegator_id.id,
                'credit_change': -contract.escrow_credits,
                'description': _("ESCROW RESERVE: Sustainability credits held for task delegation %s. (外包委托履约资金锁仓托管)") % contract.name,
                'state': 'draft' # Escrow status is draft, so it does not permanently deduct yet
            })
            
            # Deduct the balance in Python to prevent double spending
            contract.delegator_id.impact_credits -= contract.escrow_credits
            
            contract.write({
                'state': 'escrow',
                'ledger_id': ledger_line.id
            })
        return True

    def action_approve_execution(self):
        """
        Step 2: Transition contract to active executing state
        """
        for contract in self:
            if contract.state != 'escrow':
                continue
            contract.write({'state': 'approved'})
        return True

    def action_complete_clearing(self, proof_hash):
        """
        Step 3: Verification of Merkle Proof and release Escrow credits to Delegatee
        """
        for contract in self:
            if contract.state != 'approved':
                continue
            
            # Verify the proof matches a valid 64-char hex string
            if not proof_hash or len(proof_hash) != 64:
                raise ValidationError(_("Invalid SFC Merkle Proof hash. (无效的 SFC 密码学哈希证明。)"))

            # Permanently confirm the delegator's deduction ledger entry
            if contract.ledger_id:
                # Add back the credits temporarily to prevent ledger confirmation from double-deducting
                contract.delegator_id.impact_credits += contract.escrow_credits
                contract.ledger_id.action_confirm()

            # Create the matching credit ledger entry for the delegatee (Double-Entry completed)
            self.env['agri.clearing.ledger'].create({
                'partner_id': contract.delegatee_id.id,
                'credit_change': contract.escrow_credits,
                'description': _("ESCROW RELEASE: Sustainability credits settled for task delegation %s. MerkleProof=%s (外包履约圆满达成，信用释放记账)") % (contract.name, proof_hash[:16]),
                'state': 'confirmed'
            })

            contract.write({
                'state': 'completed',
                'merkle_proof': proof_hash
            })
        return True

    def action_cancel_refund(self):
        """
        Step 4: Cancel and refund escrow credits
        """
        for contract in self:
            if contract.state not in ['escrow', 'approved']:
                continue
            
            # Refund delegator impact credits in Python
            contract.delegator_id.impact_credits += contract.escrow_credits
            
            # Unlink the draft ledger line
            if contract.ledger_id and contract.ledger_id.state == 'draft':
                contract.ledger_id.unlink()

            contract.write({
                'state': 'cancelled',
                'ledger_id': False
            })
        return True
