# -*- coding: utf-8 -*-
from odoo import models, fields, api

class FarmSeasonalBom(models.Model):
    _name = 'farm.seasonal.bom'
    _description = 'Seasonal BOM'
    name = fields.Char("Name")
    product_tmpl_id = fields.Many2one('product.template', string='Product')
    season_id = fields.Many2one('farm.season', string='Season')
    bom_id = fields.Many2one('mrp.bom', string='Base BOM')
    season_name = fields.Char("Season Name")
    season_start_date = fields.Date("Start Date")
    season_end_date = fields.Date("End Date")
    version_number = fields.Char("Version Number")
    version_name = fields.Char("Version Name")
    season_description = fields.Text("Description")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], string='State', default='draft')
    is_seasonal_adjustment = fields.Boolean("Seasonal Adjustment")
    
    seasonal_material_ids = fields.One2many('farm.seasonal.bom.line', 'seasonal_bom_id', string='Seasonal Material Lines')
    seasonal_parameter_ids = fields.One2many('farm.seasonal.parameter.line', 'seasonal_bom_id', string='Seasonal Parameter Lines')
    
    base_yield_factor = fields.Float("Base Yield Factor")
    seasonal_yield_factor = fields.Float("Seasonal Yield Factor")
    
    def action_activate(self):
        return True
    
    def action_deactivate(self):
        return True
    
    def action_view_seasonal_materials(self):
        return True
    
    def action_view_seasonal_parameters(self):
        return True

class FarmSeason(models.Model):
    _name = 'farm.season'
    _description = 'Farm Season'
    name = fields.Char("Season Name")

class FarmSeasonalBomLine(models.Model):
    _name = 'farm.seasonal.bom.line'
    _description = 'Seasonal BOM Line'
    seasonal_bom_id = fields.Many2one('farm.seasonal.bom')
    product_id = fields.Many2one('product.product', string='Product')
    base_qty = fields.Float("Base Qty")
    seasonal_qty = fields.Float("Seasonal Qty")
    qty_difference = fields.Float("Difference", compute='_compute_qty_diff')
    adjustment_reason = fields.Char("Reason")

    @api.depends('base_qty', 'seasonal_qty')
    def _compute_qty_diff(self):
        for rec in self:
            rec.qty_difference = rec.seasonal_qty - rec.base_qty

class FarmSeasonalBomMaterial(models.Model):
    _name = 'farm.seasonal.bom.material'
    _description = 'Seasonal BOM Material'
    seasonal_bom_id = fields.Many2one('farm.seasonal.bom')
    product_id = fields.Many2one('product.product')
    base_qty = fields.Float("Base Qty")
    seasonal_qty = fields.Float("Seasonal Qty")
    qty_difference = fields.Float("Difference")
    adjustment_reason = fields.Char("Reason")

class FarmSeasonalParameterLine(models.Model):
    _name = 'farm.seasonal.parameter.line'
    _description = 'Seasonal Parameter Line'
    seasonal_bom_id = fields.Many2one('farm.seasonal.bom')
    parameter_id = fields.Many2one('agri.ai.parameter', string='Parameter')
    parameter_name = fields.Char(related='parameter_id.name', string='Parameter Name', readonly=True)
    base_value = fields.Float("Base Value")
    seasonal_value = fields.Float("Seasonal Value")
    value_difference = fields.Float("Difference", compute='_compute_value_diff')
    adjustment_reason = fields.Char("Reason")
    target_value = fields.Float("Target Value")
    unit_of_measure = fields.Char("Unit")

    @api.depends('base_value', 'seasonal_value')
    def _compute_value_diff(self):
        for rec in self:
            rec.value_difference = rec.seasonal_value - rec.base_value

class FarmSeasonalBomParameter(models.Model):
    _name = 'farm.seasonal.bom.parameter'
    _description = 'Seasonal BOM Parameter'
    seasonal_bom_id = fields.Many2one('farm.seasonal.bom')
    parameter_id = fields.Many2one('agri.ai.parameter')
    parameter_name = fields.Char("Parameter Name")
    base_value = fields.Float("Base Value")
    seasonal_value = fields.Float("Seasonal Value")
    value_difference = fields.Float("Difference")
    adjustment_reason = fields.Char("Reason")
    unit_of_measure = fields.Char("Unit")

class AgriAiParameter(models.Model):
    _name = 'agri.ai.parameter'
    _description = 'Agri AI Parameter'
    name = fields.Char("Parameter Name")

class FarmProcessingStep(models.Model):
    _name = 'farm.processing.step'
    _description = 'Processing Step'
    _order = 'sequence, id'
    
    name = fields.Char("Step Name")
    production_id = fields.Many2one('mrp.production', string='Production Order')
    
    sequence = fields.Integer("Sequence", default=10)
    step_name = fields.Char("Step Name")
    step_type = fields.Selection([
        ('washing', 'Washing'),
        ('cutting', 'Cutting'),
        ('packing', 'Packaging'),
        ('cooling', 'Cooling'),
        ('sorting', 'Sorting')
    ], string='Step Type')
    
    input_qty = fields.Float("Input Qty")
    output_qty = fields.Float("Output Qty")
    loss_qty = fields.Float("Loss Qty")
    temperature = fields.Float("Temperature")
    humidity = fields.Float("Humidity")
    ph_level = fields.Float("pH Level")
    
    state = fields.Selection([('draft', 'Draft')], string='State', default='draft')

