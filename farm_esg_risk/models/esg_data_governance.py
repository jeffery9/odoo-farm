from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ESGDataGovernance(models.Model):
    """
    US-52-03: ESG数据治理与审计追踪
    ESG Data Governance for ensuring data integrity and auditability
    """
    _name = 'farm.esg.data.governance'
    _description = 'ESG Data Governance'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Data Governance Record', required=True)
    data_source = fields.Char('Data Source', help='System or process that generated the data')
    data_type = fields.Selection([
        'environmental', 'social', 'governance', 'financial', 'operational'
    ], string='Data Type', required=True)
    collection_method = fields.Selection([
        'automated', 'manual', 'sensor', 'third_party', 'survey', 'other'
    ], string='Collection Method', required=True)
    collection_date = fields.Datetime('Collection Date', required=True)
    data_owner = fields.Many2one('res.users', 'Data Owner')
    data_quality_score = fields.Float('Data Quality Score', help='Score from 0-100 for data quality')
    validation_status = fields.Selection([
        'pending', 'validated', 'invalid', 'requires_review'
    ], string='Validation Status', default='pending')
    data_retention_years = fields.Integer('Data Retention (Years)', default=7)
    access_control_list = fields.Text('Access Control List', help='List of users/groups with access')
    anonymization_applied = fields.Boolean('Anonymization Applied', help='Whether data has been anonymized')
    data_backup_status = fields.Selection([
        ('none', 'No Backup'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly')
    ], string='Backup Status', default='daily')
    data_security_classification = fields.Selection([
        ('public', 'Public'),
        ('internal', 'Internal'),
        ('confidential', 'Confidential'),
        ('restricted', 'Restricted')
    ], string='Security Classification', default='internal')
    audit_trail_enabled = fields.Boolean('Audit Trail Enabled', default=True)
    data_lineage = fields.Text('Data Lineage', help='Trace of data transformations')
    data_quality_issues = fields.Text('Data Quality Issues')
    remediation_status = fields.Selection([
        'open', 'in_progress', 'resolved', 'wont_fix'
    ], string='Remediation Status', default='open')
    last_updated = fields.Datetime('Last Updated', default=fields.Datetime.now)

    @api.model
    def check_data_quality_issues(self):
        """Check for data quality issues across all records"""
        records = self.search([])

        issues = []
        for record in records:
            if record.data_quality_score < 70:  # Threshold for poor quality
                issues.append({
                    'record_id': record.id,
                    'name': record.name,
                    'quality_score': record.data_quality_score,
                    'type': record.data_type,
                    'owner': record.data_owner.name if record.data_owner else 'Unknown'
                })

        return issues

    def action_validate_data(self):
        """Validate data quality for records"""
        for record in self:
            # Basic validation logic
            quality_score = 100  # Start with perfect score

            # Reduce score for missing critical fields
            if not record.data_owner:
                quality_score -= 10
            if not record.data_lineage:
                quality_score -= 5
            if record.validation_status == 'invalid':
                quality_score -= 20

            # Ensure score doesn't go below 0
            record.data_quality_score = max(0, quality_score)
            record.validation_status = 'validated' if quality_score >= 70 else 'requires_review'