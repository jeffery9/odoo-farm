from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import random

class InputFinancing(models.Model):
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id)
    """
    Input Financing functionality integrated into farm_finance_loan
    """
    _name = 'farm.input.financing'
    _description = 'Input Financing'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Financing Reference', required=True)
    partner_id = fields.Many2one('res.partner', string='Farmer', required=True)
    input_type = fields.Selection([
        ('seed', 'Seed'),
        ('fertilizer', 'Fertilizer'),
        ('pesticide', 'Pesticide'),
        ('equipment', 'Equipment'),
        ('fuel', 'Fuel'),
        ('feed', 'Feed'),
    ], string='Input Type', required=True)
    product_id = fields.Many2one('product.template', string='Input Product')
    supplier_id = fields.Many2one('res.partner', string='Supplier')

    # Input details
    quantity = fields.Float('Quantity')
    unit_price = fields.Float('Unit Price')
    total_amount = fields.Monetary('Total Amount', currency_field='currency_id', compute='_compute_total_amount', store=True, precompute=True)

    # Financial terms
    amount_financed = fields.Monetary('Amount Financed', currency_field='currency_id')
    interest_rate = fields.Float('Interest Rate (%)', default=7.0, digits=(16, 2))
    service_fees = fields.Monetary('Service Fees', currency_field='currency_id')
    duration_months = fields.Integer('Duration (months)', default=12)

    # Repayment
    repayment_method = fields.Selection([
        ('harvest_proceeds', 'Harvest Proceeds'),
        ('fixed_schedule', 'Fixed Schedule'),
        ('revenue_sharing', 'Revenue Sharing'),
    ], string='Repayment Method', default='harvest_proceeds')
    repayment_percentage = fields.Float('Repayment Percentage (%)', default=100.0)

    # Collateral
    collateral_input = fields.Boolean('Collateral Input', help="Input itself serves as collateral", default=True)

    # Tracking
    application_date = fields.Date('Application Date', default=fields.Date.context_today)
    approval_date = fields.Date('Approval Date')
    maturity_date = fields.Date('Maturity Date', compute='_compute_maturity_date', store=True, precompute=True)

    # Delivery & Usage
    delivery_status = fields.Selection([
        ('ordered', 'Ordered'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('used', 'Used'),
    ], string='Delivery Status', default='ordered')
    usage_verification = fields.Boolean('Usage Verification', default=False)

    # Risk
    risk_score = fields.Float('Risk Score', compute='_compute_risk_score')

    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='draft', required=True)

    @api.depends('quantity', 'unit_price')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = record.quantity * record.unit_price

    @api.depends('application_date', 'duration_months')
    def _compute_maturity_date(self):
        for record in self:
            if record.application_date and record.duration_months:
                record.maturity_date = fields.Date.from_string(record.application_date) + timedelta(days=record.duration_months*30)
            else:
                record.maturity_date = False

    @api.depends('partner_id')
    def _compute_risk_score(self):
        """Compute risk score based on partner's credit profile"""
        for record in self:
            if record.partner_id:
                # Check for existing credit score
                credit_score = self.env['farm.credit.score'].search([
                    ('partner_id', '=', record.partner_id.id)
                ], order='score_date desc', limit=1)
                record.risk_score = credit_score.total_score if credit_score else 60.0
            else:
                record.risk_score = 0.0

    def confirm_delivery(self):
        """Confirm input delivery"""
        self.write({'delivery_status': 'delivered'})

    def verify_usage(self):
        """Verify input usage"""
        self.write({'usage_verification': True})

    def calculate_financing_amount(self):
        """Calculate financing amount"""
        for record in self:
            # By default, finance 80% of total amount
            record.amount_financed = record.total_amount * 0.8

    def action_submit_application(self):
        """Submit application for approval"""
        for record in self:
            record.write({'state': 'submitted'})

    def action_approve_application(self):
        """Approve the financing application"""
        for record in self:
            if record.risk_score < 60:
                raise ValidationError(_("Cannot approve financing for partner with low risk score."))
            record.write({
                'state': 'approved',
                'approval_date': fields.Date.context_today(record),
                'amount_financed': record.total_amount * 0.8  # Default to 80%
            })

    def action_activate_service(self):
        """Activate the financing service"""
        for record in self:
            record.write({'state': 'active'})