from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import random

class FarmLoan(models.Model):
    _name = 'farm.loan'
    _description = 'Agricultural Loan'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Loan Reference", default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string="Lender (Bank/Co-op)", required=True)
    loan_type = fields.Selection([
        ('operational', 'Operational'),
        ('equipment', 'Equipment'),
        ('biological', 'Biological Asset Mortgage'),
        ('input', 'Input Financing'),
        ('supply_chain', 'Supply Chain Finance'),
        ('carbon_credit', 'Carbon Credit Finance'),
        ('subsidy', 'Subsidy Finance'),
    ], required=True)

    amount_principal = fields.Monetary("Principal Amount", currency_field='currency_id')
    amount_interest = fields.Monetary("Projected Interest", currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)

    # Financial terms from farm_financial_services integration
    interest_rate = fields.Float('Interest Rate (%)', digits=(16, 2), default=8.0)
    duration_months = fields.Integer('Duration (months)')
    service_fees = fields.Monetary('Service Fees', currency_field='currency_id')
    repayment_frequency = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('harvest', 'At Harvest'),
        ('end_term', 'End of Term'),
    ], string='Repayment Frequency', default='monthly')

    date_start = fields.Date("Start Date")
    date_maturity = fields.Date("Maturity Date")

    # Collateral from original farm_finance_loan with improvement
    collateral_lot_ids = fields.Many2many('stock.lot', 'farm_loan_stock_lot_collateral_rel', 'loan_id', 'lot_id', string="Collateral Assets")
    collateral_value = fields.Monetary("Collateral Valuation", compute='_compute_collateral_value')

    # Financial Trust Integration [US-078-02]
    credit_score_id = fields.Many2one('farm.credit.score', string="Production Credit Rating", compute='_compute_credit_rating', store=True, precompute=True)
    credit_score = fields.Float(related='credit_score_id.total_score', string="Score Value")
    is_high_risk = fields.Boolean("High Financial Risk", compute='_compute_risk', store=True, precompute=True)

    # Risk assessment from integrated functionality
    risk_assessment_id = fields.Many2one('farm.risk.assessment', string="Risk Assessment")
    risk_score = fields.Float(related='risk_assessment_id.risk_score', string="Risk Score")

    # Repayment tracking
    total_repaid = fields.Monetary("Total Repaid", currency_field='currency_id', compute='_compute_repayment_status', store=True, precompute=True)
    remaining_balance = fields.Monetary("Remaining Balance", currency_field='currency_id', compute='_compute_repayment_status', store=True, precompute=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('active', 'Active'),
        ('in_default', 'In Default'),
        ('paid', 'Fully Paid'),
        ('defaulted', 'Defaulted'),
        ('cancelled', 'Cancelled'),
    ], default='draft', tracking=True)

    @api.depends('partner_id')
    def _compute_credit_rating(self):
        for loan in self:
            rating = self.env['farm.credit.score'].search([
                ('partner_id', '=', loan.partner_id.id),
                ('state', '=', 'validated')
            ], order='rating_date desc', limit=1)
            loan.credit_score_id = rating

    @api.depends('credit_score')
    def _compute_risk(self):
        for loan in self:
            loan.is_high_risk = loan.credit_score < 70.0 if loan.credit_score_id else False

    @api.depends('collateral_lot_ids')
    def _compute_collateral_value(self):
        for loan in self:
            # Enhanced valuation using biological asset valuation where available
            val = 0.0
            for lot in loan.collateral_lot_ids:
                # Check if lot has an associated biological asset with valuation
                bio_asset = self.env['agri.biological.asset'].search([('lot_id', '=', lot.id)], limit=1)
                if bio_asset:
                    val += bio_asset.current_valuation
                else:
                    # Fallback to product standard price
                    price = lot.product_id.standard_price
                    qty = getattr(lot, 'animal_count', 1)
                    val += price * qty
            loan.collateral_value = val

    @api.depends('amount_principal', 'amount_interest', 'total_repaid')
    def _compute_repayment_status(self):
        for loan in self:
            total_due = loan.amount_principal + loan.amount_interest
            loan.total_repaid = min(loan.total_repaid, total_due)  # Cap at total due
            loan.remaining_balance = max(0, total_due - loan.total_repaid)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.loan') or _('LOAN')
        return super().create(vals_list)

    def action_submit_application(self):
        """Submit loan application for review"""
        for loan in self:
            loan.write({
                'state': 'submitted',
                'date_start': fields.Date.today()
            })

    def action_approve_loan(self):
        """Approve the loan application"""
        for loan in self:
            if not loan.credit_score_id or loan.credit_score < 60:
                raise ValidationError(_("Cannot approve loan for partner with low credit score."))
            loan.write({
                'state': 'approved'
            })

    def action_disburse_loan(self):
        """Disburse funds for approved loan"""
        for loan in self:
            if loan.state != 'approved':
                raise ValidationError(_("Loan must be approved before disbursement."))
            loan.write({
                'state': 'active',
                'date_start': fields.Date.today()
            })

    def action_mark_repaid(self, amount):
        """Record loan repayment"""
        for loan in self:
            new_repaid = loan.total_repaid + amount
            loan.write({
                'total_repaid': new_repaid
            })
            if loan.remaining_balance <= 0:
                loan.write({'state': 'paid'})