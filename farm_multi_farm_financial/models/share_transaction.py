from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class ShareTransaction(models.Model):
    """
    股份交易记录 [US-042-06]
    """
    _name = 'share.transaction'
    _description = 'Share Transaction'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'transaction_date desc'

    name = fields.Char('Transaction Reference', required=True, default=lambda self: _('New'))
    member_id = fields.Many2one('cooperative.member', string='Member', required=True)
    transaction_type = fields.Selection([
        ('subscription', 'Subscription'),
        ('transfer_in', 'Transfer In'),
        ('transfer_out', 'Transfer Out'),
        ('redemption', 'Redemption'),
        ('bonus', 'Bonus Share'),
    ], string='Transaction Type', required=True)
    shares_count = fields.Float('Shares Count', required=True)
    share_price = fields.Float('Share Price', help='Price per share at transaction time')
    total_amount = fields.Float('Total Amount', compute='_compute_total_amount', store=True)
    transaction_date = fields.Date('Transaction Date', default=fields.Date.context_today, required=True)
    description = fields.Text('Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', required=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('share.transaction') or '/'
        return super().create(vals)

    @api.depends('shares_count', 'share_price')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = record.shares_count * record.share_price

    def action_confirm(self):
        """确认股份交易"""
        for transaction in self:
            if transaction.state != 'draft':
                continue
            # Update member's share count
            if transaction.transaction_type in ['subscription', 'transfer_in', 'bonus']:
                transaction.member_id.shares_held += transaction.shares_count
            elif transaction.transaction_type in ['redemption', 'transfer_out']:
                if transaction.member_id.shares_held < transaction.shares_count:
                    raise ValidationError(_('Insufficient shares to redeem/transfer'))
                transaction.member_id.shares_held -= transaction.shares_count
            transaction.state = 'confirmed'

    def action_cancel(self):
        """取消股份交易"""
        for transaction in self:
            if transaction.state != 'confirmed':
                continue
            # Reverse the transaction
            if transaction.transaction_type in ['subscription', 'transfer_in', 'bonus']:
                transaction.member_id.shares_held -= transaction.shares_count
            elif transaction.transaction_type in ['redemption', 'transfer_out']:
                transaction.member_id.shares_held += transaction.shares_count
            transaction.state = 'cancelled'