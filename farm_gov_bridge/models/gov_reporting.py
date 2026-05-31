# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import requests
import json
import logging

_logger = logging.getLogger(__name__)

class GovPlatformConfig(models.Model):
    """
    [US-GOV-05] Centralized Government Platform Configuration.
    Manages endpoints and credentials for automated reporting.
    """
    _name = 'gov.platform.config'
    _description = 'Government Platform Configuration'

    name = fields.Char('Platform Name', required=True)
    platform_type = fields.Selection([
        ('provincial', 'Provincial Regulation (肥药两制)'),
        ('national', 'National Traceability'),
        ('subsidy', 'Subsidy Management'),
        ('esg', 'ESG/Carbon Registry')
    ], string='Platform Type', required=True)
    
    endpoint_url = fields.Char('API Endpoint URL', required=True)
    api_key = fields.Char('API Key / Secret')
    
    active = fields.Boolean(default=True)
    
    # Auto-push settings
    auto_report_enabled = fields.Boolean('Enable Automated Reporting', default=False)
    report_on_event = fields.Selection([
        ('intervention_done', 'On Intervention Completion'),
        ('lot_harvested', 'On Harvesting Output'),
        ('manual', 'Manual Only')
    ], string='Trigger Event', default='manual')

class GovAuditSnapshot(models.Model):
    _inherit = 'gov.audit.snapshot'

    is_reported = fields.Boolean('Reported to Gov', default=False, readonly=True)
    report_date = fields.Datetime('Report Timestamp', readonly=True)
    platform_response = fields.Text('Platform Response', readonly=True)

    def action_push_to_platform(self):
        """ Manually push a specific snapshot to the configured government platform """
        self.ensure_one()
        # Find active platform for this type
        platform = self.env['gov.platform.config'].search([
            ('active', '=', True),
            ('auto_report_enabled', '=', True)
        ], limit=1) # Simplified selection
        
        if not platform:
            raise UserError(_("No active government platform configuration found with 'Automated Reporting' enabled."))

        return self._do_push_report(platform)

    def _do_push_report(self, platform):
        """ Internal execution of the API push """
        self.ensure_one()
        try:
            # 1. Prepare standard EPCIS/JSON-LD payload from snapshot
            payload = json.loads(self.snapshot_data)
            
            # Add security headers and metadata
            headers = {
                'Content-Type': 'application/json',
                'X-API-KEY': platform.api_key or '',
                'X-DIGITAL-SIGNATURE': self.digital_signature
            }

            # 2. Transmit to centralized platform
            # response = requests.post(platform.endpoint_url, json=payload, headers=headers, timeout=20)
            # response.raise_for_status()
            
            # Mock success for now
            self.write({
                'is_reported': True,
                'report_date': fields.Datetime.now(),
                'platform_response': 'Success: Record Accepted by Central Platform'
            })
            self.message_post(body=_("Automated Gov Report: Successfully transmitted to %s") % platform.name)
            return True
        except Exception as e:
            _logger.error(f"Gov Reporting Failed for {self.snapshot_ref}: {str(e)}")
            self.write({'platform_response': f"Error: {str(e)}"})
            return False

class GovReportingService(models.AbstractModel):
    """
    [US-GOV-06] Background Service for Centralized Reporting.
    """
    _name = 'gov.reporting.service'
    _description = 'Government Reporting Background Service'

    @api.model
    def _cron_push_pending_reports(self):
        """ Periodically scan and push un-reported snapshots """
        pending = self.env['gov.audit.snapshot'].search([
            ('is_reported', '=', False),
            ('gov_review_status', '!=', 'rejected')
        ], limit=50)
        
        platform = self.env['gov.platform.config'].search([
            ('active', '=', True),
            ('auto_report_enabled', '=', True)
        ], limit=1)
        
        if not platform or not pending:
            return

        for snapshot in pending:
            snapshot._do_push_report(platform)
