from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class ContractFarmingAgreement(models.Model):
    """
    Contract Farming Agreement Model
    US-19-24: "Company + Farmer" Contract Farming Management
    """
    _name = 'contract.farming.agreement'
    _description = 'Contract Farming Agreement'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_date desc'

    name = fields.Char('Agreement Reference', required=True, default=lambda self: _('New'))
    company_id = fields.Many2one('res.company', string='Agricultural Enterprise', required=True,
                                default=lambda self: self.env.company)
    farmer_id = fields.Many2one('res.partner', string='Farmer/Contractor', required=True,
                               domain=[('is_company', '=', False), ('supplier', '=', True)])

    # Contract Terms
    crop_type = fields.Many2one('product.category', string='Crop Type',
                               domain=[('parent_id.name', '=', 'Crops')])
    planting_area = fields.Float('Planting Area (mu)', help='Area in mu (Chinese acre)')
    planting_date = fields.Date('Expected Planting Date')
    harvest_date = fields.Date('Expected Harvest Date')
    quality_standards = fields.Text('Quality Standards & Specifications')

    # Financial Terms
    pricing_method = fields.Selection([
        ('fixed', 'Fixed Price'),
        ('market', 'Market-Based Price'),
        ('cost_plus', 'Cost Plus'),
        ('revenue_share', 'Revenue Sharing'),
    ], string='Pricing Method', default='fixed', required=True)

    fixed_price = fields.Float('Fixed Price (per kg)', digits=(16, 2))
    cost_plus_margin = fields.Float('Cost Plus Margin (%)', default=10.0)
    revenue_share_percentage = fields.Float('Revenue Share (%)', default=50.0)

    # Input Prepayment Management
    input_prepayment_total = fields.Monetary('Total Input Prepayment',
                                            currency_field='currency_id',
                                            compute='_compute_input_prepayment_total', store=True)
    input_prepayment_paid = fields.Monetary('Input Prepayment Paid',
                                           currency_field='currency_id',
                                           compute='_compute_input_prepayment_paid', store=True)
    input_prepayment_remaining = fields.Monetary('Input Prepayment Remaining',
                                                currency_field='currency_id',
                                                compute='_compute_input_prepayment_remaining', store=True)

    # Yield Commitment
    yield_commitment = fields.Float('Yield Commitment (kg/mu)', help='Expected yield per mu')
    actual_yield = fields.Float('Actual Yield (kg)', compute='_compute_actual_yield', store=True)
    yield_performance = fields.Float('Yield Performance (%)',
                                    compute='_compute_yield_performance', store=True)

    # Financial Settlement
    projected_revenue = fields.Monetary('Projected Revenue',
                                       currency_field='currency_id',
                                       compute='_compute_projected_revenue', store=True)
    actual_revenue = fields.Monetary('Actual Revenue',
                                    currency_field='currency_id',
                                    compute='_compute_actual_revenue', store=True)
    settlement_amount = fields.Monetary('Settlement Amount',
                                       currency_field='currency_id',
                                       compute='_compute_settlement_amount', store=True)

    # Contract Management
    start_date = fields.Date('Contract Start Date', required=True)
    end_date = fields.Date('Contract End Date', required=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)

    # Input prepayments
    input_prepayment_ids = fields.One2many('contract.farming.input.prepayment', 'agreement_id',
                                          string='Input Prepayments')

    # Yield and harvest tracking
    yield_commitment_ids = fields.One2many('contract.farming.yield.commitment', 'agreement_id',
                                          string='Yield Commitments')

    # Settlement records
    settlement_ids = fields.One2many('contract.farming.settlement', 'agreement_id',
                                    string='Settlement Records')

    # State management
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('in_progress', 'In Progress'),
        ('harvest_complete', 'Harvest Complete'),
        ('settled', 'Settled'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True, tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('contract.farming.agreement') or '/'
        return super().create(vals)

    @api.constrains('start_date', 'end_date')
    def _check_date_range(self):
        for record in self:
            if record.start_date and record.end_date and record.start_date > record.end_date:
                raise ValidationError(_('Start date must be earlier than end date.'))

    @api.depends('input_prepayment_ids')
    def _compute_input_prepayment_total(self):
        for record in self:
            record.input_prepayment_total = sum(record.input_prepayment_ids.mapped('amount'))

    @api.depends('input_prepayment_ids.paid_amount')
    def _compute_input_prepayment_paid(self):
        for record in self:
            record.input_prepayment_paid = sum(record.input_prepayment_ids.mapped('paid_amount'))

    @api.depends('input_prepayment_total', 'input_prepayment_paid')
    def _compute_input_prepayment_remaining(self):
        for record in self:
            record.input_prepayment_remaining = record.input_prepayment_total - record.input_prepayment_paid

    @api.depends('yield_commitment_ids.expected_yield', 'yield_commitment_ids.area')
    def _compute_actual_yield(self):
        for record in self:
            # Calculate based on actual harvest records
            actual_yields = record.yield_commitment_ids.mapped('actual_yield')
            record.actual_yield = sum(actual_yields) if actual_yields else 0.0

    @api.depends('yield_commitment', 'actual_yield', 'planting_area')
    def _compute_yield_performance(self):
        for record in self:
            if record.yield_commitment and record.planting_area:
                expected_total = record.yield_commitment * record.planting_area
                if expected_total > 0:
                    record.yield_performance = (record.actual_yield / expected_total) * 100
                else:
                    record.yield_performance = 0.0
            else:
                record.yield_performance = 0.0

    @api.depends('fixed_price', 'actual_yield')
    def _compute_projected_revenue(self):
        for record in self:
            if record.pricing_method == 'fixed':
                record.projected_revenue = record.fixed_price * record.actual_yield
            else:
                # For other pricing methods, would need market price data
                record.projected_revenue = record.fixed_price * record.actual_yield

    @api.depends('settlement_ids.amount')
    def _compute_actual_revenue(self):
        for record in self:
            record.actual_revenue = sum(record.settlement_ids.mapped('amount'))

    @api.depends('actual_revenue', 'input_prepayment_remaining')
    def _compute_settlement_amount(self):
        for record in self:
            # Settlement is revenue minus any remaining prepayments
            record.settlement_amount = record.actual_revenue - record.input_prepayment_remaining

    def action_approve_agreement(self):
        """Approve the contract agreement"""
        for record in self:
            if record.state == 'draft':
                record.state = 'approved'
                record.message_post(body=_("Agreement approved by %s" % self.env.user.name))

    def action_start_farming(self):
        """Mark farming as started"""
        for record in self:
            if record.state == 'approved':
                record.state = 'in_progress'
                record.message_post(body=_("Farming started on %s" % fields.Date.today()))

    def action_complete_harvest(self):
        """Mark harvest as complete"""
        for record in self:
            if record.state == 'in_progress':
                record.state = 'harvest_complete'
                record.message_post(body=_("Harvest completed, ready for settlement"))

    def action_settle_contract(self):
        """Complete settlement of the contract"""
        for record in self:
            if record.state == 'harvest_complete':
                # Calculate final settlement
                total_settled = sum(record.settlement_ids.mapped('amount'))
                remaining = record.settlement_amount - total_settled

                if remaining > 0:
                    # Create final settlement record
                    self.env['contract.farming.settlement'].create({
                        'agreement_id': record.id,
                        'type': 'final',
                        'amount': remaining,
                        'description': 'Final contract settlement'
                    })

                record.state = 'settled'
                record.message_post(body=_("Contract fully settled"))

    def action_cancel_agreement(self):
        """Cancel the agreement"""
        for record in self:
            if record.state in ['draft', 'submitted', 'approved']:
                record.state = 'cancelled'
                record.message_post(body=_("Agreement cancelled by %s" % self.env.user.name))


class ContractFarmingInputPrepayment(models.Model):
    """
    Input Prepayment Management for Contract Farming
    US-19-24: Input prepayment tracking and repayment
    """
    _name = 'contract.farming.input.prepayment'
    _description = 'Contract Farming Input Prepayment'
    _order = 'create_date desc'

    agreement_id = fields.Many2one('contract.farming.agreement', string='Agreement', required=True, ondelete='cascade')
    input_type = fields.Selection([
        ('seed', 'Seed'),
        ('fertilizer', 'Fertilizer'),
        ('pesticide', 'Pesticide'),
        ('equipment', 'Equipment'),
        ('other', 'Other'),
    ], string='Input Type', required=True)

    product_id = fields.Many2one('product.product', string='Input Product',
                                domain=[('categ_id.parent_id.name', 'in', ['Seeds', 'Fertilizers', 'Pesticides'])])
    quantity = fields.Float('Quantity')
    unit_price = fields.Float('Unit Price')
    amount = fields.Monetary('Total Amount', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', related='agreement_id.currency_id')

    # Delivery and verification
    delivery_date = fields.Date('Delivery Date')
    delivered_quantity = fields.Float('Delivered Quantity')
    verification_status = fields.Selection([
        ('pending', 'Pending Delivery'),
        ('delivered', 'Delivered'),
        ('verified', 'Verified Used'),
        ('repaid', 'Repaid'),
    ], string='Verification Status', default='pending')

    # Repayment tracking
    repayment_method = fields.Selection([
        ('harvest_proceeds', 'Harvest Proceeds'),
        ('fixed_schedule', 'Fixed Schedule'),
        ('revenue_sharing', 'Revenue Sharing'),
    ], string='Repayment Method', default='harvest_proceeds')

    repayment_due_date = fields.Date('Repayment Due Date')
    paid_amount = fields.Monetary('Paid Amount', currency_field='currency_id', default=0.0)
    remaining_amount = fields.Monetary('Remaining Amount',
                                      currency_field='currency_id',
                                      compute='_compute_remaining_amount', store=True)

    description = fields.Text('Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('delivered', 'Delivered'),
        ('repaid', 'Repaid'),
    ], string='State', default='draft')

    @api.onchange('product_id', 'quantity')
    def _onchange_product_quantity(self):
        if self.product_id and self.quantity:
            self.unit_price = self.product_id.standard_price
            self.amount = self.unit_price * self.quantity

    @api.depends('amount', 'paid_amount')
    def _compute_remaining_amount(self):
        for record in self:
            record.remaining_amount = record.amount - record.paid_amount

    def action_confirm_delivery(self):
        """Confirm delivery of inputs"""
        for record in self:
            if record.state == 'draft':
                record.state = 'confirmed'
                record.verification_status = 'delivered'
                record.delivery_date = fields.Date.today()
                record.delivered_quantity = record.quantity

    def action_verify_usage(self):
        """Verify that inputs were used"""
        for record in self:
            record.verification_status = 'verified'

    def action_mark_repaid(self, amount=None):
        """Mark as repaid"""
        for record in self:
            pay_amount = amount or record.amount
            if pay_amount > record.remaining_amount:
                raise ValidationError(_('Payment amount exceeds remaining amount'))

            record.paid_amount += pay_amount
            record.verification_status = 'repaid'
            record.state = 'repaid'


class ContractFarmingYieldCommitment(models.Model):
    """
    Yield Commitment and Performance Tracking
    US-19-24: Track yield commitments vs actual performance
    """
    _name = 'contract.farming.yield.commitment'
    _description = 'Contract Farming Yield Commitment'

    agreement_id = fields.Many2one('contract.farming.agreement', string='Agreement', required=True, ondelete='cascade')
    expected_yield = fields.Float('Expected Yield (kg/mu)')
    actual_yield = fields.Float('Actual Yield (kg)', default=0.0)
    area = fields.Float('Area (mu)', help='Area for this specific yield commitment')
    quality_grade = fields.Selection([
        ('premium', 'Premium'),
        ('standard', 'Standard'),
        ('basic', 'Basic'),
    ], string='Quality Grade', default='standard')

    harvest_date = fields.Date('Harvest Date')
    notes = fields.Text('Harvest Notes')

    # Performance metrics
    performance_rate = fields.Float('Performance Rate (%)', compute='_compute_performance_rate', store=True)
    quality_compliance = fields.Boolean('Quality Compliance', compute='_compute_quality_compliance', store=True)

    @api.depends('expected_yield', 'actual_yield', 'area')
    def _compute_performance_rate(self):
        for record in self:
            if record.expected_yield and record.area:
                expected_total = record.expected_yield * record.area
                if expected_total > 0:
                    record.performance_rate = (record.actual_yield / expected_total) * 100
                else:
                    record.performance_rate = 0.0
            else:
                record.performance_rate = 0.0

    def _compute_quality_compliance(self):
        for record in self:
            # This would typically check against quality standards defined in the agreement
            # For now, a basic check based on grade
            record.quality_compliance = record.quality_grade in ['premium', 'standard']


class ContractFarmingSettlement(models.Model):
    """
    Profit Distribution and Settlement System
    US-19-24: Calculate and distribute profits based on contract terms
    """
    _name = 'contract.farming.settlement'
    _description = 'Contract Farming Settlement'
    _order = 'create_date desc'

    agreement_id = fields.Many2one('contract.farming.agreement', string='Agreement', required=True, ondelete='cascade')
    type = fields.Selection([
        ('advance', 'Advance Payment'),
        ('interim', 'Interim Settlement'),
        ('final', 'Final Settlement'),
        ('revenue_share', 'Revenue Share'),
    ], string='Settlement Type', required=True)

    amount = fields.Monetary('Settlement Amount', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', related='agreement_id.currency_id')

    settlement_date = fields.Date('Settlement Date', default=fields.Date.today)
    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('offset', 'Offset Against Prepayment'),
    ], string='Payment Method', default='bank_transfer')

    description = fields.Text('Description')

    # Financial breakdown
    enterprise_share = fields.Monetary('Enterprise Share', currency_field='currency_id', compute='_compute_shares', store=True)
    farmer_share = fields.Monetary('Farmer Share', currency_field='currency_id', compute='_compute_shares', store=True)

    @api.depends('amount', 'agreement_id.revenue_share_percentage')
    def _compute_shares(self):
        for record in self:
            if record.agreement_id.pricing_method == 'revenue_share':
                farmer_percent = record.agreement_id.revenue_share_percentage
                enterprise_percent = 100 - farmer_percent

                record.farmer_share = (record.amount * farmer_percent) / 100
                record.enterprise_share = (record.amount * enterprise_percent) / 100
            else:
                # For other pricing methods, farmer gets the full proceeds after prepayments are recovered
                prepayments_paid = sum(record.agreement_id.input_prepayment_ids.mapped('paid_amount'))
                remaining_from_pre = record.agreement_id.input_prepayment_total - prepayments_paid

                if remaining_from_pre > 0:
                    # Recover remaining prepayments first
                    recovery_amount = min(record.amount, remaining_from_pre)
                    record.enterprise_share = recovery_amount
                    record.farmer_share = max(0, record.amount - recovery_amount)
                else:
                    # All goes to farmer
                    record.farmer_share = record.amount
                    record.enterprise_share = 0.0

    def action_process_settlement(self):
        """Process the settlement payment"""
        for record in self:
            if record.payment_method == 'offset':
                # Offset against prepayment obligations
                prepayments = record.agreement_id.input_prepayment_ids
                remaining_to_pay = record.amount

                for prepay in prepayments:
                    if remaining_to_pay <= 0:
                        break

                    pay_from_this = min(remaining_to_pay, prepay.remaining_amount)
                    prepay.action_mark_repaid(pay_from_this)
                    remaining_to_pay -= pay_from_this

            record.message_post(body=_("Settlement processed: %s %s" % (record.amount, record.currency_id.name)))