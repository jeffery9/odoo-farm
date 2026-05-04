from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import json
import logging
import requests
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class FarmGovernmentPlatformConfig(models.Model):
    """
    Configuration for government regulatory platforms
    """
    _name = 'farm.government.platform.config'
    _description = 'Government Platform Configuration'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Platform Name', required=True)
    code = fields.Char('Platform Code', required=True, copy=False)
    api_endpoint = fields.Char('API Endpoint', required=True, help='Base URL for the government platform API')
    api_username = fields.Char('API Username', help='Username for API authentication')
    api_password = fields.Char('API Password', help='Password for API authentication')
    api_key = fields.Char('API Key', help='API key for authentication')
    data_format = fields.Selection([
        ('json', 'JSON'),
        ('xml', 'XML'),
        ('csv', 'CSV'),
    ], string='Data Format', default='json', required=True)
    active = fields.Boolean('Active', default=True)
    submission_frequency = fields.Selection([
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ], string='Submission Frequency', default='daily')
    last_submission = fields.Datetime('Last Submission')
    next_scheduled_submission = fields.Datetime('Next Scheduled Submission')
    description = fields.Text('Description')

    def action_test_connection(self):
        """Test connection to the government platform"""
        for config in self:
            try:
                # Create a simple test payload
                test_data = {
                    'test': True,
                    'timestamp': fields.Datetime.now(),
                    'platform_code': config.code
                }

                headers = {
                    'Content-Type': 'application/json',
                    'User-Agent': 'Odoo-Government-Integration/1.0'
                }

                # Add authentication headers based on platform configuration
                if config.api_username and config.api_password:
                    # Basic authentication
                    import base64
                    credentials = base64.b64encode(f'{config.api_username}:{config.api_password}'.encode()).decode()
                    headers['Authorization'] = f'Basic {credentials}'
                elif config.api_key:
                    # API key authentication
                    headers['Authorization'] = f'Bearer {config.api_key}'
                    # Or could be: headers['X-API-Key'] = config.api_key

                response = requests.post(
                    f"{config.api_endpoint.rstrip('/')}/test",
                    json=test_data,
                    headers=headers,
                    timeout=30
                )

                if response.status_code in [200, 201]:
                    self.message_post(body=_(f"Successfully connected to {config.name}. Response: {response.text[:100]}..."))
                else:
                    raise UserError(f"Connection failed with status {response.status_code}: {response.text}")

            except Exception as e:
                _logger.error(f"Failed to connect to government platform {config.name}: {str(e)}")
                raise UserError(f"Connection test failed for {config.name}: {str(e)}")


