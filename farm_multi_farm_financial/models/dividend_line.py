from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class DividendLine(models.Model):
    """
    分红明细 [US-19-06]
    """
    _name = 'dividend.line'
    _description = 'Dividend Distribution Line'

    distribution_id = fields.Many2one('dividend.distribution', string='Distribution', required=True, ondelete='cascade')
    member_id = fields.Many2one('cooperative.member', string='Member', required=True)
    share_based_amount = fields.Float('Share-based Amount')
    trading_based_amount = fields.Float('Trading-based Amount')
    total_amount = fields.Float('Total Amount', required=True)
    paid_amount = fields.Float('Paid Amount', default=0.0)
    paid_date = fields.Date('Paid Date')
    state = fields.Selection([
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='pending')

    @api.depends('paid_amount', 'total_amount')
    def _compute_state(self):
        for record in self:
            if record.paid_amount >= record.total_amount and record.total_amount > 0:
                record.state = 'paid'
            elif record.paid_amount > 0:
                record.state = 'partial'
            else:
                record.state = 'pending'

    def action_mark_as_paid(self):
        """Mark dividend line as paid"""
        for line in self:
            line.write({
                'paid_amount': line.total_amount,
                'paid_date': fields.Date.context_today(line),
            })

    def action_pay_partial(self, amount):
        """Record partial payment for dividend line"""
        for line in self:
            if amount <= 0:
                raise ValidationError(_("Payment amount must be positive"))
            new_paid_amount = line.paid_amount + amount
            if new_paid_amount > line.total_amount:
                raise ValidationError(_("Payment amount exceeds total dividend amount"))
            line.write({
                'paid_amount': new_paid_amount,
                'paid_date': fields.Date.context_today(line),
            })