class AgriProcessingFormulaAutoCorrection(models.Model):
    _name = 'agri.processing.formula.auto.correction'
    _description = 'Formula Auto Correction'
    name = fields.Char("Correction ID")
    state = fields.Selection([('draft', 'Draft')], string='State', default='draft')

class AgriProcessingMultiOutput(models.Model):
    _name = 'agri.processing.multi.output'
    _description = 'Multi Output Management'
    name = fields.Char("Output ID")
    bom_id = fields.Many2one('mrp.bom', string='BOM')
    production_id = fields.Many2one('mrp.production', string='Production Order')
    input_qty = fields.Float("Input Qty")
    total_output_qty = fields.Float("Total Output Qty")
    yield_rate = fields.Float("Yield Rate")
    traceability_id = fields.Char("Traceability ID")
    output_line_ids = fields.One2many('agri.processing.multi.output.line', 'multi_output_id', string='Output Lines')
    state = fields.Selection([('draft', 'Draft')], string='State', default='draft')

class AgriProcessingMultiOutputLine(models.Model):
    _name = 'agri.processing.multi.output.line'
    _description = 'Multi Output Line'
    multi_output_id = fields.Many2one('agri.processing.multi.output')
    product_id = fields.Many2one('product.product', string='Product')
    product_qty = fields.Float("Quantity")
    quality_grade = fields.Selection([('grade_a', 'Grade A'), ('grade_b', 'Grade B')], string='Grade')

class AgriProcessingAttributeInheritance(models.Model):
    _name = 'agri.processing.attribute.inheritance'
    _description = 'Attribute Inheritance'
    name = fields.Char("Inheritance ID")
    source_product_id = fields.Many2one('product.product', string='Source Product')
    target_product_id = fields.Many2one('product.product', string='Target Product')
    inherits_organic = fields.Boolean("Inherit Organic Status")
    inherits_biodynamic = fields.Boolean("Inherit Biodynamic Status")
    inherits_geo_origin = fields.Boolean("Inherit Geo Origin")
    inherits_harvest_date = fields.Boolean("Inherit Harvest Date")
    mapping_logic = fields.Text("Mapping Logic")
    processing_method = fields.Char("Processing Method")
    special_features = fields.Char("Special Features")
    attribute_json = fields.Text("Attribute JSON")
    inherited_attributes = fields.Text("Inherited Attributes")
    incremental_attributes = fields.Text("Incremental Attributes")
    active = fields.Boolean("Active", default=True)
    state = fields.Selection([('draft', 'Draft')], string='State', default='draft')

class AgriProcessingActiveIngredient(models.Model):
    _name = 'agri.processing.active.ingredient'
    _description = 'Active Ingredient Management'
    name = fields.Char("Ingredient ID")
    ai_name = fields.Char("AI Name")
    product_tmpl_id = fields.Many2one('product.template', string='Product')
    target_ai_content = fields.Float("Target AI Content")
    actual_ai_content = fields.Float("Actual AI Content")
    min_ai_content = fields.Float("Min AI Content")
    max_ai_content = fields.Float("Max AI Content")
    correction_factor = fields.Float("Correction Factor")
    is_content_valid = fields.Boolean("Is Content Valid")
    ai_measurement_unit = fields.Char("Unit")
    methodology = fields.Text("Methodology")
    adjustment_factor = fields.Float("Adjustment Factor")
    adjusted_dosage = fields.Float("Adjusted Dosage")
    notes = fields.Text("Notes")
    state = fields.Selection([('draft', 'Draft')], string='State', default='draft')

class AgriProcessingAllergenControl(models.Model):
    _name = 'agri.processing.allergen.control'
    _description = 'Allergen Control'
    name = fields.Char("Control ID")
    production_id = fields.Many2one('mrp.production', string='Production Order')
    workcenter_id = fields.Many2one('mrp.workcenter', string='Workcenter')
    allergen_conflict_detected = fields.Boolean("Conflict Detected")
    cleaning_required = fields.Boolean("Cleaning Required")
    cleaning_performed = fields.Boolean("Cleaning Performed")
    contains_allergens = fields.Boolean("Contains Allergens")
    allergen_details = fields.Text("Allergen Details")
    all_allergens = fields.Boolean("All Allergens")
    previous_allergens = fields.Text("Previous Allergens")
    cleaning_procedure = fields.Text("Cleaning Procedure")
    previous_production_id = fields.Many2one('mrp.production', string='Previous Production')
    allergen_risk_score = fields.Float("Risk Score")
    cleaning_verification_result = fields.Selection([('pass', 'Pass'), ('fail', 'Fail')], string='Cleaning Result')
    cleaner_id = fields.Many2one('res.users', string='Cleaner')
    cleaning_by = fields.Many2one('res.users', string='Cleaned By')
    cleaning_date = fields.Date("Cleaning Date")
    cleaning_verification_by = fields.Many2one('res.users', string='Verified By')
    cleaning_verification_date = fields.Date("Verification Date")
    verification_id = fields.Many2one('res.users', string='Verifier')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('cleaning_required', 'Cleaning Required'),
        ('cleaning_performed', 'Cleaning Performed'),
        ('passed', 'Passed')
    ], string='State', default='draft')

    def action_execute_recall_simulation(self):
        return True

