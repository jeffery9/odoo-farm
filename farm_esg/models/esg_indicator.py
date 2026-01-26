from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ESGIndicator(models.Model):
    """
    ESG Indicator model to define measurable ESG metrics
    """
    _name = 'esg.indicator'
    _description = 'ESG Indicator'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'category, name'

    name = fields.Char('Indicator Name', required=True)
    code = fields.Char('Indicator Code', required=True, copy=False)
    description = fields.Text('Description')
    category = fields.Selection([
        ('environmental', 'Environmental'),
        ('social', 'Social'),
        ('governance', 'Governance')
    ], string='Category', required=True)
    subcategory = fields.Selection([
        # Environmental subcategories
        ('carbon_emissions', 'Carbon Emissions'),
        ('water_usage', 'Water Usage'),
        ('waste_management', 'Waste Management'),
        ('biodiversity', 'Biodiversity'),
        ('energy_efficiency', 'Energy Efficiency'),
        ('pollution_control', 'Pollution Control'),
        # Social subcategories
        ('employee_wellbeing', 'Employee Wellbeing'),
        ('diversity_inclusion', 'Diversity & Inclusion'),
        ('community_engagement', 'Community Engagement'),
        ('health_safety', 'Health & Safety'),
        ('local_employment', 'Local Employment'),
        ('fair_wages', 'Fair Wages'),
        # Governance subcategories
        ('compliance', 'Compliance'),
        ('transparency', 'Transparency'),
        ('ethics', 'Ethics'),
        ('risk_management', 'Risk Management'),
        ('stakeholder_engagement', 'Stakeholder Engagement'),
        ('board_diversity', 'Board Diversity')
    ], string='Subcategory', required=True)

    framework_id = fields.Many2one('esg.framework', 'ESG Framework', required=True)
    unit_of_measurement = fields.Char('Unit of Measurement', required=True)
    data_collection_method = fields.Selection([
        ('automated', 'Automated Collection'),
        ('manual_input', 'Manual Input'),
        ('third_party', 'Third Party Data'),
        ('survey', 'Survey'),
        ('audit', 'Audit')
    ], string='Data Collection Method', default='manual_input')

    # Target and benchmarking
    baseline_value = fields.Float('Baseline Value')
    target_value = fields.Float('Target Value')
    threshold_value = fields.Float('Threshold Value', help='Minimum acceptable value')
    weight = fields.Float('Weight', default=1.0, help='Weight in overall ESG score calculation')

    # Data validation
    min_acceptable_value = fields.Float('Min Acceptable Value')
    max_acceptable_value = fields.Float('Max Acceptable Value')
    is_percentage = fields.Boolean('Is Percentage', help='Whether this indicator is a percentage')

    # Status and metadata
    is_active = fields.Boolean('Is Active', default=True)
    reporting_frequency = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually')
    ], string='Reporting Frequency', default='monthly')

    # Related to assessments
    assessment_line_ids = fields.One2many('esg.assessment.line', 'indicator_id', 'Assessment Lines')

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code, framework_id)', 'Indicator code must be unique per framework.')
    ]

    @api.constrains('min_acceptable_value', 'max_acceptable_value')
    def _check_value_range(self):
        """Ensure min value is not greater than max value"""
        for record in self:
            if (record.min_acceptable_value and record.max_acceptable_value and
                record.min_acceptable_value > record.max_acceptable_value):
                raise ValidationError("Minimum acceptable value cannot be greater than maximum acceptable value.")


class ESGAssessmentLine(models.Model):
    """
    ESG Assessment Line - individual indicator scores within an assessment
    """
    _name = 'esg.assessment.line'
    _description = 'ESG Assessment Line'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    assessment_id = fields.Many2one('esg.assessment', 'ESG Assessment', required=True, ondelete='cascade')
    indicator_id = fields.Many2one('esg.indicator', 'ESG Indicator', required=True)
    actual_value = fields.Float('Actual Value', required=True)
    target_value = fields.Float('Target Value', related='indicator_id.target_value')
    baseline_value = fields.Float('Baseline Value', related='indicator_id.baseline_value')
    variance = fields.Float('Variance', compute='_compute_variance', store=True)

    # Performance metrics
    performance_score = fields.Float('Performance Score (0-100)', compute='_compute_performance_score', store=True)
    achievement_percentage = fields.Float('Achievement %', compute='_compute_achievement_percentage', store=True)

    # Data source and validation
    data_source = fields.Char('Data Source')
    verification_status = fields.Selection([
        ('unverified', 'Unverified'),
        ('self_verified', 'Self Verified'),
        ('third_party_verified', 'Third Party Verified'),
        ('certified', 'Certified')
    ], string='Verification Status', default='unverified')

    collection_date = fields.Date('Collection Date', default=fields.Date.context_today)
    collected_by = fields.Many2one('res.users', 'Collected By', default=lambda self: self.env.user)

    @api.depends('actual_value', 'target_value')
    def _compute_variance(self):
        """Compute variance from target"""
        for record in self:
            if record.target_value:
                record.variance = record.actual_value - record.target_value
            else:
                record.variance = 0.0

    @api.depends('actual_value', 'target_value', 'baseline_value')
    def _compute_performance_score(self):
        """Compute performance score based on achievement of target"""
        for record in self:
            if record.target_value:
                achievement_ratio = record.actual_value / record.target_value if record.target_value != 0 else 0
                # Convert to 0-100 scale where 1:1 ratio = 70 points, exceeding target gives bonus
                record.performance_score = min(100, max(0, 70 * achievement_ratio))
            else:
                # Use baseline as reference if no target
                if record.baseline_value:
                    achievement_ratio = record.actual_value / record.baseline_value if record.baseline_value != 0 else 0
                    record.performance_score = min(100, max(0, 70 * achievement_ratio))
                else:
                    record.performance_score = 50  # Neutral score if no baseline

    @api.depends('actual_value', 'target_value')
    def _compute_achievement_percentage(self):
        """Compute achievement percentage"""
        for record in self:
            if record.target_value:
                record.achievement_percentage = (record.actual_value / record.target_value) * 100 if record.target_value != 0 else 0
            else:
                record.achievement_percentage = 0.0

    @api.constrains('actual_value')
    def _check_value_range(self):
        """Check if value is within acceptable range"""
        for record in self:
            indicator = record.indicator_id
            if (indicator.min_acceptable_value and record.actual_value < indicator.min_acceptable_value):
                raise ValidationError(f"Actual value {record.actual_value} is below minimum acceptable value {indicator.min_acceptable_value} for {indicator.name}")
            if (indicator.max_acceptable_value and record.actual_value > indicator.max_acceptable_value):
                raise ValidationError(f"Actual value {record.actual_value} exceeds maximum acceptable value {indicator.max_acceptable_value} for {indicator.name}")