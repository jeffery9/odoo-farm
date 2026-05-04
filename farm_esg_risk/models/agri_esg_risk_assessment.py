from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AgriESGRiskAssessment(models.Model):
    """
    US-082-01: ESG风险自动评估与评级
    US-082-02: 合规风险自动监控与预警
    ESG Risk Assessment for automatic evaluation and rating
    """
    _name = 'agri.esg.risk.assessment'
    _description = 'Agricultural ESG Risk Assessment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Assessment Name', required=True)
    assessment_date = fields.Date('Assessment Date', required=True, default=fields.Date.context_today)
    assessment_type = fields.Selection([
        'environmental', 'social', 'governance', 'combined'
    ], string='Assessment Type', required=True, default='combined')
    assessment_period = fields.Selection([
        ('q1', 'Q1'),
        ('q2', 'Q2'),
        ('q3', 'Q3'),
        ('q4', 'Q4'),
        ('annual', 'Annual')
    ], string='Assessment Period', required=True)
    year = fields.Integer('Year', default=lambda self: fields.Date.context_today(self).year)
    environmental_score = fields.Float('Environmental Score', help='Score from 0-100 for environmental factors')
    social_score = fields.Float('Social Score', help='Score from 0-100 for social factors')
    governance_score = fields.Float('Governance Score', help='Score from 0-100 for governance factors')
    overall_esg_score = fields.Float('Overall ESG Score', compute='_compute_overall_score', store=True)
    esg_risk_level = fields.Selection([
        ('very_low', 'Very Low (90-100)'),
        ('low', 'Low (70-89)'),
        ('medium', 'Medium (50-69)'),
        ('high', 'High (30-49)'),
        ('very_high', 'Very High (0-29)')
    ], string='ESG Risk Level', compute='_compute_risk_level', store=True)
    next_assessment_date = fields.Date('Next Assessment Date')
    assessment_method = fields.Selection([
        ('automated', 'Automated'),
        ('manual', 'Manual'),
        ('hybrid', 'Hybrid')
    ], string='Assessment Method', default='automated')

    # Environmental risk factors
    carbon_intensity = fields.Float('Carbon Intensity')
    water_usage_efficiency = fields.Float('Water Usage Efficiency')
    waste_management_score = fields.Float('Waste Management Score')
    biodiversity_impact_score = fields.Float('Biodiversity Impact Score')

    # Social risk factors
    labor_practice_score = fields.Float('Labor Practice Score')
    community_relation_score = fields.Float('Community Relation Score')
    health_safety_score = fields.Float('Health Safety Score')

    # Governance risk factors
    transparency_score = fields.Float('Transparency Score')
    compliance_score = fields.Float('Compliance Score')
    ethics_score = fields.Float('Ethics Score')

    risk_factors = fields.Text('Risk Factors', help='Description of identified risk factors')
    mitigation_plan = fields.Text('Mitigation Plan', help='Plan to address identified risks')
    responsible_user = fields.Many2one('res.users', 'Responsible User')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('reviewed', 'Reviewed')
    ], string='Status', default='draft')

    @api.depends('environmental_score', 'social_score', 'governance_score')
    def _compute_overall_score(self):
        """Compute the overall ESG score as average of three components"""
        for record in self:
            record.overall_esg_score = (
                (record.environmental_score or 0) +
                (record.social_score or 0) +
                (record.governance_score or 0)
            ) / 3

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
            if record.environmental_score and (record.environmental_score < 0 or record.environmental_score > 100):
                raise ValidationError("Environmental score must be between 0 and 100.")
            if record.social_score and (record.social_score < 0 or record.social_score > 100):
                raise ValidationError("Social score must be between 0 and 100.")
            if record.governance_score and (record.governance_score < 0 or record.governance_score > 100):
                raise ValidationError("Governance score must be between 0 and 100.")

    @api.model
    def generate_risk_assessment_report(self, year=None, assessment_period=None):
        """Generate ESG risk assessment report"""
        if year is None:
            year = fields.Date.context_today(self).year

        domain = [('year', '=', year)]
        if assessment_period:
            domain.append(('assessment_period', '=', assessment_period))

        assessments = self.search(domain)

        if not assessments:
            return {
                'year': year,
                'period': assessment_period,
                'total_assessments': 0,
                'avg_overall_esg_score': 0.0,
                'esg_risk_distribution': {}
            }

        total_assessments = len(assessments)
        avg_esg_score = sum(assessments.mapped('overall_esg_score')) / len(assessments)

        # Count risk levels
        risk_distribution = {
            'very_low': len(assessments.filtered(lambda r: r.esg_risk_level == 'very_low')),
            'low': len(assessments.filtered(lambda r: r.esg_risk_level == 'low')),
            'medium': len(assessments.filtered(lambda r: r.esg_risk_level == 'medium')),
            'high': len(assessments.filtered(lambda r: r.esg_risk_level == 'high')),
            'very_high': len(assessments.filtered(lambda r: r.esg_risk_level == 'very_high'))
        }

        return {
            'year': year,
            'period': assessment_period,
            'total_assessments': total_assessments,
            'avg_overall_esg_score': avg_esg_score,
            'esg_risk_distribution': risk_distribution,
            'detailed_assessments': assessments
        }

    def action_calculate_scores_automatically(self):
        """Calculate ESG scores automatically based on related data"""
        for record in self:
            # This would typically pull data from other ESG modules
            # For now, we'll use placeholder logic
            record.environmental_score = record._calculate_environmental_score()
            record.social_score = record._calculate_social_score()
            record.governance_score = record._calculate_governance_score()

    def _calculate_environmental_score(self):
        """Calculate environmental score based on related data"""
        # Placeholder implementation - in real scenario, this would aggregate data from environmental modules
        return 75.0

    def _calculate_social_score(self):
        """Calculate social score based on related data"""
        # Placeholder implementation - in real scenario, this would aggregate data from social modules
        return 80.0

    def _calculate_governance_score(self):
        """Calculate governance score based on related data"""
        # Placeholder implementation - in real scenario, this would aggregate data from governance modules
        return 85.0