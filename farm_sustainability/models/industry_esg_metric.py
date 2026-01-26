from odoo import models, fields, api
from odoo.exceptions import ValidationError

class IndustryESGMetric(models.Model):
    """
    Specific ESG metrics for industry models
    """
    _name = 'farm.sustainability.industry.esg.metric'
    _description = 'Industry ESG Metric'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    model_id = fields.Many2one('farm.sustainability.industry.esg.model', 'Industry Model', required=True, ondelete='cascade')
    metric_name = fields.Char('Metric Name', required=True)
    metric_type = fields.Selection([
        ('environmental', 'Environmental'),
        ('social', 'Social'),
        ('governance', 'Governance')
    ], string='Metric Type', required=True)
    metric_category = fields.Char('Metric Category', help='Category within the ESG type')
    description = fields.Text('Description')
    unit_of_measurement = fields.Char('Unit of Measurement', required=True)
    data_collection_method = fields.Selection([
        ('automated', 'Automated Collection'),
        ('manual_survey', 'Manual Survey'),
        ('third_party', 'Third Party Report'),
        ('estimation', 'Estimation'),
        ('hybrid', 'Hybrid Method')
    ], string='Data Collection Method')
    frequency = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually')
    ], string='Reporting Frequency', default='annually')
    target_value = fields.Float('Target Value')
    baseline_value = fields.Float('Baseline Value')
    current_value = fields.Float('Current Value')
    achievement_percentage = fields.Float('Achievement %', compute='_compute_achievement_percentage', store=True)
    weight_in_esg_score = fields.Float('Weight in ESG Score (%)', default=10.0,
                                       help='Percentage weight of this metric in the overall ESG score')
    reporting_standard = fields.Char('Reporting Standard Reference',
                                     help='Reference to specific reporting standard requirement')
    verification_method = fields.Selection([
        ('internal_audit', 'Internal Audit'),
        ('external_audit', 'External Audit'),
        ('third_party', 'Third Party Verification'),
        ('self_report', 'Self Reporting')
    ], string='Verification Method')
    responsible_department = fields.Many2one('hr.department', 'Responsible Department')
    data_source = fields.Char('Data Source')
    notes = fields.Text('Notes')

    @api.depends('current_value', 'target_value')
    def _compute_achievement_percentage(self):
        """Compute achievement percentage for the metric"""
        for record in self:
            if record.target_value and record.target_value != 0:
                record.achievement_percentage = (record.current_value / record.target_value) * 100
            else:
                record.achievement_percentage = 0.0

    @api.constrains('weight_in_esg_score')
    def _check_weight_range(self):
        """Ensure weight is between 0 and 100"""
        for record in self:
            if record.weight_in_esg_score < 0 or record.weight_in_esg_score > 100:
                raise ValidationError("Weight in ESG score must be between 0 and 100.")