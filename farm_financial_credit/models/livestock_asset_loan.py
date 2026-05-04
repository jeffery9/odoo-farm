# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
import json
from datetime import datetime, timedelta
import random

_logger = logging.getLogger(__name__)

class FarmLivestockAssetLoan(models.Model):
    """
    Model for live animal asset lending
    Implements US-088-02: Live Asset Mortgage Loan Management
    """
    _name = 'farm.livestock.asset.loan'
    _description = 'Farm Livestock Asset Loan'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Loan Reference', required=True, default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string='Farmer', required=True)
    loan_type = fields.Selection([('livestock', 'Livestock Asset Loan')], string='Loan Type', default='livestock')

    amount = fields.Monetary('Loan Amount', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('active', 'Active'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', required=True)
    reference = fields.Char('Reference', help="External reference from financial institution")
    risk_score = fields.Float('Risk Score')
    interest_rate = fields.Float('Interest Rate (%)', digits=(16, 2), default=8.0)
    duration_months = fields.Integer('Duration (months)')
    application_date = fields.Date('Application Date', default=fields.Date.context_today)
    approval_date = fields.Date('Approval Date')
    maturity_date = fields.Date('Maturity Date', compute='_compute_maturity_date', store=True, precompute=True)
    collateral_value = fields.Monetary('Collateral Value', currency_field='currency_id')
    insurance_coverage = fields.Float('Insurance Coverage (%)', help="Insurance coverage percentage")
    service_fees = fields.Monetary('Service Fees', currency_field='currency_id')

    animal_category = fields.Selection([
        ('cattle', 'Cattle'),
        ('poultry', 'Poultry'),
        ('swine', 'Swine'),
        ('sheep', 'Sheep'),
        ('goats', 'Goats'),
        ('horses', 'Horses'),
    ], string='Animal Category')
    animal_count = fields.Integer('Animal Count')
    animal_avg_weight = fields.Float('Average Weight (kg)')
    animal_age_months = fields.Integer('Average Age (months)')
    breed_type = fields.Char('Breed Type')
    animal_valuation = fields.Monetary('Animal Valuation', currency_field='currency_id')
    valuation_date = fields.Date('Valuation Date', default=fields.Date.context_today)
    insurance_policy = fields.Char('Insurance Policy Number')
    veterinary_cert = fields.Char('Veterinary Certificate')
    health_status = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ], string='Health Status', default='good')
    monitoring_frequency = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('biweekly', 'Bi-weekly'),
        ('monthly', 'Monthly'),
    ], string='Monitoring Frequency', default='weekly')
    tracking_device_id = fields.Char('Tracking Device ID')
    loan_to_value_ratio = fields.Float('Loan-to-Value Ratio (%)', default=70.0)

    def calculate_animal_valuation(self):
        """Calculate live animal valuation based on various factors"""
        for record in self:
            if record.animal_category and record.animal_count:
                # Base valuation per animal by category
                base_values = {
                    'cattle': 2000.0,
                    'poultry': 10.0,
                    'swine': 150.0,
                    'sheep': 100.0,
                    'goats': 80.0,
                    'horses': 3000.0,
                }

                base_value = base_values.get(record.animal_category, 100.0)

                # Adjust by weight and age
                weight_factor = 1.0
                if record.animal_avg_weight:
                    weight_factor = record.animal_avg_weight / 500.0 if record.animal_category == 'cattle' else record.animal_avg_weight / 2.0

                age_factor = 1.0
                if record.animal_age_months:
                    # Peak value at maturity
                    if record.animal_category in ['cattle', 'swine', 'sheep', 'goats']:
                        if 12 <= record.animal_age_months <= 24:
                            age_factor = 1.2  # Peak value period
                        elif record.animal_age_months > 60:
                            age_factor = 0.8  # Older animals worth less
                        else:
                            age_factor = min(1.1, record.animal_age_months / 12.0)

                # Adjust by health status
                health_factor = {'excellent': 1.1, 'good': 1.0, 'fair': 0.8, 'poor': 0.6}.get(record.health_status, 1.0)

                total_valuation = base_value * record.animal_count * weight_factor * age_factor * health_factor
                record.animal_valuation = total_valuation
                record.collateral_value = total_valuation

                # Calculate risk score based on animal factors
                risk_factors = [
                    10 if record.health_status == 'poor' else 0,
                    5 if record.animal_age_months and record.animal_age_months > 60 else 0,
                    5 if record.animal_category in ['poultry'] else 0,  # Higher risk for poultry due to disease
                ]
                base_risk = sum(risk_factors)
                record.risk_score = max(40, 100 - base_risk)

    def update_health_status(self):
        """Update health status based on monitoring"""
        for record in self:
            # In a real implementation, this would connect to IoT sensors or veterinary data
            # For simulation, we'll randomly adjust health status
            if record.health_status == 'excellent':
                new_health = random.choice(['excellent', 'good', 'good'])
            elif record.health_status == 'good':
                new_health = random.choice(['excellent', 'good', 'fair'])
            elif record.health_status == 'fair':
                new_health = random.choice(['good', 'fair', 'poor'])
            else:
                new_health = random.choice(['fair', 'poor'])

            record.health_status = new_health

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.livestock.asset.loan') or _('LAL')
        return super().create(vals_list)

    @api.depends('application_date', 'duration_months')
    def _compute_maturity_date(self):
        for record in self:
            if record.application_date and record.duration_months:
                record.maturity_date = fields.Date.from_string(record.application_date) + timedelta(days=record.duration_months*30)
            else:
                record.maturity_date = False

    def action_submit_application(self):
        """Submit the loan application"""
        self.write({'state': 'submitted'})

    def action_approve_loan(self):
        """Approve the loan application"""
        self.write({'state': 'approved', 'approval_date': fields.Date.context_today(self)})

    def action_activate_loan(self):
        """Activate the loan after approval"""
        self.write({'state': 'active'})

    def action_mark_repaid(self):
        """Mark the loan as repaid"""
        self.write({'state': 'paid'})