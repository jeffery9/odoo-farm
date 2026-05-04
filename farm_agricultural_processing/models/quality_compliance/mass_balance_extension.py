# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class FarmProcessingProductionMassBalanceExtension(models.Model):
    """
    Extension to Processing ISL Production Model for Mass Balance - US-037-13
    """
    _inherit = 'farm.processing.production'

    # Mass balance specific fields extending the existing ISL model
    mass_balance_name = fields.Char('Balance Check No.')
    total_input_qty = fields.Float('Total Input Quantity', required=True)
    total_output_qty = fields.Float('Total Output Quantity', required=True)
    total_loss_qty = fields.Float('Total Process Loss', required=True)
    theoretical_output_qty = fields.Float('Theoretical Output Quantity')

    # Variance tracking
    balance_variance = fields.Float('Balance Variance', compute='_compute_variance', store=True)
    variance_percentage = fields.Float('Variance Percentage', compute='_compute_variance', store=True)

    # Tolerance settings
    max_variance_tolerance = fields.Float('Max Variance Tolerance (+/-)', default=0.01, help='Maximum acceptable variance (e.g., 0.01 for 1%)')

    # Compliance status
    is_balanced = fields.Boolean('Is Balanced', compute='_compute_balance_status', store=True)
    compliance_status = fields.Selection([
        ('compliant', 'Compliant'),
        ('warning', 'Warning'),
        ('non_compliant', 'Non-Compliant'),
    ], string='Compliance Status', compute='_compute_balance_status', store=True)

    @api.depends('total_input_qty', 'total_output_qty', 'theoretical_output_qty')
    def _compute_variance(self):
        for record in self:
            record.balance_variance = record.total_output_qty - record.theoretical_output_qty
            if record.total_input_qty > 0:
                record.variance_percentage = abs((record.balance_variance / record.total_input_qty) * 100)
            else:
                record.variance_percentage = 0.0

    @api.depends('balance_variance', 'max_variance_tolerance', 'variance_percentage')
    def _compute_balance_status(self):
        for record in self:
            if record.variance_percentage <= (record.max_variance_tolerance * 100):
                record.is_balanced = True
                record.compliance_status = 'compliant'
            elif record.variance_percentage <= (record.max_variance_tolerance * 200):  # double tolerance warning
                record.is_balanced = False
                record.compliance_status = 'warning'
            else:
                record.is_balanced = False
                record.compliance_status = 'non_compliant'

    def action_mass_balance_check(self):
        """Perform mass balance check and update compliance status"""
        for record in self:
            # Update compliance status based on current values
            record._compute_balance_status()
            # Log the balance check
            _logger.info(f"Mass balance check performed for {record.mass_balance_name}: Status={record.compliance_status}, Variance={record.balance_variance}")


class FarmProcessingProductionMultiOutputExtension(models.Model):
    """
    Extension to Processing ISL Production Model for Multi-Output - US-037-01
    """
    _inherit = 'farm.processing.production'

    # Multi-output processing fields
    is_multi_output = fields.Boolean('Is Multi-Output Process', default=False)
    multi_output_line_ids = fields.One2many('agri.processing.multi.output.line', 'production_id', string='Multi-Output Product Lines')

    def action_calculate_multi_output(self):
        """Calculate and validate multi-output results according to [US-037-01] Multi-output Processing"""
        for record in self:
            total_output = sum([line.product_qty for line in record.multi_output_line_ids])
            if record.final_output_qty != total_output:
                record.final_output_qty = total_output
                _logger.info(f"Multi-output calculation adjusted for {record.name}")


