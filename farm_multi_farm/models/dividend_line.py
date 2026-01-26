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

    @api.depends('paid_amount')
    def _compute_paid_status(self):
        for record in self:
            if record.paid_amount >= record.total_amount:
                record.state = 'paid'
            elif record.paid_amount > 0:
                record.state = 'partial'
            else:
                record.state = 'pending'