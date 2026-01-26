from odoo import models, fields, api
from odoo.exceptions import ValidationError

class IndustryESGModel(models.Model):
    """
    US-30-14: 行业特定ESG数据模型ISL扩展
    Industry Specific ESG Model for implementing industry-specific ESG data models
    """
    _name = 'farm.sustainability.industry.esg.model'
    _description = 'Industry Specific ESG Model'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Model Name', required=True)
    industry_type = fields.Selection([
        ('crop_farming', 'Crop Farming'),
        ('livestock', 'Livestock'),
        ('dairy', 'Dairy'),
        ('poultry', 'Poultry'),
        ('aquaculture', 'Aquaculture'),
        ('horticulture', 'Horticulture'),
        ('food_processing', 'Food Processing'),
        ('beverage', 'Beverage'),
        ('biofuel', 'Biofuel'),
        ('textile', 'Textile'),
        ('pharmaceutical', 'Pharmaceutical'),
        ('chemical', 'Chemical'),
        ('other', 'Other')
    ], string='Industry Type', required=True)
    description = fields.Text('Description')
    model_version = fields.Char('Model Version', default='1.0')
    active = fields.Boolean('Active', default=True)

    # ESG category support
    environmental_supported = fields.Boolean('Environmental Metrics Supported')
    social_supported = fields.Boolean('Social Metrics Supported')
    governance_supported = fields.Boolean('Governance Metrics Supported')

    # Industry-specific metrics
    environmental_metrics = fields.Text('Environmental Metrics JSON', help='JSON formatted list of environmental metrics for this industry')
    social_metrics = fields.Text('Social Metrics JSON', help='JSON formatted list of social metrics for this industry')
    governance_metrics = fields.Text('Governance Metrics JSON', help='JSON formatted list of governance metrics for this industry')

    # Reporting standards
    reporting_standard = fields.Selection([
        ('gri', 'GRI Standards'),
        ('sasb', 'SASB Standards'),
        ('tcfd', 'TCFD Recommendations'),
        ('cdp', 'CDP Questionnaire'),
        ('integrated_report', 'Integrated Reporting'),
        ('other', 'Other Standard')
    ], string='Primary Reporting Standard')
    secondary_standards = fields.Char('Secondary Standards', help='Comma-separated list of secondary standards')

    # Compliance and regulation
    applicable_regulations = fields.Text('Applicable Regulations')
    compliance_frequency = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semi_annually', 'Semi-Annually'),
        ('annually', 'Annually')
    ], string='Compliance Reporting Frequency', default='annually')

    # Scoring and targets
    esg_score_calculation_method = fields.Text('ESG Score Calculation Method',
                                               help='Description of how the ESG score is calculated for this industry')
    baseline_year = fields.Integer('Baseline Year', default=lambda self: fields.Date.context_today(self).year - 1)
    target_year = fields.Integer('Target Year', default=lambda self: fields.Date.context_today(self).year + 5)
    target_improvement_percentage = fields.Float('Target Improvement (%)',
                                                 help='Target percentage improvement from baseline')

    # Audit and verification
    audit_requirements = fields.Text('Audit Requirements')
    verification_body = fields.Char('Verification Body', help='Certifying body for ESG verification')

    # Related ESG metrics
    esg_metric_ids = fields.One2many('farm.sustainability.industry.esg.metric', 'model_id', 'ESG Metrics')

    @api.constrains('target_improvement_percentage')
    def _check_positive_target(self):
        """Ensure target improvement is non-negative"""
        for record in self:
            if record.target_improvement_percentage < 0:
                raise ValidationError("Target improvement percentage cannot be negative.")

    def action_calculate_esg_score(self, entity_data):
        """
        Calculate ESG score based on this industry-specific model
        This would be called with entity-specific data to compute an industry-adjusted ESG score
        """
        # This would be implemented to use industry-specific methodologies
        # For now, we'll return a structure that other models can use
        result = {
            'scoring_method': self.esg_score_calculation_method,
            'environmental_metrics': self.environmental_metrics,
            'social_metrics': self.social_metrics,
            'governance_metrics': self.governance_metrics,
            'baseline_year': self.baseline_year,
            'target_year': self.target_year,
            'target_improvement': self.target_improvement_percentage
        }
        return result