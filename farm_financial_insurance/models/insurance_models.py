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
    Implements US-059-03: Crop Yield Insurance Actuarial & Payout
    US-059-04: Index-based Insurance Automation
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
    premium_amount = fields.Monetary('Premium Amount', currency_field='currency_id', compute='_compute_premium_amount', store=True, precompute=True)
    duration_months = fields.Integer('Duration (months)')
    application_date = fields.Date('Application Date', default=fields.Date.context_today)
    approval_date = fields.Date('Approval Date')
    maturity_date = fields.Date('Maturity Date', compute='_compute_maturity_date', store=True, precompute=True)
    service_fees = fields.Monetary('Service Fees', currency_field='currency_id')

    product_id = fields.Many2one('product.template', string='Crop Type')
    land_location_id = fields.Many2one('farm.location', string='Farm Location')
    coverage_area = fields.Float('Coverage Area (hectares)')
    planting_date = fields.Date('Planting Date')
    expected_yield = fields.Float('Expected Yield (tons/ha)')
    coverage_type = fields.Selection([
        ('yield', 'Yield Only'),
        ('revenue', 'Revenue Protection'),
        ('multi_peril', 'Multi-Peril'),
        ('weather_index', 'Weather Index Based'),
    ], string='Coverage Type', default='yield')
    coverage_percentage = fields.Float('Coverage Percentage (%)', default=75.0)
    indemnity_base_price = fields.Float('Indemnity Base Price', digits=(16, 2))
    premium_rate = fields.Float('Premium Rate (%)', default=5.0)
    historical_yield = fields.Float('Historical Yield (tons/ha)', help="Historical yield for this farm")
    weather_monitoring = fields.Boolean('Weather Monitoring', default=True)

    # Claim management
    claim_ids = fields.One2many('farm.insurance.claim', 'insurance_id', string="Claims")
    claim_amount = fields.Monetary('Total Claim Amount', currency_field='currency_id', default=0)
    claim_status = fields.Selection([
        ('no_claim', 'No Claim'),
        ('reported', 'Claim Reported'),
        ('verified', 'Claim Verified'),
        ('approved', 'Claim Approved'),
        ('paid', 'Claim Paid'),
    ], string='Claim Status', default='no_claim')
    payout_percentage = fields.Float('Payout Percentage (%)', default=0.0, help="Percentage of claim approved")
    adjuster_id = fields.Many2one('res.partner', string='Claims Adjuster')

    # Index based configuration [US-059-04]
    weather_index_ids = fields.Many2many('farm.insurance.index', string="Weather Trigger Indices")

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
            actual_yield = record.expected_yield * random.uniform(0.3, 1.2)  # 30% to 120% of expected

            if actual_yield < record.expected_yield * (record.coverage_percentage / 100):
                # Calculate yield loss
                yield_loss = (record.expected_yield - actual_yield) * record.coverage_area
                claim_amt = yield_loss * record.indemnity_base_price

                # Create a claim record
                self.env['farm.insurance.claim'].create({
                    'insurance_id': record.id,
                    'claim_type': 'yield_loss',
                    'requested_amount': claim_amt,
                    'evidence_summary': f"Actual yield {actual_yield:.2f} tons/ha below threshold.",
                })
                record.claim_status = 'reported'
                record.state = 'claim_made'

    def action_check_weather_indices(self):
        """
        US-059-04: Automated Weather Index Claim Trigger
        Check if any weather indices are triggered based on telemetry/external data
        """
        for record in self:
            if not record.weather_index_ids:
                continue

            for index in record.weather_index_ids:
                # Mock: check if index is triggered (in real system, would check farm.weather.log)
                triggered, value = index._check_trigger(record.land_location_id)
                if triggered:
                    # Auto-generate claim
                    self.env['farm.insurance.claim'].create({
                        'insurance_id': record.id,
                        'claim_type': 'weather_index',
                        'index_id': index.id,
                        'requested_amount': record.amount * (index.payout_factor / 100.0),
                        'evidence_summary': f"Weather index '{index.name}' triggered. Value: {value}. Threshold: {index.threshold_value}",
                        'auto_triggered': True
                    })
                    record.claim_status = 'reported'
                    record.state = 'claim_made'

    def approve_claim(self):
        """Approve the insurance claim"""
        for record in self:
            record.claim_status = 'approved'
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


class FarmInsuranceIndex(models.Model):
    _name = 'farm.insurance.index'
    _description = 'Agricultural Insurance Index Trigger'

    name = fields.Char("Index Name", required=True)
    index_type = fields.Selection([
        ('rainfall_high', 'High Rainfall (Flood)'),
        ('rainfall_low', 'Low Rainfall (Drought)'),
        ('temp_high', 'Extreme Heat'),
        ('temp_low', 'Frost/Cold')
    ], string="Index Type", required=True)

    threshold_value = fields.Float("Threshold Value", required=True)
    comparison_operator = fields.Selection([
        ('gt', '>'), ('lt', '<'), ('gte', '>='), ('lte', '<=')
    ], string="Operator", default='gt', required=True)

    payout_factor = fields.Float("Payout Factor (%)", help="Percentage of total coverage to pay out if triggered", default=20.0)

    def _check_trigger(self, location_id):
        """Simulate checking weather logs"""
        # In reality, query farm.weather.log filtered by location and current period
        mock_val = random.uniform(0, 150)
        is_triggered = False
        if self.comparison_operator == 'gt' and mock_val > self.threshold_value:
            is_triggered = True
        elif self.comparison_operator == 'lt' and mock_val < self.threshold_value:
            is_triggered = True
        # ... other operators
        return is_triggered, mock_val


class FarmInsuranceClaim(models.Model):
    _name = 'farm.insurance.claim'
    _description = 'Agricultural Insurance Claim'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    insurance_id = fields.Many2one('farm.crop.yield.insurance', string="Policy", ondelete='cascade')
    claim_type = fields.Selection([
        ('yield_loss', 'Yield Loss'),
        ('weather_index', 'Weather Index Trigger'),
        ('pest_outbreak', 'Pest/Disease Outbreak')
    ], string="Claim Type", required=True)

    index_id = fields.Many2one('farm.insurance.index', string="Triggering Index")
    requested_amount = fields.Monetary("Requested Amount", currency_field='currency_id')
    approved_amount = fields.Monetary("Approved Amount", currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', related='insurance_id.currency_id')

    evidence_summary = fields.Text("Evidence Summary")
    auto_triggered = fields.Boolean("Auto-triggered", default=False)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('verified', 'Verified'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
        ('rejected', 'Rejected')
    ], string="Status", default='draft')

    def action_verify(self):
        self.state = 'verified'

    def action_approve(self):
        self.state = 'approved'
        self.approved_amount = self.requested_amount