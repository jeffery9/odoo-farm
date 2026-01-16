from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class CooperativeTreasury(models.Model):
    """
    合作社资金池 [US-19-14]
    """
    _name = 'cooperative.treasury'
    _description = 'Cooperative Treasury'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Treasury Name', required=True)
    cooperative_id = fields.Many2one('cooperative.entity', string='Cooperative', required=True)
    current_balance = fields.Float('Current Balance', compute='_compute_current_balance', store=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    description = fields.Text('Description')

    @api.depends()
    def _compute_current_balance(self):
        # This would aggregate all member account balances
        for treasury in self:
            treasury.current_balance = 0.0  # Placeholder calculation

    def action_view_cash_flow_projection(self):
        """查看现金流预测"""
        # This would show cash flow projections
        pass


class InternalLoan(models.Model):
    """
    内部头寸拆借 [US-19-15]
    """
    _name = 'internal.loan'
    _description = 'Internal Loan'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Loan Reference', required=True, default=lambda self: _('New'))
    cooperative_id = fields.Many2one('cooperative.entity', string='Cooperative', required=True)
    borrower_member_id = fields.Many2one('cooperative.member', string='Borrower Member', required=True)
    lender_member_id = fields.Many2one('cooperative.member', string='Lender Member', required=True)
    loan_amount = fields.Float('Loan Amount', required=True)
    interest_rate = fields.Float('Interest Rate (%)', required=True)
    loan_date = fields.Date('Loan Date', default=fields.Date.context_today, required=True)
    maturity_date = fields.Date('Maturity Date', required=True)
    repayment_schedule = fields.Selection([
        ('bullet', 'Bullet Payment'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annual', 'Annual'),
    ], string='Repayment Schedule', default='bullet')
    description = fields.Text('Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('disbursed', 'Disbursed'),
        ('repaid', 'Repaid'),
        ('defaulted', 'Defaulted'),
    ], string='State', default='draft', required=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('internal.loan') or '/'
        return super().create(vals)

    @api.constrains('loan_amount')
    def _check_loan_amount(self):
        for record in self:
            if record.loan_amount <= 0:
                raise ValidationError(_('Loan amount must be positive.'))

    def action_approve(self):
        """批准贷款"""
        for loan in self:
            loan.state = 'approved'

    def action_disburse(self):
        """发放贷款"""
        for loan in self:
            if loan.state == 'approved':
                loan.state = 'disbursed'

    def action_repay(self):
        """还款"""
        for loan in self:
            loan.state = 'repaid'


class SubsidyDisbursement(models.Model):
    """
    政策性补贴下拨 [US-19-16]
    """
    _name = 'subsidy.disbursement'
    _description = 'Subsidy Disbursement'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Subsidy Name', required=True)
    cooperative_id = fields.Many2one('cooperative.entity', string='Cooperative', required=True)
    subsidy_source = fields.Char('Subsidy Source', required=True)
    total_amount = fields.Float('Total Subsidy Amount', required=True)
    disbursement_date = fields.Date('Disbursement Date', default=fields.Date.context_today)
    description = fields.Text('Description')
    state = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('distributed', 'Distributed'),
        ('completed', 'Completed'),
    ], string='State', default='pending', required=True)

    disbursement_lines = fields.One2many('subsidy.disbursement.line', 'disbursement_id', string='Disbursement Lines')


class SubsidyDisbursementLine(models.Model):
    """
    补贴下拨明细 [US-19-16]
    """
    _name = 'subsidy.disbursement.line'
    _description = 'Subsidy Disbursement Line'

    disbursement_id = fields.Many2one('subsidy.disbursement', string='Disbursement', required=True, ondelete='cascade')
    member_id = fields.Many2one('cooperative.member', string='Member', required=True)
    amount = fields.Float('Amount', required=True)
    basis_for_allocation = fields.Char('Basis for Allocation', help='E.g., certified area, production volume')
    description = fields.Text('Description')
    receipt_date = fields.Date('Receipt Date')
    receipt_confirmed = fields.Boolean('Receipt Confirmed', default=False)


