from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import random

class AgriSupplyChainFinance(models.Model):
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id)
    """
    Supply Chain Finance functionality integrated into farm_finance_loan
    """
    _name = 'farm.supply.chain.finance'
    _description = 'Agricultural Supply Chain Finance'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Finance Reference', required=True)
    partner_id = fields.Many2one('res.partner', string='Farmer', required=True)
    sale_order_id = fields.Many2one('sale.order', string='Sales Order')
    invoice_id = fields.Many2one('account.move', string='Invoice')
    buyer_id = fields.Many2one('res.partner', string='Buyer', related='sale_order_id.partner_id', store=True)

    # Financial terms
    amount = fields.Monetary('Receivable Amount', currency_field='currency_id')
    advance_amount = fields.Monetary('Advance Amount', currency_field='currency_id', compute='_compute_advance_amount', store=True, precompute=True)
    financing_percentage = fields.Float('Financing Percentage (%)', default=80.0)
    interest_rate = fields.Float('Interest Rate (%)', default=5.0, digits=(16, 2))
    service_fees = fields.Monetary('Service Fees', currency_field='currency_id')
    duration_months = fields.Integer('Duration (months)', default=6)

    # Terms
    recourse_type = fields.Selection([
        ('recourse', 'Recourse'),
        ('non_recourse', 'Non-Recourse'),
    ], string='Recourse Type', default='recourse')

    # Tracking
    application_date = fields.Date('Application Date', default=fields.Date.context_today)
    approval_date = fields.Date('Approval Date')
    maturity_date = fields.Date('Maturity Date', compute='_compute_maturity_date', store=True, precompute=True)
    payment_received = fields.Boolean('Payment Received', default=False)
    early_payment_discount = fields.Float('Early Payment Discount (%)', default=2.0)

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

    @api.depends('amount', 'financing_percentage')
    def _compute_advance_amount(self):
        for record in self:
            if record.amount and record.financing_percentage:
                record.advance_amount = record.amount * (record.financing_percentage / 100)
            else:
                record.advance_amount = 0

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

    def calculate_financing_amount(self):
        """Calculate the financing amount based on receivable value"""
        for record in self:
            if record.invoice_id:
                record.amount = record.invoice_id.amount_total
            elif record.sale_order_id:
                record.amount = record.sale_order_id.amount_total

            record.advance_amount = record.amount * (record.financing_percentage / 100)

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
                'approval_date': fields.Date.context_today(record)
            })

    def action_activate_service(self):
        """Activate the financing service"""
        for record in self:
            record.write({'state': 'active'})