from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SupplyChainESGRating(models.Model):
    """
    US-082-07: 供应链ESG风险评估
    US-091-08: 供应链可持续性评估
    Supply Chain ESG Rating for supplier sustainability assessment
    """
    _name = 'farm.esg.supply.chain.rating'
    _description = 'Supply Chain ESG Rating'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Rating Name', required=True)
    supplier_id = fields.Many2one('res.partner', 'Supplier', required=True)
    rating_date = fields.Date('Rating Date', required=True, default=fields.Date.context_today)
    environmental_score = fields.Float('Environmental Score (0-100)')
    social_score = fields.Float('Social Score (0-100)')
    governance_score = fields.Float('Governance Score (0-100)')
    overall_esg_score = fields.Float('Overall ESG Score', compute='_compute_overall_score', store=True)
    esg_risk_level = fields.Selection([
        ('very_low', 'Very Low (90-100)'),
        ('low', 'Low (70-89)'),
        ('medium', 'Medium (50-69)'),
        ('high', 'High (30-49)'),
        ('very_high', 'Very High (0-29)')
    ], string='ESG Risk Level', compute='_compute_risk_level', store=True)
    rating_period = fields.Selection([
        ('q1', 'Q1'),
        ('q2', 'Q2'),
        ('q3', 'Q3'),
        ('q4', 'Q4'),
        ('annual', 'Annual')
    ], string='Rating Period', required=True)
    year = fields.Integer('Year', default=lambda self: fields.Date.context_today(self).year)
    next_rating_date = fields.Date('Next Rating Date')
    rating_method = fields.Selection([
        ('self_assessment', 'Self Assessment'),
        ('third_party', 'Third Party Audit'),
        ('hybrid', 'Hybrid'),
        ('automated', 'Automated')
    ], string='Rating Method', default='self_assessment')
    assessment_criteria = fields.Text('Assessment Criteria')
    compliance_status = fields.Selection([
        ('compliant', 'Compliant'),
        ('partially_compliant', 'Partially Compliant'),
        ('non_compliant', 'Non-Compliant')
    ], string='Compliance Status')
    corrective_action_required = fields.Boolean('Corrective Action Required')
    corrective_action_plan = fields.Text('Corrective Action Plan')
    improvement_deadline = fields.Date('Improvement Deadline')
    rating_valid_until = fields.Date('Rating Valid Until')
    assurance_provider = fields.Char('Assurance Provider')
    rating_notes = fields.Text('Rating Notes')

    @api.depends('environmental_score', 'social_score', 'governance_score')
    def _compute_overall_score(self):
        """Compute the overall ESG score as average of three components"""
        for record in self:
            scores = [s for s in [record.environmental_score, record.social_score, record.governance_score] if s is not None]
            if scores:
                record.overall_esg_score = sum(scores) / len(scores)
            else:
                record.overall_esg_score = 0.0

    @api.depends('overall_esg_score')
    def _compute_risk_level(self):
        """Compute the ESG risk level based on overall score"""
        for record in self:
            score = record.overall_esg_score
            if score >= 90:
                record.esg_risk_level = 'very_low'
            elif score >= 70:
                record.esg_risk_level = 'low'
            elif score >= 50:
                record.esg_risk_level = 'medium'
            elif score >= 30:
                record.esg_risk_level = 'high'
            else:
                record.esg_risk_level = 'very_high'

    @api.constrains('environmental_score', 'social_score', 'governance_score')
    def _check_scores_range(self):
        """Ensure scores are within 0-100 range"""
        for record in self:
            for score_name in ['environmental_score', 'social_score', 'governance_score']:
                score_value = record[score_name]
                if score_value is not None and (score_value < 0 or score_value > 100):
                    raise ValidationError(f"{score_name.replace('_', ' ').title()} must be between 0 and 100.")