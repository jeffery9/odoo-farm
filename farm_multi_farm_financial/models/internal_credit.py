from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class InternalCredit(models.Model):
    """
    内部信用额度管理 [US-19-07]
    """
    _name = 'internal.credit'
    _description = 'Internal Credit'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Credit Reference', required=True, default=lambda self: _('New'))
    member_id = fields.Many2one('cooperative.member', string='Member', required=True)
    cooperative_id = fields.Many2one("cooperative.entity", string="Cooperative", required=True)
    credit_limit = fields.Float('Credit Limit', required=True)
    utilized_amount = fields.Float('Utilized Amount', default=0.0)
    available_amount = fields.Float('Available Amount', compute='_compute_available_amount', store=True)
    start_date = fields.Date('Start Date', default=fields.Date.context_today)
    end_date = fields.Date('End Date')
    interest_rate = fields.Float('Interest Rate (%)', default=0.0)
    grace_period_days = fields.Integer('Grace Period (Days)', default=0)
    description = fields.Text('Description')
    state = fields.Selection([
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('suspended', 'Suspended'),
        ('closed', 'Closed'),
    ], string='State', default='active', required=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('internal.credit') or '/'
        return super().create(vals)

    @api.depends('credit_limit', 'utilized_amount')
    def _compute_available_amount(self):
        for record in self:
            record.available_amount = record.credit_limit - record.utilized_amount

    @api.constrains('credit_limit', 'utilized_amount')
    def _check_credit_limit(self):
        for record in self:
            if record.utilized_amount > record.credit_limit:
                raise ValidationError(_('Utilized amount cannot exceed credit limit.'))

    def action_increase_credit_limit(self):
        """增加信用额度"""
        # Wizard or form would be used to specify new limit
        pass

    def action_close_credit(self):
        """关闭信用额度"""
        for credit in self:
            if credit.utilized_amount > 0:
                raise ValidationError(_('Cannot close credit with outstanding balance.'))
            credit.state = 'closed'