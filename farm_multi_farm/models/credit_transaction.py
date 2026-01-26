from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class CreditTransaction(models.Model):
    """
    信用交易记录 [US-19-07]
    """
    _name = 'credit.transaction'
    _description = 'Credit Transaction'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'transaction_date desc'

    name = fields.Char('Transaction Reference', required=True, default=lambda self: _('New'))
    member_id = fields.Many2one('cooperative.member', string='Member', required=True)
    credit_line_id = fields.Many2one('internal.credit', string='Credit Line', required=True)
    transaction_type = fields.Selection([
        ('usage', 'Usage'),
        ('repayment', 'Repayment'),
        ('interest', 'Interest Charge'),
    ], string='Transaction Type', required=True)
    amount = fields.Float('Amount', required=True)
    transaction_date = fields.Date('Transaction Date', default=fields.Date.context_today, required=True)
    description = fields.Text('Description')
    related_document = fields.Reference([
        ('stock.picking', 'Stock Picking'),
        ('purchase.order', 'Purchase Order'),
        ('account.move', 'Account Move'),
    ], string='Related Document')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('reversed', 'Reversed'),
    ], string='State', default='draft', required=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('credit.transaction') or '/'
        return super().create(vals)

    def action_confirm(self):
        """确认信用交易"""
        for transaction in self:
            if transaction.state != 'draft':
                continue

            credit_line = transaction.credit_line_id
            if transaction.transaction_type == 'usage':
                # Increase utilized amount
                new_utilized = credit_line.utilized_amount + transaction.amount
                if new_utilized > credit_line.credit_limit:
                    # Check if we need approval for exceeding limit
                    # In real implementation, this could trigger an approval flow
                    raise ValidationError(_('Credit transaction would exceed limit. Approval required.'))
                credit_line.utilized_amount = new_utilized
            elif transaction.transaction_type == 'repayment':
                # Decrease utilized amount
                new_utilized = max(0, credit_line.utilized_amount - transaction.amount)
                credit_line.utilized_amount = new_utilized
            elif transaction.transaction_type == 'interest':
                # Interest charges increase the utilized amount
                credit_line.utilized_amount += transaction.amount

            transaction.state = 'confirmed'

    def action_reverse(self):
        """冲销信用交易"""
        for transaction in self:
            if transaction.state != 'confirmed':
                continue

            credit_line = transaction.credit_line_id
            if transaction.transaction_type == 'usage':
                # Reverse usage by decreasing utilized amount
                new_utilized = max(0, credit_line.utilized_amount - transaction.amount)
                credit_line.utilized_amount = new_utilized
            elif transaction.transaction_type == 'repayment':
                # Reverse repayment by increasing utilized amount
                new_utilized = credit_line.utilized_amount + transaction.amount
                credit_line.utilized_amount = new_utilized
            elif transaction.transaction_type == 'interest':
                # Reverse interest by decreasing utilized amount
                new_utilized = max(0, credit_line.utilized_amount - transaction.amount)
                credit_line.utilized_amount = new_utilized

            transaction.state = 'reversed'