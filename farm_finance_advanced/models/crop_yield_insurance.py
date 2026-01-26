# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
import json
from datetime import datetime, timedelta
import random

_logger = logging.getLogger(__name__)

class FarmCropYieldInsurance(models.Model):
    """
    Model for crop yield insurance
    Implements US-58-03: Crop Yield Insurance Actuarial & Payout
    """
    _name = 'farm.crop.yield.insurance'
    _description = 'Farm Crop Yield Insurance'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Insurance Policy Reference', required=True, default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string='Farmer', required=True)
    insurance_type = fields.Selection([('crop_yield', 'Crop Yield Insurance')], string='Insurance Type', default='crop_yield')

    amount = fields.Monetary('Insurance Coverage Amount', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('active', 'Active'),
        ('claim_made', 'Claim Made'),
        ('claim_approved', 'Claim Approved'),
        ('settled', 'Settled'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', required=True)
    reference = fields.Char('Reference', help="External reference from insurance provider")
    risk_score = fields.Float('Risk Score')
    premium_amount = fields.Monetary('Premium Amount', currency_field='currency_id', compute='_compute_premium_amount', store=True)
    duration_months = fields.Integer('Duration (months)')
    application_date = fields.Date('Application Date', default=fields.Date.context_today)
    approval_date = fields.Date('Approval Date')
    maturity_date = fields.Date('Maturity Date', compute='_compute_maturity_date', store=True)
    service_fees = fields.Monetary('Service Fees', currency_field='currency_id')

    product_id = fields.Many2one('product.template', string='Crop Type')
    land_location_id = fields.Many2one('stock.location', string='Farm Location')
    coverage_area = fields.Float('Coverage Area (hectares)')
    planting_date = fields.Date('Planting Date')
    expected_yield = fields.Float('Expected Yield (tons/ha)')
    coverage_type = fields.Selection([
        ('yield', 'Yield Only'),
        ('revenue', 'Revenue Protection'),
        ('multi_peril', 'Multi-Peril'),
    ], string='Coverage Type', default='yield')
    coverage_percentage = fields.Float('Coverage Percentage (%)', default=75.0)
    indemnity_base_price = fields.Float('Indemnity Base Price', digits=(16, 2))
    premium_rate = fields.Float('Premium Rate (%)', default=5.0)
    premium_amount = fields.Monetary('Premium Amount', currency_field='currency_id', compute='_compute_premium_amount', store=True)
    historical_yield = fields.Float('Historical Yield (tons/ha)', help="Historical yield for this farm")
    weather_monitoring = fields.Boolean('Weather Monitoring', default=True)
    claim_amount = fields.Monetary('Claim Amount', currency_field='currency_id', default=0)
    claim_status = fields.Selection([
        ('no_claim', 'No Claim'),
        ('reported', 'Claim Reported'),
        ('verified', 'Claim Verified'),
        ('approved', 'Claim Approved'),
        ('paid', 'Claim Paid'),
    ], string='Claim Status', default='no_claim')
    payout_percentage = fields.Float('Payout Percentage (%)', default=0.0, help="Percentage of claim approved")
    adjuster_id = fields.Many2one('res.partner', string='Claims Adjuster')

    @api.depends('application_date', 'duration_months')
    def _compute_maturity_date(self):
        for record in self:
            if record.application_date and record.duration_months:
                record.maturity_date = fields.Date.from_string(record.application_date) + timedelta(days=record.duration_months*30)
            else:
                record.maturity_date = False

    @api.depends('amount', 'premium_rate')
    def _compute_premium_amount(self):
        for record in self:
            record.premium_amount = record.amount * (record.premium_rate / 100)

    def calculate_expected_yield(self):
        """Calculate expected yield based on historical data and crop variety"""
        for record in self:
            if record.product_id and record.land_location_id:
                # Base yield by crop type
                base_yields = {
                    'corn': 8.0,
                    'wheat': 4.0,
                    'soybean': 3.0,
                    'rice': 6.0,
                    'cotton': 1.5,
                    'potato': 40.0,
                    'tomato': 60.0,
                }

                crop_name = record.product_id.name.lower() if record.product_id.name else ''
                base_yield = next((yield_val for crop_name_key, yield_val in base_yields.items()
                                  if crop_name_key in crop_name), 5.0)  # Default to 5 if not found

                # Adjust by historical performance of this location
                if record.historical_yield:
                    adjustment = record.historical_yield / 5.0  # Normalize to 5 as baseline
                    base_yield = base_yield * adjustment

                record.expected_yield = base_yield

                # Calculate insured amount
                record.amount = record.coverage_area * base_yield * record.indemnity_base_price * (record.coverage_percentage / 100)

    def calculate_claim(self):
        """Calculate insurance claim based on actual vs expected yield"""
        for record in self:
            # In a real system, this would connect to yield monitoring systems
            # For simulation, we'll use random actual yield
            actual_yield = record.expected_yield * random.uniform(0.3, 1.2)  # 30% to 120% of expected

            if actual_yield < record.expected_yield * (record.coverage_percentage / 100):
                # Calculate yield loss
                yield_loss = (record.expected_yield - actual_yield) * record.coverage_area
                record.claim_amount = yield_loss * record.indemnity_base_price
                record.payout_percentage = min(100, (record.claim_amount / record.amount) * 100)
            else:
                record.claim_amount = 0
                record.payout_percentage = 0

            record.claim_status = 'verified'  # Simulate verification step

    def approve_claim(self):
        """Approve the insurance claim"""
        for record in self:
            record.claim_status = 'approved'
            record.payout_percentage = min(100, record.payout_percentage)  # Cap at 100%
            record.state = 'claim_approved'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.crop.yield.insurance') or _('CYI')
        return super().create(vals_list)

    def action_submit_application(self):
        """Submit the insurance application"""
        self.write({'state': 'submitted'})

    def action_approve_insurance(self):
        """Approve the insurance application"""
        self.write({'state': 'approved', 'approval_date': fields.Date.context_today(self)})

    def action_activate_insurance(self):
        """Activate the insurance policy"""
        self.write({'state': 'active'})

    def action_settle_claim(self):
        """Settle the approved claim"""
        self.write({'state': 'settled'})