class FarmGovernmentDataReport(models.Model):
    """
    Model to track regulatory data submissions to government platforms
    US-057-04: Government regulatory platform对接
    """
    _name = 'farm.government.data.report'
    _description = 'Government Data Report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'submission_date desc'

    name = fields.Char('Report Name', required=True, copy=False)
    platform_config_id = fields.Many2one('farm.government.platform.config', string='Government Platform', required=True)
    report_type = fields.Selection([
        ('environmental', 'Environmental Data'),
        ('production', 'Production Data'),
        ('compliance', 'Compliance Data'),
        ('financial', 'Financial Data'),
        ('other', 'Other Data'),
    ], string='Report Type', required=True)

    submission_date = fields.Datetime('Submission Date', default=fields.Datetime.now)
    submission_status = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending Submission'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('failed', 'Failed'),
    ], string='Submission Status', default='draft', tracking=True)

    data_payload = fields.Text('Data Payload', help='The actual data being submitted to the government platform')
    response_data = fields.Text('Response Data', help='Response received from the government platform')
    error_message = fields.Text('Error Message', help='Error details if submission failed')

    greenhouse_ids = fields.Many2many('farm.location',
                                      domain=[('is_greenhouse', '=', True)],
                                      string='Greenhouses',
                                      help='Greenhouses whose data is included in this report')

    start_date = fields.Datetime('Data Start Date', help='Start date for the data included in this report')
    end_date = fields.Datetime('Data End Date', help='End date for the data included in this report')

    data_summary = fields.Text('Data Summary', compute='_compute_data_summary', store=True, precompute=True)
    submission_attempts = fields.Integer('Submission Attempts', default=0)
    last_attempt_date = fields.Datetime('Last Attempt Date')

    @api.depends('greenhouse_ids', 'report_type', 'start_date', 'end_date')
    def _compute_data_summary(self):
        """Compute summary of data to be included in the report"""
        for record in self:
            if record.greenhouse_ids and record.start_date and record.end_date:
                # Count relevant records for summary
                summary_parts = []

                if record.report_type in ['environmental', 'production', 'compliance']:
                    # Environmental data summary
                    env_data = self._get_greenhouse_environmental_data(
                        record.greenhouse_ids,
                        record.start_date,
                        record.end_date
                    )

                    if env_data:
                        summary_parts.append(f"Environmental data for {len(record.greenhouse_ids)} greenhouses")
                        summary_parts.append(f"Period: {record.start_date} to {record.end_date}")
                        summary_parts.append(f"Records: {len(env_data)} data points")

                record.data_summary = "; ".join(summary_parts)
            else:
                record.data_summary = "No data summary available"

    def action_prepare_data(self):
        """Prepare the data payload for government submission"""
        for record in self:
            try:
                if record.report_type == 'environmental':
                    # Prepare environmental data from greenhouse sensors
                    data = self._prepare_environmental_data(record)
                elif record.report_type == 'production':
                    # Prepare production data
                    data = self._prepare_production_data(record)
                elif record.report_type == 'compliance':
                    # Prepare compliance data
                    data = self._prepare_compliance_data(record)
                else:
                    # Handle other data types
                    data = self._prepare_other_data(record)

                # Convert to the format required by the platform
                formatted_data = self._format_data_for_platform(data, record.platform_config_id)

                record.data_payload = json.dumps(formatted_data, default=str, indent=2)
                record.submission_status = 'pending'

            except Exception as e:
                _logger.error(f"Error preparing data for report {record.name}: {str(e)}")
                record.message_post(body=_(f"Error preparing data: {str(e)}"))
                raise ValidationError(f"Error preparing data for report {record.name}: {str(e)}")

    def _prepare_environmental_data(self, record):
        """Prepare environmental data from greenhouse sensors"""
        environmental_data = []

        for greenhouse in record.greenhouse_ids:
            # Get environmental readings for the specified period
            # This would typically come from IoT telemetry data
            env_readings = self.env['farm.location'].search([
                ('id', '=', greenhouse.id)
            ])

            if env_readings:
                # Create a record for each greenhouse with environmental data
                greenhouse_data = {
                    'greenhouse_id': greenhouse.id,
                    'greenhouse_name': greenhouse.name,
                    'location': greenhouse.display_name,
                    'environmental_readings': {
                        'temperature': greenhouse.current_temp,
                        'humidity': greenhouse.current_humidity,
                        'co2': greenhouse.current_co2,
                        'light_intensity': greenhouse.current_light,
                        'nutrient_ec': greenhouse.current_ec,
                        'nutrient_ph': greenhouse.current_ph,
                        'data_timestamp': fields.Datetime.now(),
                    },
                    'period_start': record.start_date,
                    'period_end': record.end_date,
                }
                environmental_data.append(greenhouse_data)

        return environmental_data

    def _prepare_production_data(self, record):
        """Prepare production data for government reporting"""
        # Placeholder for production data preparation
        # This would include yield data, harvest records, etc.
        production_data = []

        for greenhouse in record.greenhouse_ids:
            # This would typically involve more complex queries to get production data
            # from harvest records, yield tracking, etc.
            production_record = {
                'greenhouse_id': greenhouse.id,
                'greenhouse_name': greenhouse.name,
                'production_summary': {
                    # Add production-specific fields here
                },
                'period_start': record.start_date,
                'period_end': record.end_date,
            }
            production_data.append(production_record)

        return production_data

    def _prepare_compliance_data(self, record):
        """Prepare compliance data for government reporting"""
        # Placeholder for compliance data preparation
        # This would include audit trails, certification compliance, etc.
        compliance_data = []

        for greenhouse in record.greenhouse_ids:
            compliance_record = {
                'greenhouse_id': greenhouse.id,
                'greenhouse_name': greenhouse.name,
                'compliance_status': 'compliant',  # This would be calculated from actual compliance data
                'certifications': [],  # Actual certifications would be included here
                'period_start': record.start_date,
                'period_end': record.end_date,
            }
            compliance_data.append(compliance_record)

        return compliance_data

    def _prepare_other_data(self, record):
        """Prepare other types of data for government reporting"""
        # Placeholder for other data types
        return {'placeholder': True}

    def _format_data_for_platform(self, data, platform_config):
        """Format data according to the specific requirements of the government platform"""
        formatted_data = {
            'platform_code': platform_config.code,
            'report_type': self.report_type,
            'submission_timestamp': fields.Datetime.now(),
            'data_records': data,
            'format_version': '1.0'
        }

        # Apply platform-specific formatting if needed
        if platform_config.data_format == 'json':
            # JSON format - already in the right format
            pass
        elif platform_config.data_format == 'xml':
            # Would need to convert to XML here
            pass
        elif platform_config.data_format == 'csv':
            # Would need to convert to CSV here
            pass

        return formatted_data

    def action_submit_to_government(self):
        """Submit the prepared data to the government platform"""
        for record in self:
            if record.submission_status != 'pending':
                raise ValidationError(_("Only pending reports can be submitted. Current status: %s") % record.submission_status)

            if not record.data_payload:
                raise ValidationError(_("No data payload prepared. Please prepare data first."))

            try:
                # Increment submission attempts
                record.submission_attempts += 1
                record.last_attempt_date = fields.Datetime.now()

                # Parse the payload
                payload = json.loads(record.data_payload)

                # Prepare headers for the API call
                headers = {
                    'Content-Type': 'application/json',
                    'User-Agent': 'Odoo-Government-Integration/1.0'
                }

                # Add authentication based on platform configuration
                config = record.platform_config_id
                if config.api_username and config.api_password:
                    import base64
                    credentials = base64.b64encode(f'{config.api_username}:{config.api_password}'.encode()).decode()
                    headers['Authorization'] = f'Basic {credentials}'
                elif config.api_key:
                    headers['Authorization'] = f'Bearer {config.api_key}'

                # Make the API call to the government platform
                response = requests.post(
                    f"{config.api_endpoint.rstrip('/')}/submit",
                    json=payload,
                    headers=headers,
                    timeout=60  # 60 seconds timeout for potentially large payloads
                )

                # Process the response
                if response.status_code in [200, 201]:
                    record.response_data = response.text
                    record.submission_status = 'submitted'
                    record.message_post(body=_("Successfully submitted to government platform. Response: %s") % response.text[:200])

                    # Update the platform config with last submission time
                    config.last_submission = fields.Datetime.now()
                    next_time = fields.Datetime.now()
                    if config.submission_frequency == 'hourly':
                        next_time += timedelta(hours=1)
                    elif config.submission_frequency == 'daily':
                        next_time += timedelta(days=1)
                    elif config.submission_frequency == 'weekly':
                        next_time += timedelta(weeks=1)
                    elif config.submission_frequency == 'monthly':
                        # Move to next month (simplified - just add 30 days)
                        next_time += timedelta(days=30)

                    config.next_scheduled_submission = next_time
                else:
                    record.submission_status = 'failed'
                    record.error_message = f"HTTP {response.status_code}: {response.text}"
                    record.message_post(body=_("Submission failed. Status: %s, Response: %s") % (response.status_code, response.text[:200]))
                    _logger.error(f"Government submission failed for report {record.name}: {response.status_code} - {response.text}")

            except Exception as e:
                _logger.error(f"Error submitting report {record.name} to government platform: {str(e)}")
                record.submission_status = 'failed'
                record.error_message = str(e)
                record.message_post(body=_("Submission failed with error: %s") % str(e))
                raise ValidationError(_("Failed to submit report to government platform: %s") % str(e))

    def action_resubmit_failed(self):
        """Resubmit any failed reports"""
        failed_reports = self.filtered(lambda r: r.submission_status == 'failed')
        for report in failed_reports:
            report.submission_status = 'pending'
            report.action_submit_to_government()

    def _get_greenhouse_environmental_data(self, greenhouses, start_date, end_date):
        """Helper method to get environmental data for specified greenhouses in date range"""
        # This is a simplified implementation - in real usage, this would query
        # actual historical environmental data from IoT systems
        data_points = []

        for greenhouse in greenhouses:
            # Get recent environmental data for the greenhouse
            # In a real implementation, this would query historical telemetry data
            data_point = {
                'greenhouse_id': greenhouse.id,
                'greenhouse_name': greenhouse.name,
                'timestamp': fields.Datetime.now(),
                'temperature': greenhouse.current_temp,
                'humidity': greenhouse.current_humidity,
                'co2': greenhouse.current_co2,
                'light_intensity': greenhouse.current_light,
                'nutrient_ec': greenhouse.current_ec,
                'nutrient_ph': greenhouse.current_ph,
            }
            data_points.append(data_point)

        return data_points


