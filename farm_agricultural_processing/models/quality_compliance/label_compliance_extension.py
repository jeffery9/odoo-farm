# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class FarmProcessingProductionLabelComplianceExtension(models.Model):
    """
    Extension to Processing ISL Production Model for Label Compliance - US-037-17
    """
    _inherit = 'farm.processing.production'

    # Nutrition labeling compliance fields
    requires_nutrition_labeling = fields.Boolean('Requires Nutrition Labeling', default=False)
    nutrition_facts = fields.Text('Nutrition Facts (JSON format)')
    allergen_declaration = fields.Text('Allergen Declaration')
    net_weight = fields.Float('Net Weight')
    net_weight_uom_id = fields.Many2one('uom.uom', string='Net Weight UOM')

    # Label compliance status
    label_compliance_status = fields.Selection([
        ('pending', 'Pending'),
        ('compliant', 'Compliant'),
        ('non_compliant', 'Non-Compliant'),
    ], string='Label Compliance Status', compute='_compute_label_compliance_status', store=True)

    # Regulatory compliance
    fda_compliant = fields.Boolean('FDA Compliant', default=False)
    eu_compliant = fields.Boolean('EU Compliant', default=False)
    local_regulations_compliant = fields.Boolean('Local Regulations Compliant', default=False)

    @api.depends('requires_nutrition_labeling', 'nutrition_facts', 'allergen_declaration', 'net_weight')
    def _compute_label_compliance_status(self):
        """Compute label compliance status based on required fields"""
        for record in self:
            if record.requires_nutrition_labeling:
                # Check if all required label fields are filled
                if record.nutrition_facts and record.allergen_declaration and record.net_weight:
                    record.label_compliance_status = 'compliant'
                else:
                    record.label_compliance_status = 'non_compliant'
            else:
                record.label_compliance_status = 'compliant'


class FarmProcessingProductionHaccpExtension(models.Model):
    """
    Extension to Processing ISL Production Model for HACCP - US-037-18
    """
    _inherit = 'farm.processing.production'

    # HACCP plan fields
    is_haccp_controlled = fields.Boolean('Is HACCP Controlled Process', default=False)
    # haccp_plan_id = fields.Many2one('quality.control.standard', string='HACCP Plan')
    haccp_critical_control_points = fields.Text('HACCP Critical Control Points')

    # HACCP compliance tracking
    haccp_monitoring_line_ids = fields.One2many('agri.processing.haccp.monitoring.line', 'production_id', string='HACCP Monitoring Lines')
    haccp_verification_line_ids = fields.One2many('agri.processing.haccp.verification.line', 'production_id', string='HACCP Verification Lines')

    # Compliance status
    haccp_compliance_status = fields.Selection([
        ('pending', 'Pending'),
        ('compliant', 'Compliant'),
        ('non_compliant', 'Non-Compliant'),
        ('action_required', 'Action Required'),
    ], string='HACCP Compliance Status', compute='_compute_haccp_compliance_status', store=True)

    # Critical limits
    haccp_critical_limits = fields.Text('Critical Limits (JSON)')

    @api.depends('haccp_monitoring_line_ids', 'haccp_verification_line_ids')
    def _compute_haccp_compliance_status(self):
        """Compute HACCP compliance status"""
        for record in self:
            if not record.is_haccp_controlled:
                record.haccp_compliance_status = 'compliant'
            else:
                non_compliant_monitoring = record.haccp_monitoring_line_ids.filtered(lambda r: not r.is_in_spec)
                if non_compliant_monitoring:
                    record.haccp_compliance_status = 'action_required'
                else:
                    record.haccp_compliance_status = 'compliant'

    def action_haccp_plan_check(self):
        """Execute HACCP plan checks for the production order"""
        for record in self:
            if record.is_haccp_controlled and record.haccp_plan_id:
                # Create monitoring records based on HACCP plan
                # Use inspection_criteria from quality control standard as basis for CCPs
                if record.haccp_plan_id.inspection_criteria:
                    # Create a single monitoring line based on the inspection criteria
                    self.env['agri.processing.haccp.monitoring.line'].create({
                        'production_id': record.id,
                        'ccp_name': 'HACCP Monitoring from Standard',
                        'critical_limit_min': record.haccp_plan_id.quality_threshold,  # Use quality threshold as min
                        'critical_limit_max': 100.0,  # Default max value
                    })


class AgriProcessingHaccpMonitoringLine(models.Model):
    """
    HACCP Monitoring Lines - US-037-18
    """
    _name = 'agri.processing.haccp.monitoring.line'
    _description = 'HACCP Monitoring Lines'

    production_id = fields.Many2one('farm.processing.production', string='Production Order', ondelete='cascade')
    ccp_name = fields.Char('Critical Control Point', required=True)
    monitoring_date = fields.Datetime('Monitoring Date', default=fields.Datetime.now)
    measured_value = fields.Float('Measured Value')
    critical_limit_min = fields.Float('Critical Limit Min')
    critical_limit_max = fields.Float('Critical Limit Max')
    is_in_spec = fields.Boolean('Is In Specification', compute='_compute_is_in_spec', store=True)
    corrective_action_taken = fields.Text('Corrective Action Taken')

    @api.depends('measured_value', 'critical_limit_min', 'critical_limit_max')
    def _compute_is_in_spec(self):
        for record in self:
            if record.measured_value is not False and record.critical_limit_min is not False and record.critical_limit_max is not False:
                record.is_in_spec = record.critical_limit_min <= record.measured_value <= record.critical_limit_max
            else:
                record.is_in_spec = False


class AgriProcessingHaccpVerificationLine(models.Model):
    """
    HACCP Verification Lines - US-037-18
    """
    _name = 'agri.processing.haccp.verification.line'
    _description = 'HACCP Verification Lines'

    production_id = fields.Many2one('farm.processing.production', string='Production Order', ondelete='cascade')
    verification_date = fields.Datetime('Verification Date', default=fields.Datetime.now)
    verification_type = fields.Selection([
        ('internal_audit', 'Internal Audit'),
        ('external_audit', 'External Audit'),
        ('equipment_calibration', 'Equipment Calibration'),
        ('record_review', 'Record Review'),
    ], string='Verification Type', required=True)
    verified_by = fields.Many2one('res.users', string='Verified By')
    is_verified = fields.Boolean('Is Verified', default=False)
    verification_notes = fields.Text('Verification Notes')