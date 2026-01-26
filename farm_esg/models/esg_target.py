from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ESGTarget(models.Model):
    """
    ESG Target model to define ESG goals and targets
    """
    _name = 'esg.target'
    _description = 'ESG Target'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Target Name', required=True)
    description = fields.Text('Description')
    category = fields.Selection([
        ('environmental', 'Environmental'),
        ('social', 'Social'),
        ('governance', 'Governance')
    ], string='Category', required=True)

    target_type = fields.Selection([
        ('reduction', 'Reduction Target'),
        ('improvement', 'Improvement Target'),
        ('compliance', 'Compliance Target'),
        ('certification', 'Certification Target'),
        ('benchmark', 'Benchmark Target')
    ], string='Target Type', required=True)

    # Target metrics
    baseline_value = fields.Float('Baseline Value', required=True)
    target_value = fields.Float('Target Value', required=True)
    current_value = fields.Float('Current Value', compute='_compute_current_value', store=True)
    unit_of_measurement = fields.Char('Unit of Measurement', required=True)

    # Timeline
    start_date = fields.Date('Start Date', required=True, default=fields.Date.context_today)
    target_date = fields.Date('Target Date', required=True)
    achieved_date = fields.Date('Achieved Date', readonly=True)

    # Progress tracking
    progress_percentage = fields.Float('Progress %', compute='_compute_progress_percentage', store=True)
    is_achieved = fields.Boolean('Is Achieved', compute='_compute_is_achieved', store=True)

    # Related framework and indicators
    framework_id = fields.Many2one('esg.framework', 'ESG Framework')
    related_indicator_ids = fields.Many2many('esg.indicator', string='Related Indicators')

    # Management
    responsible_user_id = fields.Many2one('res.users', 'Responsible Person')
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ], string='Priority', default='medium')
    status = fields.Selection([
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('partially_achieved', 'Partially Achieved'),
        ('achieved', 'Achieved'),
        ('deferred', 'Deferred'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='planned', required=True)

    # Stakeholder engagement
    stakeholder_ids = fields.Many2many('res.partner', string='Stakeholders')
    last_update = fields.Text('Last Update')

    @api.depends('current_value', 'baseline_value', 'target_value')
    def _compute_progress_percentage(self):
        """Compute target progress percentage based on values"""
        for record in self:
            if record.baseline_value != record.target_value:  # Avoid division by zero if baseline equals target
                if record.target_value > record.baseline_value:
                    # Improvement target (higher is better)
                    if record.current_value >= record.target_value:
                        record.progress_percentage = 100.0
                    elif record.current_value <= record.baseline_value:
                        record.progress_percentage = 0.0
                    else:
                        range_total = record.target_value - record.baseline_value
                        range_completed = record.current_value - record.baseline_value
                        record.progress_percentage = min(100.0, max(0.0, (range_completed / range_total) * 100.0))
                else:
                    # Reduction target (lower is better)
                    if record.current_value <= record.target_value:
                        record.progress_percentage = 100.0
                    elif record.current_value >= record.baseline_value:
                        record.progress_percentage = 0.0
                    else:
                        range_total = record.baseline_value - record.target_value
                        range_completed = record.baseline_value - record.current_value
                        record.progress_percentage = min(100.0, max(0.0, (range_completed / range_total) * 100.0))
            else:
                record.progress_percentage = 100.0 if record.current_value == record.target_value else 0.0

    @api.depends('current_value', 'target_value')
    def _compute_is_achieved(self):
        """Determine if the target has been achieved"""
        for record in self:
            if record.target_value > record.baseline_value:
                # Improvement target
                record.is_achieved = record.current_value >= record.target_value
            else:
                # Reduction target
                record.is_achieved = record.current_value <= record.target_value

    def _compute_current_value(self):
        """Compute current value - this is typically updated by business logic"""
        for record in self:
            # In a real implementation, this would be updated based on actual data
            # For now, we'll keep it as 0 or the baseline value
            record.current_value = record.baseline_value  # Default to baseline

    @api.constrains('start_date', 'target_date', 'baseline_value', 'target_value')
    def _check_dates_and_values(self):
        """Validate target dates and values"""
        for record in self:
            if record.start_date and record.target_date:
                if record.start_date >= record.target_date:
                    raise ValidationError("Target date must be after start date.")
            if record.baseline_value == record.target_value:
                raise ValidationError("Target value should be different from baseline value to provide meaningful target.")

    def action_update_current_value(self):
        """Manual action to update current value based on related indicators"""
        for record in self:
            if record.related_indicator_ids:
                # Calculate current value based on related indicator measurements
                latest_assessment_lines = self.env['esg.assessment.line'].search([
                    ('indicator_id', 'in', record.related_indicator_ids.ids),
                    ('collection_date', '<=', fields.Date.context_today(self)),
                ], order='collection_date desc', limit=len(record.related_indicator_ids))

                if latest_assessment_lines:
                    # Calculate average of related indicator values
                    avg_value = sum(latest_assessment_lines.mapped('actual_value')) / len(latest_assessment_lines)
                    record.current_value = avg_value

    def action_mark_achieved(self):
        """Mark target as achieved manually"""
        for record in self:
            if record.current_value >= record.target_value if record.target_value > record.baseline_value else record.current_value <= record.target_value:
                record.status = 'achieved'
                record.achieved_date = fields.Date.context_today(self)
            else:
                raise ValidationError(f"Target has not been achieved yet. Current value: {record.current_value}, Target: {record.target_value}")

    def action_track_progress(self):
        """Track progress by creating assessment lines"""
        for record in self:
            # This would typically be called by scheduled actions or business processes
            # For now, just update the current value if related indicators exist
            if record.related_indicator_ids:
                record._compute_current_value()


class ESGPerformanceReport(models.Model):
    """
    ESG Performance Report model for reporting and analytics
    """
    _name = 'esg.performance.report'
    _description = 'ESG Performance Report'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Report Name', required=True)
    report_date = fields.Date('Report Date', required=True, default=fields.Date.context_today)
    report_period = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semi_annually', 'Semi-Annually'),
        ('annually', 'Annually')
    ], string='Report Period', default='annually')
    year = fields.Integer('Year', default=lambda self: fields.Date.context_today(self).year)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)

    # ESG scores
    environmental_score = fields.Float('Environmental Score (0-100)')
    social_score = fields.Float('Social Score (0-100)')
    governance_score = fields.Float('Governance Score (0-100)')
    overall_esg_score = fields.Float('Overall ESG Score (0-100)', compute='_compute_overall_score', store=True)

    # Target achievement metrics
    total_targets = fields.Integer('Total Targets', compute='_compute_target_metrics')
    achieved_targets = fields.Integer('Achieved Targets', compute='_compute_target_metrics')
    achievement_rate = fields.Float('Achievement Rate %', compute='_compute_target_metrics')

    # Compliance metrics
    compliance_rate = fields.Float('Compliance Rate %')
    audit_findings = fields.Integer('Audit Findings')
    corrective_actions = fields.Integer('Corrective Actions Required')

    # Report content
    executive_summary = fields.Html('Executive Summary')
    key_achievements = fields.Html('Key Achievements')
    challenges = fields.Html('Challenges')
    improvement_plan = fields.Html('Improvement Plan')

    # Related records
    assessment_ids = fields.Many2many('esg.assessment', string='Related Assessments')
    target_ids = fields.Many2many('esg.target', string='Related Targets')

    @api.depends('environmental_score', 'social_score', 'governance_score')
    def _compute_overall_score(self):
        """Compute overall ESG score as weighted average"""
        for record in self:
            scores = [s for s in [record.environmental_score, record.social_score, record.governance_score] if s is not None]
            if scores:
                record.overall_esg_score = sum(scores) / len(scores)
            else:
                record.overall_esg_score = 0.0

    @api.depends('target_ids')
    def _compute_target_metrics(self):
        """Compute target-related metrics"""
        for record in self:
            if record.target_ids:
                record.total_targets = len(record.target_ids)
                achieved_targets = record.target_ids.filtered('is_achieved')
                record.achieved_targets = len(achieved_targets)
                record.achievement_rate = (record.achieved_targets / record.total_targets) * 100 if record.total_targets > 0 else 0.0
            else:
                record.total_targets = 0
                record.achieved_targets = 0
                record.achievement_rate = 0.0

    def action_generate_report(self):
        """Generate the ESG performance report based on current data"""
        for record in self:
            # This would typically aggregate data from various sources
            # For now, just update with the latest assessment data if available
            latest_assessments = self.env['esg.assessment'].search([
                ('assessment_date', '>=', fields.Date.start_of(record.report_date, 'year' if record.report_period == 'annually' else 'quarter')),
                ('assessment_date', '<=', fields.Date.end_of(record.report_date, 'year' if record.report_period == 'annually' else 'quarter')),
            ], order='assessment_date desc')

            if latest_assessments:
                record.assessment_ids = latest_assessments
                # Calculate average scores
                record.environmental_score = sum(latest_assessments.mapped('environmental_score')) / len(latest_assessments) if latest_assessments.mapped('environmental_score') else 0
                record.social_score = sum(latest_assessments.mapped('social_score')) / len(latest_assessments) if latest_assessments.mapped('social_score') else 0
                record.governance_score = sum(latest_assessments.mapped('governance_score')) / len(latest_assessments) if latest_assessments.mapped('governance_score') else 0

            # Link to related targets
            current_targets = self.env['esg.target'].search([
                ('start_date', '<=', record.report_date),
                ('target_date', '>=', record.report_date),
            ])
            record.target_ids = current_targets