class FarmLocation(models.Model):
    """Extend farm.location to include government reporting capabilities"""
    _inherit = 'farm.location'

    # Add fields for government reporting readiness
    regulatory_reporting_enabled = fields.Boolean('Regulatory Reporting Enabled',
                                                 help='Enable this greenhouse for government regulatory reporting')
    last_regulatory_sync = fields.Datetime('Last Regulatory Sync',
                                          help='Last time this greenhouse data was synchronized with government platform')

    def action_prepare_regulatory_data(self):
        """Prepare a regulatory report for this greenhouse"""
        # Create a new government data report for the selected greenhouse(s)
        report = self.env['farm.government.data.report'].create({
            'name': f'Regulatory Report - {self.name} - {fields.Datetime.now().strftime("%Y-%m-%d %H:%M")}',
            'report_type': 'environmental',
            'greenhouse_ids': [(6, 0, self.ids)],  # Many2many field
            'start_date': fields.Datetime.now() - timedelta(days=1),  # Last 24 hours
            'end_date': fields.Datetime.now(),
        })

        # Prepare the data for submission
        report.action_prepare_data()

        return {
            'type': 'ir.actions.act_window',
            'name': _('Government Data Report'),
            'res_model': 'farm.government.data.report',
            'res_id': report.id,
            'view_mode': 'form',
            'target': 'current',
        }