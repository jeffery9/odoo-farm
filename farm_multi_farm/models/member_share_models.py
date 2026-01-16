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
    trading_volume = fields.Float('Trading Volume', help='Volume of transactions with cooperative')
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


class ShareTransaction(models.Model):
    """
    股份交易记录 [US-19-06]
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


class DividendDistribution(models.Model):
    """
    分红分配 [US-19-06]
    """
    _name = 'dividend.distribution'
    _description = 'Dividend Distribution'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Distribution Name', required=True)
    cooperative_id = fields.Many2one('cooperative.entity', string='Cooperative', required=True)
    distribution_date = fields.Date('Distribution Date', default=fields.Date.context_today, required=True)
    total_dividend_amount = fields.Float('Total Dividend Amount', required=True)
    dividend_per_share = fields.Float('Dividend per Share', compute='_compute_dividend_per_share', store=True)
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
            total_shares = sum(member.shares_held for member in record.cooperative_id.member_farm_ids.mapped('cooperative_member_ids'))
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
            for member in distribution.cooperative_id.member_farm_ids.mapped('cooperative_member_ids'):
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


class InternalCredit(models.Model):
    """
    内部信用额度管理 [US-19-07]
    """
    _name = 'internal.credit'
    _description = 'Internal Credit'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Credit Reference', required=True, default=lambda self: _('New'))
    member_id = fields.Many2one('cooperative.member', string='Member', required=True)
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


class SharedMachineryPool(models.Model):
    """
    共享农机池 [US-19-08]
    """
    _name = 'shared.machinery.pool'
    _description = 'Shared Machinery Pool'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Machinery Name', required=True)
    code = fields.Char('Machinery Code', required=True, copy=False)
    cooperative_id = fields.Many2one('cooperative.entity', string='Cooperative', required=True)
    owner_member_id = fields.Many2one('cooperative.member', string='Owner Member', required=True)
    equipment_id = fields.Many2one('fleet.vehicle', string='Equipment', required=True)
    hourly_rate = fields.Float('Hourly Rate')
    daily_rate = fields.Float('Daily Rate')
    availability_status = fields.Selection([
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('maintenance', 'Under Maintenance'),
        ('out_of_service', 'Out of Service'),
    ], string='Availability Status', default='available', required=True)
    location = fields.Char('Current Location')
    description = fields.Text('Description')
    is_active = fields.Boolean('Is Active', default=True)

    @api.model
    def create(self, vals):
        if 'code' not in vals or not vals['code']:
            vals['code'] = self.env['ir.sequence'].next_by_code('shared.machinery.pool') or '/'
        return super().create(vals)

    def action_set_available(self):
        """设置为可用"""
        self.availability_status = 'available'

    def action_set_in_use(self):
        """设置为使用中"""
        self.availability_status = 'in_use'

    def action_set_maintenance(self):
        """设置为维护中"""
        self.availability_status = 'maintenance'

    def action_set_out_of_service(self):
        """设置为停用"""
        self.availability_status = 'out_of_service'


class MachineryRental(models.Model):
    """
    机具租赁记录 [US-19-08]
    """
    _name = 'machinery.rental'
    _description = 'Machinery Rental'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Rental Reference', required=True, default=lambda self: _('New'))
    machinery_id = fields.Many2one('shared.machinery.pool', string='Machinery', required=True)
    renter_member_id = fields.Many2one('cooperative.member', string='Renter Member', required=True)
    start_date = fields.Datetime('Start Date', required=True)
    end_date = fields.Datetime('End Date', required=True)
    actual_end_date = fields.Datetime('Actual End Date')
    rental_type = fields.Selection([
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('area_based', 'Area-based'),
        ('task_based', 'Task-based'),
    ], string='Rental Type', default='hourly', required=True)
    expected_cost = fields.Float('Expected Cost', compute='_compute_expected_cost', store=True)
    actual_cost = fields.Float('Actual Cost', default=0.0)
    settlement_id = fields.Many2one('internal.settlement', string='Settlement')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', required=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('machinery.rental') or '/'
        return super().create(vals)

    @api.depends('start_date', 'end_date', 'rental_type', 'machinery_id')
    def _compute_expected_cost(self):
        for record in self:
            if not record.start_date or not record.end_date:
                record.expected_cost = 0.0
                continue

            machinery = record.machinery_id
            duration = 0.0
            if record.rental_type == 'hourly':
                diff = fields.Datetime.from_string(record.end_date) - fields.Datetime.from_string(record.start_date)
                duration = diff.total_seconds() / 3600.0
                record.expected_cost = duration * machinery.hourly_rate
            elif record.rental_type == 'daily':
                from datetime import datetime
                start = fields.Date.from_string(str(record.start_date)[:10])
                end = fields.Date.from_string(str(record.end_date)[:10])
                duration = (end - start).days + 1
                record.expected_cost = duration * machinery.daily_rate
            else:
                record.expected_cost = 0.0  # Other types need different calculation

    def action_confirm(self):
        """确认租赁"""
        for rental in self:
            if rental.state == 'draft':
                rental.state = 'confirmed'
                # Update machinery status to in_use
                rental.machinery_id.availability_status = 'in_use'

    def action_start_rental(self):
        """开始租赁"""
        for rental in self:
            if rental.state == 'confirmed':
                rental.state = 'in_progress'
                rental.machinery_id.availability_status = 'in_use'

    def action_complete_rental(self):
        """完成租赁"""
        for rental in self:
                rental.state = 'completed'
                rental.actual_end_date = fields.Datetime.now()
                rental.machinery_id.availability_status = 'available'

                # Create internal settlement for the rental
                settlement = self.env['internal.settlement'].create({
                    'from_entity_id': rental.renter_member_id.partner_id.company_id.id,
                    'to_entity_id': rental.machinery_id.owner_member_id.partner_id.company_id.id,
                    'settlement_type': 'resource_rental',
                    'resource_sharing_id': False,  # This is machinery rental, not resource sharing
                    'amount': rental.actual_cost or rental.expected_cost,
                    'description': f'Machinery rental for {rental.machinery_id.name}',
                })
                rental.settlement_id = settlement.id