class AgriProcessingMultiOutputLine(models.Model):
    """
    Multi-Output Product Lines for Agricultural Processing - US-037-01
    """
    _name = 'agri.processing.multi.output.line'
    _description = 'Multi-Output Product Lines for Agricultural Processing'
    multi_output_id = fields.Many2one('agri.processing.multi.output', string='Multi-Output Record')
    production_id = fields.Many2one('farm.processing.production', string='Production Order', ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    product_qty = fields.Float('Quantity', required=True)
    output_qty = fields.Float('Output Quantity')
    output_percentage = fields.Float('Output Percentage')
    component_ratio = fields.Float('Component Ratio')
    product_uom_id = fields.Many2one('uom.uom', string='Unit of Measure', required=True)
    output_sequence = fields.Integer('Output Sequence')

    # Quality attributes for each output
    quality_grade = fields.Selection([
        ('a', 'Grade A / Premium'),
        ('b', 'Grade B / Standard'),
        ('c', 'Grade C / Processing'),
        ('loss', 'Loss/Waste')
    ], string='Quality Grade')

    # Compliance tracking per output
    is_compliant = fields.Boolean('Is Compliant', default=True)
    compliance_notes = fields.Text('Compliance Notes')


class FarmProcessingProductionAttributeInheritanceExtension(models.Model):
    """
    Extension to Processing ISL Production Model for Attribute Inheritance - US-037-02
    """
    _inherit = 'farm.processing.production'

    # Incremental labeling system fields
    incremental_label_base = fields.Char('Incremental Label Base', help='Base part of incremental label')
    incremental_label_sequence = fields.Integer('Incremental Label Sequence', default=1)

    # Attribute inheritance control
    inherit_attributes_from_raw_materials = fields.Boolean('Inherit Attributes from Raw Materials', default=True)
    inherited_attributes = fields.Text('Inherited Attributes (JSON)', help='JSON format of inherited attributes')


class FarmProcessingProductionActiveIngredientExtension(models.Model):
    """
    Extension to Processing ISL Production Model for Active Ingredient Standardization - US-037-11
    """
    _inherit = 'farm.processing.production'

    # Active ingredient analysis for standardization processing
    active_ingredient_content = fields.Float('Active Ingredient Content (%)')
    active_ingredient_target = fields.Float('Target Active Ingredient Content (%)')
    active_ingredient_variance = fields.Float('Active Ingredient Variance', compute='_compute_active_ingredient_variance', store=True)

    @api.depends('active_ingredient_content', 'active_ingredient_target')
    def _compute_active_ingredient_variance(self):
        for record in self:
            record.active_ingredient_variance = record.active_ingredient_content - record.active_ingredient_target

    def _validate_active_ingredient_content(self):
        """[US-037-11] Active Ingredient Standardization for compliance"""
        for record in self:
            if record.active_ingredient_content <= 0:
                raise ValidationError(_("Active ingredient content must be greater than 0%"))
            if record.active_ingredient_variance and abs(record.active_ingredient_variance) > 5:  # 5% tolerance
                raise ValidationError(_("Active ingredient variance exceeds tolerance of 5%: %.2f%%") % record.active_ingredient_variance)


class FarmProcessingProductionAllergenExtension(models.Model):
    """
    Extension to Processing ISL Production Model for Allergen Control - US-037-14
    """
    _inherit = 'farm.processing.production'

    # Allergen tracking and control
    contains_allergens = fields.Boolean('Contains Allergens', default=False)
    allergen_list = fields.Char('Allergen List', help='Comma-separated list of allergens')
    allergen_control_status = fields.Selection([
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('non_compliant', 'Non-Compliant'),
    ], string='Allergen Control Status', default='pending')

    # Equipment allergen cleaning tracking
    equipment_cleaning_required = fields.Boolean('Equipment Cleaning Required', default=False)
    equipment_cleaned_by = fields.Many2one('res.users', string='Equipment Cleaned By')
    equipment_cleaned_date = fields.Datetime('Equipment Cleaned On')
    equipment_cleaning_certificate = fields.Char('Cleaning Certificate No.')

    def action_verify_allergen_control(self):
        """Verify allergen control status for the production order"""
        for record in self:
            if record.contains_allergens:
                if record.allergen_list:
                    record.allergen_control_status = 'verified'
                else:
                    record.allergen_control_status = 'non_compliant'
            else:
                record.allergen_control_status = 'verified'


class FarmProcessingProductionGmpExtension(models.Model):
    """
    Extension to Processing ISL Production Model for GMP Environmental Monitoring - US-037-15
    """
    _inherit = 'farm.processing.production'

    # GMP environmental monitoring
    gmp_temperature_monitoring = fields.Boolean('Temperature Monitoring', default=True)
    gmp_humidity_monitoring = fields.Boolean('Humidity Monitoring', default=True)

    # Environmental parameters
    environmental_monitoring_line_ids = fields.One2many('agri.processing.environmental.monitoring.line', 'production_id', string='Environmental Monitoring Lines')

    def action_gmp_compliance_check(self):
        """Perform GMP compliance check for environmental parameters"""
        for record in self:
            non_compliant_readings = record.environmental_monitoring_line_ids.filtered(
                lambda r: not r.is_compliant
            )
            if non_compliant_readings:
                raise ValidationError(_(
                    "GMP Compliance Failed: Found %d non-compliant environmental readings" % len(non_compliant_readings)
                ))


class AgriProcessingEnvironmentalMonitoringLine(models.Model):
    """
    Environmental Monitoring Lines for GMP Compliance - US-037-15
    """
    _name = 'agri.processing.environmental.monitoring.line'
    _description = 'Environmental Monitoring Lines for GMP Compliance'

    production_id = fields.Many2one('farm.processing.production', string='Production Order', ondelete='cascade')
    monitoring_date = fields.Datetime('Monitoring Date', required=True)
    temperature = fields.Float('Temperature (℃)')
    humidity = fields.Float('Humidity (%)')

    # Temperature range validation
    temperature_min = fields.Float('Min Temperature', default=18.0)
    temperature_max = fields.Float('Max Temperature', default=25.0)

    # Humidity range validation
    humidity_min = fields.Float('Min Humidity (%)', default=45.0)
    humidity_max = fields.Float('Max Humidity (%)', default=65.0)

    # Compliance status
    is_compliant = fields.Boolean('Is Compliant', compute='_compute_compliance', store=True)
    compliance_notes = fields.Text('Compliance Notes')

    @api.depends('temperature', 'humidity', 'temperature_min', 'temperature_max', 'humidity_min', 'humidity_max')
    def _compute_compliance(self):
        for record in self:
            temp_compliant = (record.temperature_min <= record.temperature <= record.temperature_max) if record.temperature else True
            humidity_compliant = (record.humidity_min <= record.humidity <= record.humidity_max) if record.humidity else True
            record.is_compliant = temp_compliant and humidity_compliant