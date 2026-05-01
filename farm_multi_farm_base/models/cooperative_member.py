from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class CooperativeMember(models.Model):
    """
    合作社成员 [US-19-06]
    """
    _name = 'cooperative.member'
    _description = 'Cooperative Member'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Member Name', required=True)
    code = fields.Char('Member Code', required=True, copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    cooperative_id = fields.Many2one('cooperative.entity', string='Cooperative', required=True)
    join_date = fields.Date('Join Date', default=fields.Date.context_today)
    membership_status = fields.Selection([
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('withdrawn', 'Withdrawn'),
    ], string='Membership Status', default='active', required=True)
    shares_held = fields.Float('Shares Held', default=0.0)
    share_value = fields.Float('Share Value', compute='_compute_share_value', store=True)
    total_investment = fields.Float('Total Investment', compute='_compute_total_investment', store=True)
    trading_volume = fields.Float('Trading Volume', help='Volume of transactions with cooperative', compute='_compute_trading_volume', store=True)
    dividend_eligibility = fields.Boolean('Eligible for Dividends', default=True)

    # Fields for US-19-07 (Internal Credit)
    credit_limit = fields.Float('Credit Limit', help='Internal credit limit for member')
    credit_used = fields.Float('Credit Used', compute='_compute_credit_usage', store=True)
    available_credit = fields.Float('Available Credit', compute='_compute_available_credit', store=True)

    # Fields for US-19-14 (Treasury Dashboard)
    account_balance = fields.Float('Account Balance', compute='_compute_account_balance', store=True)

    # Fields for US-19-15 (Loans)
    loan_balance = fields.Float('Loan Balance', compute='_compute_loan_balance', store=True)

    @api.model
    def create(self, vals):
        if 'code' not in vals or not vals['code']:
            vals['code'] = self.env['ir.sequence'].next_by_code('cooperative.member') or '/'
        return super().create(vals)

    @api.depends('shares_held')
    def _compute_share_value(self):
        for record in self:
            # Simple calculation - in real implementation this might be based on share price
            record.share_value = record.shares_held * 100.0  # Assuming 100 per share

    @api.depends('share_value')
    def _compute_total_investment(self):
        for record in self:
            # May include other investment types in the future
            record.total_investment = record.share_value

    @api.depends('credit_limit', 'credit_used')
    def _compute_available_credit(self):
        for record in self:
            record.available_credit = record.credit_limit - record.credit_used

    @api.depends('credit_limit', 'credit_used')
    def _compute_credit_usage(self):
        for record in self:
            # Calculate how much credit has been used
            # This would be based on actual credit transactions
            record.credit_used = 0.0  # Placeholder - would need to sum actual credit usage

    @api.depends('account_balance')
    def _compute_account_balance(self):
        for record in self:
            # Would calculate based on cooperative financial records
            record.account_balance = 0.0  # Placeholder

    @api.depends('loan_balance')
    def _compute_loan_balance(self):
        for record in self:
            # Would calculate based on internal loan records
            record.loan_balance = 0.0  # Placeholder

    @api.depends('partner_id')
    def _compute_trading_volume(self):
        """
        Compute trading volume for the member based on their transactions with the cooperative
        US-19-06: Calculate trading volume for dividend distribution
        """
        SaleOrder = self.env['sale.order']
        PurchaseOrder = self.env['purchase.order']

        for record in self:
            total_volume = 0.0

            # Calculate sales (member buying from cooperative) - based on purchase orders
            purchase_orders = PurchaseOrder.search([
                ('partner_id', '=', record.partner_id.id),
                ('state', 'in', ['purchase', 'done'])  # Confirmed purchases
            ])
            for order in purchase_orders:
                total_volume += order.amount_total

            # Calculate purchases (member selling to cooperative) - based on sale orders
            sale_orders = SaleOrder.search([
                ('partner_id', '=', record.partner_id.id),
                ('state', 'in', ['sale', 'done'])  # Confirmed sales
            ])
            for order in sale_orders:
                total_volume += order.amount_total

            record.trading_volume = total_volume

    _partner_cooperative_unique = models.Constraint(
        'unique(partner_id, cooperative_id)',
        'A partner can only be a member of the same cooperative once!'
    )