class CooperativeDecision(models.Model):
    """
    三会决策记录 [US-19-17]
    """
    _name = 'cooperative.decision'
    _description = 'Cooperative Decision'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Decision Title', required=True)
    decision_type = fields.Selection([
        ('board', 'Board Meeting'),
        ('general_assembly', 'General Assembly'),
        ('supervisory', 'Supervisory Committee'),
        ('other', 'Other'),
    ], string='Decision Type', required=True)
    cooperative_id = fields.Many2one('cooperative.entity', string='Cooperative', required=True)
    meeting_date = fields.Date('Meeting Date', default=fields.Date.context_today, required=True)
    attendees_count = fields.Integer('Number of Attendees', required=True)
    total_members_count = fields.Integer('Total Members', required=True)
    voting_result = fields.Selection([
        ('passed', 'Passed'),
        ('rejected', 'Rejected'),
        ('postponed', 'Postponed'),
    ], string='Voting Result', required=True)
    required_majority = fields.Float('Required Majority (%)', help='Percentage needed for decision to pass')
    actual_majority = fields.Float('Actual Majority (%)', help='Percentage that voted in favor')
    description = fields.Text('Decision Description')
    resolution_text = fields.Text('Resolution Text', required=True)
    attachments = fields.Binary('Attachments', help='Meeting minutes, photos, etc.')
    attachment_name = fields.Char('Attachment Name')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('executed', 'Executed'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', required=True)

    def action_confirm(self):
        """确认决策"""
        for decision in self:
            decision.state = 'confirmed'

    def action_execute(self):
        """执行决策"""
        for decision in self:
            decision.state = 'executed'


class MultiSignProcess(models.Model):
    """
    分布式联签流程 [US-19-18]
    """
    _name = 'multi.sign.process'
    _description = 'Multi-sign Process'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Process Title', required=True)
    process_type = fields.Selection([
        ('asset_disposal', 'Asset Disposal'),
        ('large_purchase', 'Large Purchase'),
        ('bylaw_change', 'Bylaw Change'),
        ('loan_guarantee', 'Loan Guarantee'),
        ('other', 'Other'),
    ], string='Process Type', required=True)
    cooperative_id = fields.Many2one('cooperative.entity', string='Cooperative', required=True)
    initiator_id = fields.Many2one('cooperative.member', string='Initiator', required=True)
    required_signers = fields.Integer('Required Signers', required=True)
    description = fields.Text('Process Description')
    document_reference = fields.Reference([
        ('account.asset', 'Asset'),
        ('purchase.order', 'Purchase Order'),
        ('cooperative.decision', 'Decision'),
        ('internal.loan', 'Internal Loan'),
    ], string='Related Document')
    state = fields.Selection([
        ('initiated', 'Initiated'),
        ('in_progress', 'In Progress'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='initiated', required=True)

    sign_lines = fields.One2many('multi.sign.line', 'process_id', string='Sign Lines')


class MultiSignLine(models.Model):
    """
    联签明细 [US-19-18]
    """
    _name = 'multi.sign.line'
    _description = 'Multi-sign Line'

    process_id = fields.Many2one('multi.sign.process', string='Process', required=True, ondelete='cascade')
    signer_member_id = fields.Many2one('cooperative.member', string='Signer', required=True)
    signature_date = fields.Date('Signature Date')
    approval_status = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Status', default='pending')
    comments = fields.Text('Comments')
    is_completed = fields.Boolean('Is Completed', default=False)


class DecisionAudit(models.Model):
    """
    决策效力审计 [US-19-19]
    """
    _name = 'decision.audit'
    _description = 'Decision Audit'

    decision_id = fields.Many2one('cooperative.decision', string='Decision', required=True)
    related_document = fields.Reference([
        ('purchase.order', 'Purchase Order'),
        ('sale.order', 'Sale Order'),
        ('account.asset', 'Asset'),
        ('contract.contract', 'Contract'),
        ('internal.loan', 'Internal Loan'),
    ], string='Related Document', required=True)
    audit_result = fields.Selection([
        ('authorized', 'Authorized'),
        ('unauthorized', 'Unauthorized'),
        ('requires_review', 'Requires Review'),
    ], string='Audit Result', required=True)
    audit_date = fields.Date('Audit Date', default=fields.Date.context_today)
    audit_notes = fields.Text('Audit Notes')
    compliance_status = fields.Boolean('Compliance Status', compute='_compute_compliance', store=True)

    @api.depends('audit_result')
    def _compute_compliance(self):
        for record in self:
            record.compliance_status = (record.audit_result == 'authorized')