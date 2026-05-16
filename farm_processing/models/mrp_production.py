# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class FarmQualityRejectionReason(models.Model):
    _name = 'farm.quality.rejection.reason'
    _description = 'Quality Rejection Reason'
    name = fields.Char("Reason")

class AgriQualityCheckExtension(models.Model):
    _inherit = 'agri.quality.check'

    production_id = fields.Many2one('mrp.production', string='Production Order')
    check_date = fields.Date("Check Date", default=fields.Date.context_today)
    check_type = fields.Selection([
        ('chemical', 'Chemical'),
        ('physical', 'Physical'),
        ('microbial', 'Microbial'),
        ('sensory', 'Sensory')
    ], string='Check Type')
    result = fields.Selection([
        ('pass', 'Pass'),
        ('fail', 'Fail'),
        ('none', 'Pending')
    ], string='Result', default='none')
    checker_id = fields.Many2one('res.users', string='Checker', default=lambda self: self.env.user)

class MrpProduction(models.Model):
    _name = 'mrp.production'
    _inherit = ['mrp.production', 'agri.quality.gate.mixin']

    sequence = fields.Integer("Sequence")
    is_agri_processing = fields.Boolean("Is Agri Processing")
    is_agri_processing_enabled = fields.Boolean("Agri Processing Enabled", compute='_compute_is_agri_processing_enabled')
    is_blind_mixing = fields.Boolean("Blind Mixing Mode")
    user_can_see_quantities = fields.Boolean("Can See Quantities")
    is_growth_order = fields.Boolean("Is Growth Order")
    is_haccp_compliant = fields.Boolean("HACCP Compliant")
    loss_approval_state = fields.Selection([('draft', 'Draft'), ('pending', 'Pending'), ('approved', 'Approved')], string='Loss Approval', default='draft')
    is_high_loss = fields.Boolean("High Loss Alert")
    total_output_qty = fields.Float("Total Output Qty")
    is_balanced = fields.Boolean("Mass Balanced")
    water_meter_start = fields.Float("Water Meter Start")
    water_meter_end = fields.Float("Water Meter End")
    electricity_meter_start = fields.Float("Electricity Meter Start")
    electricity_meter_end = fields.Float("Electricity Meter End")
    harvest_lot_ids = fields.Many2many('stock.lot', 'mrp_production_harvest_lot_rel', 'production_id', 'lot_id', string='Harvest Lots')
    additive_lot_ids = fields.Many2many('stock.lot', 'mrp_production_additive_lot_rel', 'production_id', 'lot_id', string='Additive Lots')
    traceability_id = fields.Char("Traceability ID")
    
    processing_type = fields.Selection([
        ('primary', 'Primary'),
        ('deep', 'Deep'),
        ('packaging', 'Packaging')
    ], string='Processing Type')
    process_mode = fields.Selection([
        ('manual', 'Manual'),
        ('automated', 'Automated'),
        ('hybrid', 'Hybrid')
    ], string='Process Mode', default='manual')
    process_status = fields.Selection([
        ('draft', 'Draft'),
        ('running', 'Running'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], string='Process Status', default='draft')
    is_process_locked = fields.Boolean("Process Locked")
    vintage_year = fields.Char("Vintage Year")
    brix_level = fields.Float("Brix Level")
    baking_temp = fields.Float("Baking Temp")
    baking_duration = fields.Float("Baking Duration")
    is_baked = fields.Boolean("Is Baked")
    proofing_time = fields.Float("Proofing Time")
    actual_yield = fields.Float("Actual Yield")
    process_temperature = fields.Float("Process Temperature")
    process_ph = fields.Float("Process pH")
    process_brix = fields.Float("Process Brix")
    process_proofing_time = fields.Float("Process Proofing Time")
    actual_duration = fields.Float("Actual Duration")
    moisture_content = fields.Float("Moisture Content")
    
    area_to_treat = fields.Float("Area to Treat")
    water_temp = fields.Float("Water Temp")
    dissolved_oxygen = fields.Float("Dissolved Oxygen")
    ph_level = fields.Float("PH Level")
    avg_individual_weight = fields.Float("Avg Weight")
    survival_rate = fields.Float("Survival Rate")
    initial_total_weight = fields.Float("Initial Total Weight")
    final_total_weight = fields.Float("Final Total Weight")
    fcr = fields.Float("FCR")
    energy_reading_start = fields.Float("Energy Reading Start")
    energy_reading_end = fields.Float("Energy Reading End")
    energy_reading_diff = fields.Float("Energy Reading Diff")
    energy_unit_price = fields.Float("Energy Unit Price")
    energy_meter_start = fields.Float("Energy Meter Start")
    energy_meter_end = fields.Float("Energy Meter End")
    energy_consumed = fields.Float("Energy Consumed")
    energy_consumption = fields.Float("Energy Consumption")
    energy_cost_total = fields.Monetary("Total Energy Cost (Processing)", currency_field='currency_id')
    total_energy_cost = fields.Monetary("Total Energy Cost", currency_field='currency_id')
    byproduct_cost_share_total = fields.Float("By-product Cost Share Total")
    finished_product_cost_share = fields.Float("Finished Product Cost Share")
    batch_execution_state = fields.Selection([
        ('draft', 'Draft'),
        ('running', 'Running'),
        ('paused', 'Paused'),
        ('completed', 'Completed')
    ], string='Batch State', default='draft')
    lock_reason = fields.Char("Lock Reason")
    scrap_qty = fields.Float("Scrap Qty")
    scrap_reason = fields.Char("Scrap Reason")
    yield_rate = fields.Float("Yield Rate")
    loss_rate = fields.Float("Loss Rate")
    quality_gate_status = fields.Selection([('pending', 'Pending'), ('passed', 'Passed'), ('failed', 'Failed')], string='Quality Gate Status', default='pending')
    phase_start_datetime = fields.Datetime("Phase Start")
    skill_execution_status = fields.Selection([('idle', 'Idle'), ('running', 'Running'), ('error', 'Error')], string='Skill Status', default='idle')
    production_drive_type = fields.Selection([('standard', 'Standard'), ('parameter', 'Parameter-driven')], string='Drive Type', default='standard')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    rework_mo_id = fields.Many2one('mrp.production', string='Rework MO')
    rejection_reason_id = fields.Many2one('farm.quality.rejection.reason', string='Rejection Reason')
    quality_check_ids = fields.One2many('agri.quality.check', 'production_id', string='Quality Checks')

    def _compute_is_agri_processing_enabled(self):
        for rec in self:
            rec.is_agri_processing_enabled = True

    # --- Processing Specific Gate Logic ---
    def _get_isl_model(self):
        res = super(MrpProduction, self)._get_isl_model()
        if getattr(self, 'industry_type', getattr(self.bom_id, 'industry_type', '')) == 'food_processing':
            return 'agri.isl.processing.production'
        return res

    def action_confirm(self):
        """ Processing-specific pre-confirmation checks. """
        for order in self:
            if getattr(order, 'industry_type', getattr(order.bom_id, 'industry_type', '')) == 'food_processing':
                # [Level 2: DNA Gate] Enforce Quality Gate
                if hasattr(order, 'validate_quality_gate'):
                    order.validate_quality_gate()
                # US-037-09: HACCP / Quality Gate Pre-check
                pass
        return super(MrpProduction, self).action_confirm()

    def button_mark_done(self):
        """ Processing-specific pre-done checks. [Level 2: HACCP Gate] """
        for order in self:
            # US-114-02: Check if all related HACCP/CCP points are passed
            haccp_violations = self.env['farm.haccp.check'].search([
                ('quality_check_id.production_id', '=', order.id),
                ('is_violated', '=', True)
            ])
            if haccp_violations:
                raise UserError(_("HACCP BLOCK: Production cannot be completed. "
                                "Critical Limit violations detected in CCP checks: %s") % 
                                ", ".join(haccp_violations.mapped('point_id.name')))
            
            if getattr(order, 'industry_type', getattr(order.bom_id, 'industry_type', '')) == 'food_processing':
                # Energy checks etc.
                pass
        return super(MrpProduction, self).button_mark_done()
        
    def _compute_efficiencies(self):
        for rec in self:
            pass
            
    def button_recalculate_quantities(self):
        return True
        
    def action_adjust_by_potency(self):
        return True

    def button_substitute_components(self):
        return True
        
    def action_open_label_wizard(self):
        return True
        
    def action_start(self):
        return True
    
    def action_release_hold(self):
        return True
    
    def action_view_isl_record(self):
        return True
