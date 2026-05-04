from odoo import models, fields, api
from odoo.exceptions import ValidationError
import math


class ESGDataGovernance(models.Model):
    """
    US-086-05: ESG 数据治理与质量控制 (ESG Data Governance & Quality Control)
    ESG Data Governance for ensuring data integrity, accuracy, and auditability
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

    # Enhanced quality control fields
    data_completeness_percentage = fields.Float('Data Completeness (%)', help='Percentage of required fields filled')
    data_accuracy_validation = fields.Boolean('Accuracy Validated', help='Whether data accuracy has been validated')
    validation_rules_applied = fields.Text('Validation Rules Applied', help='List of rules applied during validation')
    data_profiling_report = fields.Text('Data Profiling Report', help='Analysis of data patterns and anomalies')
    quality_monitoring_enabled = fields.Boolean('Quality Monitoring Enabled', default=True)
    next_quality_check = fields.Datetime('Next Quality Check', help='When to run the next automated quality check')
    data_steward = fields.Many2one('res.users', 'Data Steward', help='Person responsible for data governance')
    data_impact_analysis = fields.Text('Data Impact Analysis', help='Analysis of what would be affected if data is changed')
    data_retention_policy_applied = fields.Boolean('Retention Policy Applied', help='Whether retention policy has been enforced')
    retention_cleanup_date = fields.Datetime('Retention Cleanup Date', help='When the data will be automatically cleaned up')

    # Automated quality control fields
    automated_quality_alerts_enabled = fields.Boolean('Automated Alerts Enabled', default=True)
    last_quality_alert_date = fields.Datetime('Last Quality Alert Date', help='When the last quality alert was raised')
    quality_issue_severity = fields.Selection([
        'low', 'medium', 'high', 'critical'
    ], string='Quality Issue Severity', help='Severity level of quality issues')
    quality_validation_rules = fields.Text('Quality Validation Rules', help='Custom validation rules for this data')
    data_quality_history = fields.Text('Quality History', help='Historical quality scores and issues')

    # Data integrity fields
    checksum = fields.Char('Checksum', help='Data integrity checksum')
    data_origin_verification = fields.Boolean('Origin Verified', help='Whether data origin has been verified')
    data_transformation_log = fields.Text('Transformation Log', help='Log of all data transformations')
    sensitive_data_identified = fields.Boolean('Sensitive Data Identified', help='Whether sensitive data was identified in this record')
    privacy_compliance_status = fields.Selection([
        'compliant', 'non_compliant', 'requires_review'
    ], string='Privacy Compliance Status', help='Privacy compliance status of the data')

    # Data lineage extensions
    upstream_data_sources = fields.Text('Upstream Data Sources', help='Sources of data that feed into this record')
    downstream_consumers = fields.Text('Downstream Consumers', help='Systems/processes that consume this data')
    data_flow_diagram = fields.Text('Data Flow Diagram', help='Visual representation of data flow')

    @api.model
    def create(self, vals):
        """Override create to update data retention cleanup date"""
        if 'data_retention_years' in vals:
            from datetime import datetime, timedelta
            retention_years = vals['data_retention_years']
            if retention_years > 0:
                cleanup_date = datetime.now() + timedelta(days=retention_years * 365)
                vals['retention_cleanup_date'] = cleanup_date
        return super().create(vals)

    def write(self, vals):
        """Override write to update retention cleanup date when retention years change"""
        if 'data_retention_years' in vals:
            retention_years = vals['data_retention_years']
            if retention_years > 0:
                from datetime import datetime, timedelta
                cleanup_date = datetime.now() + timedelta(days=retention_years * 365)
                vals['retention_cleanup_date'] = cleanup_date
        return super().write(vals)

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
            # Enhanced validation logic with comprehensive checks
            quality_score = 100  # Start with perfect score

            # Calculate data completeness percentage
            total_fields = 0
            filled_fields = 0

            # Check required fields
            if record.name:
                filled_fields += 1
            total_fields += 1

            if record.data_source:
                filled_fields += 1
            total_fields += 1

            if record.data_type:
                filled_fields += 1
            total_fields += 1

            if record.collection_method:
                filled_fields += 1
            total_fields += 1

            if record.collection_date:
                filled_fields += 1
            total_fields += 1

            if record.data_owner:
                filled_fields += 1
            total_fields += 1

            if total_fields > 0:
                record.data_completeness_percentage = (filled_fields / total_fields) * 100
                # Deduct points for incompleteness
                completeness_deduction = (total_fields - filled_fields) * 5  # 5 points per missing field
                quality_score -= completeness_deduction
            else:
                record.data_completeness_percentage = 0

            # Reduce score for missing critical fields
            if not record.data_owner:
                quality_score -= 10
            if not record.data_lineage:
                quality_score -= 5
            if record.validation_status == 'invalid':
                quality_score -= 20

            # Check for origin verification
            if not record.data_origin_verification:
                quality_score -= 5

            # Check for security classification
            if not record.data_security_classification:
                quality_score -= 3

            # Check for audit trail
            if not record.audit_trail_enabled:
                quality_score -= 5

            # Ensure score doesn't go below 0
            record.data_quality_score = max(0, quality_score)
            record.validation_status = 'validated' if quality_score >= 70 else 'requires_review'

            # Update last updated timestamp
            record.last_updated = fields.Datetime.now()

            # Set severity based on quality score
            if quality_score >= 90:
                record.quality_issue_severity = 'low'
            elif quality_score >= 70:
                record.quality_issue_severity = 'medium'
            elif quality_score >= 50:
                record.quality_issue_severity = 'high'
            else:
                record.quality_issue_severity = 'critical'

    def action_run_data_profiling(self):
        """Run data profiling analysis to identify patterns and anomalies"""
        for record in self:
            profiling_report = []

            # Analyze data type consistency
            profiling_report.append(f"Data Type: {record.data_type}")
            profiling_report.append(f"Collection Method: {record.collection_method}")
            profiling_report.append(f"Security Classification: {record.data_security_classification}")

            # Check for potential anomalies
            if not record.data_lineage:
                profiling_report.append("WARNING: No data lineage information provided")
            if record.data_completeness_percentage < 80:
                profiling_report.append(f"WARNING: Data completeness is low ({record.data_completeness_percentage}%)")
            if record.validation_status == 'invalid':
                profiling_report.append("CRITICAL: Data marked as invalid")
            if not record.data_owner:
                profiling_report.append("WARNING: No data owner assigned")

            # Add impact analysis
            impact_analysis = f"Potential impact if modified: {record.data_type} data for {record.data_source}"
            profiling_report.append(impact_analysis)

            record.data_profiling_report = '\n'.join(profiling_report)

    def action_assign_data_steward(self):
        """Assign data steward to records"""
        # This is a placeholder method - in a real implementation,
        # you would use business logic to assign stewards
        for record in self:
            if not record.data_steward:
                # Default to current user if no steward assigned
                record.data_steward = self.env.user

    def action_schedule_quality_check(self, days_ahead=7):
        """Schedule the next quality check"""
        from datetime import datetime, timedelta
        next_check = datetime.now() + timedelta(days=days_ahead)

        for record in self:
            record.next_quality_check = next_check

    def action_enforce_retention_policy(self):
        """Enforce data retention policy"""
        for record in self:
            record.data_retention_policy_applied = True
            # The cleanup date is automatically calculated during creation/updates

    def action_generate_checksum(self):
        """Generate integrity checksum for data"""
        import hashlib

        for record in self:
            # Create a string representation of key data fields
            data_string = f"{record.name}{record.data_source}{record.data_type}{record.collection_date}{record.data_quality_score}"
            checksum = hashlib.md5(data_string.encode()).hexdigest()
            record.checksum = checksum

    def action_validate_accuracy(self):
        """Run accuracy validation specific to data type"""
        for record in self:
            # Placeholder for accuracy validation logic
            # In a real implementation, accuracy validation would depend on the specific data type
            accuracy_validated = True

            # For example, for numerical data types, we might check for outliers
            # For categorical data, we might validate against controlled vocabularies
            if record.data_type in ['environmental', 'financial']:
                # For environmental or financial data, check against expected ranges
                # (This would be implemented based on specific business rules)
                record.data_accuracy_validation = accuracy_validated
            else:
                record.data_accuracy_validation = True