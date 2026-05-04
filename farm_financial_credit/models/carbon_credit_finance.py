# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
import json
from datetime import datetime, timedelta
import random

_logger = logging.getLogger(__name__)

class FarmCarbonCreditFinance(models.Model):
    """
    Model for carbon credit financing
    Implements US-060-05: Agri-Carbon Credit Trading & Financialization
    """
    _name = 'farm.carbon.credit.finance'
    _description = 'Farm Carbon Credit Finance'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Carbon Finance Reference', required=True, default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string='Farm/Partner', required=True)
    finance_type = fields.Selection([('carbon_credit', 'Carbon Credit Finance')], string='Finance Type', default='carbon_credit')

    amount = fields.Monetary('Finance Amount', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('active', 'Active'),
        ('verified', 'Verified'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', required=True)
    reference = fields.Char('Reference', help="External reference from financial institution")
    risk_score = fields.Float('Risk Score')
    interest_rate = fields.Float('Interest Rate (%)', digits=(16, 2), default=5.0)
    duration_months = fields.Integer('Duration (months)')
    application_date = fields.Date('Application Date', default=fields.Date.context_today)
    approval_date = fields.Date('Approval Date')
    maturity_date = fields.Date('Maturity Date', compute='_compute_maturity_date', store=True)
    service_fees = fields.Monetary('Service Fees', currency_field='currency_id')

    credit_type = fields.Selection([
        ('soil_carbon', 'Soil Carbon'),
        ('reduced_tillage', 'Reduced Tillage'),
        ('cover_crop', 'Cover Crop'),
        ('methane_capture', 'Methane Capture'),
        ('reforestation', 'Reforestation'),
    ], string='Credit Type')
    project_area = fields.Float('Project Area (hectares)')
    methodology_id = fields.Char('Methodology ID', help="Standard methodology used for calculation")
    baseline_emissions = fields.Float('Baseline Emissions (tCO2e)', digits=(16, 4))
    projected_reduction = fields.Float('Projected Emission Reduction (tCO2e)', digits=(16, 4))
    credit_quantity = fields.Float('Credit Quantity (tons CO2e)', digits=(16, 4), compute='_compute_credit_quantity', store=True)
    credit_value_per_ton = fields.Float('Credit Value per Ton ($)', digits=(16, 2))
    total_credit_value = fields.Monetary('Total Credit Value', currency_field='currency_id', compute='_compute_total_credit_value', store=True)
    project_start_date = fields.Date('Project Start Date')
    verification_date = fields.Date('Verification Date')
    credit_validity_years = fields.Integer('Credit Validity (years)', default=5)
    registry_name = fields.Char('Registry Name', help="Carbon registry where credits are registered")
    certification_body = fields.Char('Certification Body')
    project_location = fields.Many2one('farm.location', string='Project Location')
    implementation_status = fields.Selection([
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('verified', 'Verified'),
    ], string='Implementation Status', default='planned')
    financing_structure = fields.Selection([
        ('upfront', 'Upfront Financing'),
        ('pay_for_results', 'Pay for Results'),
        ('hybrid', 'Hybrid'),
    ], string='Financing Structure', default='pay_for_results')

    @api.depends('projected_reduction')
    def _compute_credit_quantity(self):
        for record in self:
            # Credit quantity typically equals emission reduction
            record.credit_quantity = record.projected_reduction

    @api.depends('credit_quantity', 'credit_value_per_ton')
    def _compute_total_credit_value(self):
        for record in self:
            record.total_credit_value = record.credit_quantity * record.credit_value_per_ton

    def calculate_emission_reduction(self):
        """Calculate projected emission reduction based on project type"""
        for record in self:
            if record.project_area:
                # Emission reduction factors by credit type (tCO2e/hectare/year)
                reduction_factors = {
                    'soil_carbon': 2.5,
                    'reduced_tillage': 1.2,
                    'cover_crop': 1.8,
                    'methane_capture': 5.0,
                    'reforestation': 3.0,
                }

                factor = reduction_factors.get(record.credit_type, 2.0)
                record.projected_reduction = record.project_area * factor

                # Calculate credit quantity
                record.credit_quantity = record.projected_reduction

                # Set default credit value based on market rates
                record.credit_value_per_ton = random.uniform(10, 30)  # $10-30 per ton
                record.amount = record.total_credit_value

    def verify_project(self):
        """Verify project implementation"""
        self.write({
            'verification_date': fields.Date.context_today(self),
            'implementation_status': 'verified'
        })

    @api.depends('application_date', 'duration_months')
    def _compute_maturity_date(self):
        for record in self:
            if record.application_date and record.duration_months:
                record.maturity_date = fields.Date.from_string(record.application_date) + timedelta(days=record.duration_months*30)
            else:
                record.maturity_date = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.carbon.credit.finance') or _('CCF')
        return super().create(vals_list)

    def action_submit_application(self):
        """Submit the carbon credit financing application"""
        self.write({'state': 'submitted'})

    def action_approve_finance(self):
        """Approve the financing application"""
        self.write({'state': 'approved', 'approval_date': fields.Date.context_today(self)})

    def action_activate_finance(self):
        """Activate the financing service"""
        self.write({'state': 'active'})

    def action_complete_finance(self):
        """Mark the financing as completed"""
        self.write({'state': 'completed'})