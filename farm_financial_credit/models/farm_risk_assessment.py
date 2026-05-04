from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import random

class FarmRiskAssessment(models.Model):
    """
    Risk Assessment model combining features from both modules
    """
    _name = 'farm.risk.assessment'
    _description = 'Farm Risk Assessment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Assessment Name', required=True)
    partner_id = fields.Many2one('res.partner', string='Farmer', required=True)
    assessment_date = fields.Date('Assessment Date', default=fields.Date.context_today)

    # Farm characteristics from farm_financial_services
    farm_size = fields.Float('Farm Size (hectares)')
    farming_years = fields.Integer('Years in Farming')
    crop_variety_count = fields.Integer('Number of Crop Varieties')
    livestock_types = fields.Integer('Number of Livestock Types')
    annual_revenue = fields.Monetary('Annual Revenue', currency_field='currency_id')
    previous_losses = fields.Float('Previous Losses (3-year avg)', digits=(16, 2))
    debt_to_income_ratio = fields.Float('Debt to Income Ratio', digits=(16, 2))
    insurance_coverage_pct = fields.Float('Insurance Coverage (%)', default=30.0)

    # Risk scores from farm_financial_services
    diversification_score = fields.Float('Diversification Score (0-100)', digits=(16, 2))
    soil_quality_score = fields.Float('Soil Quality Score (0-100)', digits=(16, 2))
    irrigation_access = fields.Float('Irrigation Access Score (0-100)', digits=(16, 2))
    market_access_score = fields.Float('Market Access Score (0-100)', digits=(16, 2))
    technology_adoption = fields.Float('Technology Adoption Score (0-100)', digits=(16, 2))
    weather_risk_score = fields.Float('Weather Risk Score (0-100)', digits=(16, 2))
    market_price_volatility = fields.Float('Market Price Volatility Score (0-100)', digits=(16, 2))
    credit_history_score = fields.Float('Credit History Score (0-100)', digits=(16, 2))

    # Overall risk calculation combining both module approaches
    risk_score = fields.Float('Overall Risk Score (0-100)', compute='_compute_risk_score', store=True, precompute=True)
    overall_risk_rating = fields.Selection([
        ('excellent', 'Excellent (A+)'),
        ('very_good', 'Very Good (A)'),
        ('good', 'Good (B+)'),
        ('fair', 'Fair (B)'),
        ('poor', 'Poor (C)'),
        ('very_poor', 'Very Poor (D)'),
    ], string='Overall Risk Rating', compute='_compute_overall_rating', store=True, precompute=True)

    # Loan recommendations from farm_financial_services
    recommended_loan_amount = fields.Monetary('Recommended Loan Amount', currency_field='currency_id', compute='_compute_loan_recommendation', store=True, precompute=True)
    interest_rate_adjustment = fields.Float('Interest Rate Adjustment (+/- %)', digits=(16, 2))

    # Integration with credit scoring from farm_finance_loan
    credit_score_id = fields.Many2one('farm.credit.score', string='Credit Score Reference')

    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ], default='draft', required=True)

    @api.depends(
        'diversification_score', 'soil_quality_score', 'irrigation_access', 'market_access_score',
        'technology_adoption', 'weather_risk_score', 'market_price_volatility', 'credit_history_score',
        'debt_to_income_ratio', 'previous_losses', 'farming_years'
    )
    def _compute_risk_score(self):
        for record in self:
            # Calculate various risk components (weights are approximate)
            # Financial stability: 25%
            financial_score = max(0, min(100, 100 - (record.debt_to_income_ratio * 20) - (record.previous_losses / (record.annual_revenue + 1) * 100)))

            # Farming experience: 15%
            experience_score = min(100, record.farming_years * 5) if record.farming_years else 50

            # Diversification: 10%
            div_score = min(100, 20 * record.crop_variety_count + 10 * record.livestock_types)

            # Infrastructure: 15% - irrigation, tech adoption, soil quality, market access
            infra_score = (record.irrigation_access + record.technology_adoption + record.soil_quality_score + record.market_access_score) / 4

            # External risk factors: 20% - weather, price volatility
            external_score = 100 - max(0, min(100, (record.weather_risk_score + record.market_price_volatility) / 2))

            # Historical credit: 15%
            credit_score = record.credit_history_score if record.credit_history_score else 70

            # Calculate weighted risk score
            weighted_score = (
                financial_score * 0.25 +
                experience_score * 0.15 +
                div_score * 0.10 +
                infra_score * 0.15 +
                external_score * 0.20 +
                credit_score * 0.15
            )

            record.risk_score = weighted_score

    @api.depends('risk_score')
    def _compute_overall_rating(self):
        for record in self:
            if record.risk_score >= 90:
                record.overall_risk_rating = 'excellent'
            elif record.risk_score >= 80:
                record.overall_risk_rating = 'very_good'
            elif record.risk_score >= 70:
                record.overall_risk_rating = 'good'
            elif record.risk_score >= 60:
                record.overall_risk_rating = 'fair'
            elif record.risk_score >= 50:
                record.overall_risk_rating = 'poor'
            else:
                record.overall_risk_rating = 'very_poor'

    @api.depends('annual_revenue', 'risk_score')
    def _compute_loan_recommendation(self):
        for record in self:
            # Recommend loan as percentage of annual revenue, adjusted by risk
            base_percentage = record.risk_score / 100  # Use risk score as percentage of revenue
            record.recommended_loan_amount = record.annual_revenue * (base_percentage / 3)  # Cap at 1/3 of revenue for highest risk score

    def action_calculate_comprehensive_risk(self):
        """Calculate comprehensive risk score"""
        for record in self:
            # This would trigger the computation of all risk components
            # The actual calculations are done in the computed fields
            pass

    def action_update_from_credit_score(self):
        """Update assessment based on latest credit score"""
        for record in self:
            credit_score = self.env['farm.credit.score'].search([
                ('partner_id', '=', record.partner_id.id)
            ], order='score_date desc', limit=1)

            if credit_score:
                record.credit_score_id = credit_score.id
                # Update relevant fields based on credit score
                record.credit_history_score = credit_score.overall_score