from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ESGFramework(models.Model):
    """
    Base ESG Framework model to define ESG standards and frameworks
    """
    _name = 'esg.framework'
    _description = 'ESG Framework'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Framework Name', required=True)
    code = fields.Char('Framework Code', required=True, copy=False)
    description = fields.Text('Description')
    framework_type = fields.Selection([
        ('environmental', 'Environmental'),
        ('social', 'Social'),
        ('governance', 'Governance'),
        ('combined', 'Combined ESG')
    ], string='Framework Type', required=True)
    standards_body = fields.Char('Standards Body', help='Organization that maintains this framework')
    version = fields.Char('Version')
    effective_date = fields.Date('Effective Date')
    expiry_date = fields.Date('Expiry Date')
    is_active = fields.Boolean('Is Active', default=True)
    compliance_level = fields.Selection([
        ('basic', 'Basic'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('leadership', 'Leadership')
    ], string='Compliance Level', default='basic')

    # Related ESG indicators
    indicator_ids = fields.One2many('esg.indicator', 'framework_id', 'ESG Indicators')

    _code_unique = models.Constraint(
        'UNIQUE(code)',
        'Framework code must be unique.'
    )


class ESGAssessment(models.Model):
    """
    Base ESG Assessment model to track ESG performance assessments
    """
    _name = 'esg.assessment'
    _description = 'ESG Assessment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Assessment Name', required=True)
    assessment_date = fields.Date('Assessment Date', required=True, default=fields.Date.context_today)
    assessment_type = fields.Selection([
        ('environmental', 'Environmental'),
        ('social', 'Social'),
        ('governance', 'Governance'),
        ('combined', 'Combined ESG')
    ], string='Assessment Type', required=True)
    framework_id = fields.Many2one('esg.framework', 'ESG Framework')
    assessment_period = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semi_annually', 'Semi-Annually'),
        ('annually', 'Annually')
    ], string='Assessment Period', default='annually')
    year = fields.Integer('Year', default=lambda self: fields.Date.context_today(self).year)

    assessed_entity_type = fields.Selection([
        ('company', 'Company'),
        ('farm', 'Farm'),
        ('operation', 'Operation'),
        ('product', 'Product'),
        ('process', 'Process')
    ], string='Assessed Entity Type', required=True)

    assessed_entity_id = fields.Reference([
        ('res.company', 'Company'),
        ('farm.location', 'Farm Location'),
        ('mrp.production', 'Production Process'),
        ('product.product', 'Product'),
    ], string='Assessed Entity', help='The entity being assessed')

    overall_esg_score = fields.Float('Overall ESG Score (0-100)', compute='_compute_overall_esg_score', store=True)
    assessment_status = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('validated', 'Validated'),
        ('archived', 'Archived')
    ], string='Assessment Status', default='draft')

    # Detailed scores
    environmental_score = fields.Float('Environmental Score (0-100)')
    social_score = fields.Float('Social Score (0-100)')
    governance_score = fields.Float('Governance Score (0-100)')

    # Assessment metadata
    assessor_id = fields.Many2one('res.users', 'Assessor', default=lambda self: self.env.user)
    assessment_method = fields.Selection([
        ('self_assessment', 'Self Assessment'),
        ('third_party', 'Third Party Assessment'),
        ('hybrid', 'Hybrid Assessment')
    ], string='Assessment Method', default='self_assessment')
    certification_body = fields.Char('Certification Body')

    # Related ESG targets
    target_ids = fields.Many2many('esg.target', string='Related Targets')

    @api.depends('environmental_score', 'social_score', 'governance_score')
    def _compute_overall_esg_score(self):
        """Compute overall ESG score as weighted average"""
        for record in self:
            scores = [s for s in [record.environmental_score, record.social_score, record.governance_score] if s is not None]
            if scores:
                record.overall_esg_score = sum(scores) / len(scores)
            else:
                record.overall_esg_score = 0.0

    def action_start_assessment(self):
        """Start the assessment process"""
        for record in self:
            record.assessment_status = 'in_progress'

    def action_complete_assessment(self):
        """Complete the assessment"""
        for record in self:
            record.assessment_status = 'completed'

    @api.model
    def create(self, vals):
        """Override create to ensure proper status"""
        if 'assessment_status' not in vals:
            vals['assessment_status'] = 'draft'
        return super().create(vals)