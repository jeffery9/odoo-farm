from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ESGReportCustomization(models.Model):
    """
    US-086-06: 利益相关者 ESG 报告定制化 (Stakeholder ESG Report Customization)
    Customizable ESG reports for different stakeholder groups
    """
    _name = 'farm.esg.report.customization'
    _description = 'ESG Report Customization for Stakeholders'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Report Template Name', required=True)
    report_type = fields.Selection([
        ('regulatory', 'Regulatory/Compliance'),
        ('investor', 'Investor Relations'),
        ('customer', 'Customer Transparency'),
        ('internal', 'Internal Management'),
        ('public', 'Public Disclosure'),
        ('sustainability', 'Sustainability Report'),
        ('climate', 'Climate Risk Report'),
        ('social', 'Social Impact Report'),
        ('governance', 'Governance Report'),
    ], string='Report Type', required=True)

    stakeholder_group = fields.Selection([
        ('investors', 'Investors'),
        ('regulators', 'Regulators'),
        ('customers', 'Customers'),
        ('employees', 'Employees'),
        ('community', 'Local Community'),
        ('suppliers', 'Suppliers'),
        ('partners', 'Business Partners'),
        ('media', 'Media'),
        ('general_public', 'General Public'),
    ], string='Target Stakeholder Group', required=True)

    report_format = fields.Selection([
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('dashboard', 'Dashboard'),
        ('html', 'HTML/Web'),
        ('api', 'API/JSON'),
        ('presentation', 'Presentation'),
    ], string='Output Format', default='pdf')

    report_language = fields.Selection([
        ('zh_CN', '中文'),
        ('en_US', 'English'),
        ('es_ES', 'Español'),
        ('fr_FR', 'Français'),
        ('ja_JP', '日本語'),
    ], string='Report Language', default='zh_CN')

    report_sections = fields.Text('Included Sections', help='JSON structure defining which ESG sections to include')
    custom_metrics = fields.Text('Custom Metrics', help='Additional custom metrics specific to stakeholder needs')
    data_filters = fields.Text('Data Filters', help='Filters to apply to the data for this report')
    report_logo = fields.Binary('Custom Logo', help='Custom logo for this stakeholder group')
    brand_colors = fields.Char('Brand Colors', help='Brand colors for this report (hex codes)')
    report_recipients = fields.Many2many('res.partner', string='Report Recipients')

    # Report scheduling and automation
    auto_generation = fields.Boolean('Auto Generation', help='Whether to auto-generate this report')
    generation_frequency = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually'),
    ], string='Generation Frequency', help='How often to auto-generate this report')

    last_generated = fields.Datetime('Last Generated', help='When the report was last generated')
    next_scheduled_generation = fields.Datetime('Next Scheduled Generation', help='When to generate the report next')
    is_active = fields.Boolean('Is Active', default=True)

    # Content customization
    custom_header = fields.Text('Custom Header Content')
    custom_footer = fields.Text('Custom Footer Content')
    executive_summary = fields.Text('Executive Summary Template')
    visualization_types = fields.Text('Visualization Types', help='Preferred chart/graph types for this stakeholder')

    # Access control
    allowed_users = fields.Many2many('res.users', string='Allowed Users',
                                   help='Users who can access this report template')
    report_access_level = fields.Selection([
        ('public', 'Public'),
        ('internal', 'Internal Only'),
        ('confidential', 'Confidential'),
        ('restricted', 'Restricted Access'),
    ], string='Access Level', default='internal')

    # ESG data integration
    environmental_data_included = fields.Boolean('Include Environmental Data', default=True)
    social_data_included = fields.Boolean('Include Social Data', default=True)
    governance_data_included = fields.Boolean('Include Governance Data', default=True)
    kpi_included = fields.Boolean('Include KPIs', default=True)
    compliance_data_included = fields.Boolean('Include Compliance Data', default=True)

    # Report generation methods
    def action_generate_report(self):
        """Generate the customized report based on template settings"""
        # This is a placeholder method - in a real implementation,
        # this would generate the actual report based on the template settings
        for record in self:
            # Simulate report generation
            record.last_generated = fields.Datetime.now()

            # Calculate next scheduled generation if auto-generation is enabled
            if record.auto_generation and record.generation_frequency:
                from datetime import datetime, timedelta
                current_time = datetime.now()

                if record.generation_frequency == 'daily':
                    next_gen = current_time + timedelta(days=1)
                elif record.generation_frequency == 'weekly':
                    next_gen = current_time + timedelta(weeks=1)
                elif record.generation_frequency == 'monthly':
                    # Next month same day
                    import calendar
                    days_in_month = calendar.monthrange(current_time.year, current_time.month)[1]
                    next_gen = current_time + timedelta(days=days_in_month)
                elif record.generation_frequency == 'quarterly':
                    # Next quarter (3 months)
                    next_gen = current_time + timedelta(days=90)
                else:  # annually
                    next_gen = current_time + timedelta(days=365)

                record.next_scheduled_generation = next_gen

            # In a real implementation, this would generate the actual report
            # based on the template configuration
            message = f"Custom {record.stakeholder_group} {record.report_type} report generated successfully"
            record.message_post(body=message)

    @api.model
    def schedule_report_generation(self):
        """Scheduled method to generate reports that are due"""
        current_time = fields.Datetime.now()
        reports_to_generate = self.search([
            ('auto_generation', '=', True),
            ('is_active', '=', True),
            ('next_scheduled_generation', '<=', current_time)
        ])

        for report in reports_to_generate:
            report.action_generate_report()

    def action_preview_report(self):
        """Preview the report before full generation"""
        for record in self:
            message = f"Previewing {record.name} report for {record.stakeholder_group}"
            record.message_post(body=message)
            # In a real implementation, this would show a preview
            # of what the report would look like

    def action_export_template(self):
        """Export this report template for reuse"""
        for record in self:
            message = f"Exporting template: {record.name}"
            record.message_post(body=message)
            # In a real implementation, this would export the template
            # in a reusable format

    def action_apply_filters(self):
        """Apply data filters for this report"""
        for record in self:
            # In a real implementation, this would apply the filters
            # defined in the data_filters field to the ESG data
            message = f"Applied filters to report: {record.name}"
            record.message_post(body=message)

    @api.constrains('report_sections')
    def _check_report_sections(self):
        """Validate the JSON structure of report sections"""
        import json
        for record in self:
            if record.report_sections:
                try:
                    sections = json.loads(record.report_sections)
                    if not isinstance(sections, list) and not isinstance(sections, dict):
                        raise ValidationError(_("Report sections must be a valid JSON array or object"))
                except json.JSONDecodeError:
                    raise ValidationError(_("Report sections must be valid JSON format"))

    @api.constrains('custom_metrics')
    def _check_custom_metrics(self):
        """Validate the JSON structure of custom metrics"""
        import json
        for record in self:
            if record.custom_metrics:
                try:
                    metrics = json.loads(record.custom_metrics)
                    if not isinstance(metrics, list) and not isinstance(metrics, dict):
                        raise ValidationError(_("Custom metrics must be a valid JSON array or object"))
                except json.JSONDecodeError:
                    raise ValidationError(_("Custom metrics must be valid JSON format"))

    @api.constrains('data_filters')
    def _check_data_filters(self):
        """Validate the JSON structure of data filters"""
        import json
        for record in self:
            if record.data_filters:
                try:
                    filters = json.loads(record.data_filters)
                    if not isinstance(filters, dict):
                        raise ValidationError(_("Data filters must be a valid JSON object"))
                except json.JSONDecodeError:
                    raise ValidationError(_("Data filters must be valid JSON format"))