from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class DividendDistribution(models.Model):
    """
    分红分配 [US-042-06]
    """
    _name = 'dividend.distribution'
    _description = 'Dividend Distribution'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Distribution Name', required=True)
    cooperative_id = fields.Many2one('cooperative.entity', string='Cooperative', required=True)
    distribution_date = fields.Date('Distribution Date', default=fields.Date.context_today, required=True)
    total_dividend_amount = fields.Float('Total Dividend Amount', required=True)
    dividend_per_share = fields.Float('Dividend per Share', compute='_compute_dividend_per_share', store=True, precompute=True)
    distribution_type = fields.Selection([
        ('cash', 'Cash Dividend'),
        ('stock', 'Stock Dividend'),
        ('hybrid', 'Hybrid (Cash + Stock)'),
    ], string='Distribution Type', default='cash', required=True)
    trading_volume_ratio = fields.Float('Trading Volume Ratio', default=0.5,
                                       help='Proportion of dividend based on trading volume')
    share_ratio = fields.Float('Share Ratio', default=0.5,
                              help='Proportion of dividend based on shares held')
    description = fields.Text('Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('calculated', 'Calculated'),
        ('distributed', 'Distributed'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', required=True)

    dividend_lines = fields.One2many('dividend.line', 'distribution_id', string='Dividend Lines')

    @api.depends('total_dividend_amount')
    def _compute_dividend_per_share(self):
        for record in self:
            total_shares = sum(member.shares_held for member in record.env['cooperative.member'].search([('cooperative_id', '=', record.cooperative_id.id)]))
            if total_shares > 0:
                record.dividend_per_share = record.total_dividend_amount / total_shares
            else:
                record.dividend_per_share = 0.0

    def action_calculate_dividends(self):
        """计算分红"""
        DividendLine = self.env['dividend.line']
        for distribution in self:
            # Clear existing lines
            distribution.dividend_lines.unlink()

            # Calculate dividends for each member
            for member in distribution.env['cooperative.member'].search([('cooperative_id', '=', distribution.cooperative_id.id)]):
                if not member.dividend_eligibility:
                    continue

                # Calculate based on shares and trading volume
                share_based_amount = member.shares_held * distribution.dividend_per_share * distribution.share_ratio
                trading_based_amount = member.trading_volume * distribution.total_dividend_amount * distribution.trading_volume_ratio

                total_amount = share_based_amount + trading_based_amount

                DividendLine.create({
                    'distribution_id': distribution.id,
                    'member_id': member.id,
                    'share_based_amount': share_based_amount,
                    'trading_based_amount': trading_based_amount,
                    'total_amount': total_amount,
                })

            distribution.state = 'calculated'

    def action_distribute_dividends(self):
        """分配分红"""
        for distribution in self:
            if distribution.state != 'calculated':
                continue
            distribution.state = 'distributed'