class AgriProcessingGmpMonitoring(models.Model):
    _name = 'agri.processing.gmp.monitoring'
    _description = 'GMP Monitoring'
    
    name = fields.Char("Monitoring ID", required=True)
    production_id = fields.Many2one('mrp.production', string='Production Order')
    monitoring_date = fields.Date("Monitoring Date")
    recorded_by = fields.Many2one('res.users', string='Recorded By')
    is_environment_compliant = fields.Boolean("Is Environment Compliant")
    
    temperature_min = fields.Float("Temperature Min")
    temperature_max = fields.Float("Temperature Max")
    temperature_avg = fields.Float("Temperature Avg")
    
    humidity_min = fields.Float("Humidity Min")
    humidity_max = fields.Float("Humidity Max")
    humidity_avg = fields.Float("Humidity Avg")
    
    air_pressure_diff = fields.Float("Air Pressure Difference")
    particle_count_05um = fields.Float("Particle Count 0.5um")
    particle_count_5um = fields.Float("Particle Count 5um")
    environmental_alerts = fields.Text("Environmental Alerts")
    bmr_content = fields.Text("BMR Content")
    notes = fields.Text("Notes")
    
    validated_by = fields.Many2one('res.users', string='Validated By')
    validation_date = fields.Date("Validation Date")
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], string='State', default='draft')

class AgriProcessingBatchIntegrity(models.Model):
    _name = 'agri.processing.batch.integrity'
    _description = 'Batch Integrity'
    name = fields.Char("Integrity ID")
    state = fields.Selection([('draft', 'Draft')], string='State', default='draft')

class AgriProcessingYieldOptimizer(models.Model):
    _name = 'agri.processing.yield.optimizer'
    _description = 'Yield Optimizer'
    name = fields.Char("Optimizer ID")
    state = fields.Selection([('draft', 'Draft')], string='State', default='draft')

class AgriProcessingEnergyEfficiency(models.Model):
    _name = 'agri.processing.energy.efficiency'
    _description = 'Energy Efficiency'
    name = fields.Char("Efficiency ID")
    state = fields.Selection([('draft', 'Draft')], string='State', default='draft')

class AgriProcessingLabelCompliance(models.Model):
    _name = 'agri.processing.label.compliance'
    _description = 'Label Compliance'
    
    name = fields.Char("Compliance ID", required=True)
    product_id = fields.Many2one('product.product', string='Product')
    production_batch_id = fields.Many2one('stock.lot', string='Production Batch')
    is_approved = fields.Boolean("Is Approved")
    reviewed_by = fields.Many2one('res.users', string='Reviewed By')
    reviewed_date = fields.Date("Reviewed Date")
    export_compliant = fields.Boolean("Export Compliant")
    
    sc_license_required = fields.Boolean("SC License Required")
    sc_license_number = fields.Char("SC License Number")
    is_license_compliant = fields.Boolean("Is License Compliant")
    
    allergen_warning_required = fields.Boolean("Allergen Warning Required")
    health_claim_approved = fields.Boolean("Health Claim Approved")
    
    generated_label_content = fields.Text("Generated Label Content")
    label_template_id = fields.Many2one('ir.ui.view', string='Label Template')
    nutrition_composition = fields.Text("Nutrition Composition")
    allergen_warnings = fields.Text("Allergen Warnings")
    health_claims_text = fields.Text("Health Claims Text")
    
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], string='State', default='draft')

class AgriProcessingColdChainLog(models.Model):
    _name = 'agri.processing.cold.chain.log'
    _description = 'Cold Chain Log'
    name = fields.Char("Log ID")
    state = fields.Selection([('draft', 'Draft')], string='State', default='draft')

class AgriProcessingTraceabilityMatrix(models.Model):
    _name = 'agri.processing.traceability.matrix'
    _description = 'Traceability Matrix'
    name = fields.Char("Matrix ID")
    state = fields.Selection([('draft', 'Draft')], string='State', default='draft')

class AgriProcessingWastageReport(models.Model):
    _name = 'agri.processing.wastage.report'
    _description = 'Wastage Report'
    name = fields.Char("Report ID")
    state = fields.Selection([('draft', 'Draft')], string='State', default='draft')
