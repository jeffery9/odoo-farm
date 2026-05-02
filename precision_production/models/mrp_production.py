# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class MrpProduction(models.Model):
    _inherit = ['mrp.production', 'precision.production.mixin']

    production_drive_type = fields.Selection(related='bom_id.production_drive_type', store=True)
    assigned_workcenter_id = fields.Many2one('mrp.workcenter', string="Assigned Facility", 
                                            domain="[('id', '=', bom_id.required_workcenter_id)]")
    
    recipe_phase_ids = fields.One2many('precision.recipe.phase', 'production_id', string="Control Recipe")
    
    # [US-81-01] VRA Integration
    vra_prescription_id = fields.Many2one('agri.intervention.vra.prescription', string="VRA Prescription Map",
                                         help="Link to the scientific VRA map for this production.")

    # ---------------------------------------------------------
    # ARCHITECTURAL INTEGRITY: Parallel Support
    # ---------------------------------------------------------
    active_recipe_phase_ids = fields.Many2many('precision.recipe.phase', string="Active Phases", 
                                              compute='_compute_active_phases')
    
    @api.depends('recipe_phase_ids.state')
    def _compute_active_phases(self):
        for rec in self:
            rec.active_recipe_phase_ids = rec.recipe_phase_ids.filtered(lambda p: p.state == 'progress')

    # Legacy Compatibility (Used in Header UI)
    active_recipe_phase_id = fields.Many2one('precision.recipe.phase', string="First Active Phase",
                                            compute='_compute_primary_active', store=True)

    @api.depends('recipe_phase_ids.state')
    def _compute_primary_active(self):
        for rec in self:
            # Returns the first in-progress phase for UI display
            rec.active_recipe_phase_id = rec.recipe_phase_ids.filtered(lambda p: p.state == 'progress')[:1]

    phase_start_datetime = fields.Datetime("Global Recipe Start")

    # Modern UX Fields
    progress_percentage = fields.Float(
        "Progress %",
        compute='_compute_progress_percentage',
        store=True,
        help="Overall progress percentage of the recipe execution"
    )

    @api.depends('recipe_phase_ids.state')
    def _compute_progress_percentage(self):
        for rec in self:
            if not rec.recipe_phase_ids:
                rec.progress_percentage = 0.0
            else:
                total_phases = len(rec.recipe_phase_ids)
                completed_phases = len(rec.recipe_phase_ids.filtered(lambda p: p.state == 'done'))
                rec.progress_percentage = (completed_phases / total_phases) * 100.0 if total_phases > 0 else 0.0

    @api.model
    def get_realtime_kpis(self, production_ids):
        """
        Returns real-time KPIs for active production orders for dashboard updates.
        """
        productions = self.browse(production_ids)
        result = []

        for prod in productions:
            result.append({
                'id': prod.id,
                'yield_confidence': prod.yield_confidence,
                'efficiency_index': prod.efficiency_index,
                'process_status': prod.process_status,
                'active_recipe_phase_id': prod.active_recipe_phase_id.display_name if prod.active_recipe_phase_id else False,
                'progress_percentage': prod.progress_percentage,
            })

        return result

    def notify_kpi_update(self, production_ids=None):
        """
        Send real-time KPI updates via Odoo bus to all subscribed clients.
        """
        if not production_ids:
            # If no IDs specified, notify about all active productions
            productions = self.search([('state', '=', 'progress')])
        else:
            productions = self.browse(production_ids)

        # Get updated KPIs
        kpis = self.get_realtime_kpis(productions.ids)

        # Send notification via bus
        channel_name = 'precision_production/kpi_updates'
        self.env['bus.bus'].sendone(channel_name, {
            'type': 'kpi_update',
            'data': kpis
        })

    # [ISA-88 Batch Size Scaling Logic - LOSSLESS]
    def action_confirm(self):
        """ [LOSSLESS] Confirms MO and instantiates Recipe + Preparation Moves. """
        res = super(MrpProduction, self).action_confirm()
        for rec in self:
            if rec.production_drive_type == 'parameter' and rec.bom_id:
                rec._instantiate_recipe_entity()
        return res

    def _instantiate_recipe_entity(self):
        """ 
        [ISA-88 Batch Scaling]
        Instantiates Control Recipe using Batch Size logic.
        Scales materials and scalable parameters based on actual MO quantity.
        """
        self.ensure_one()
        if self.recipe_phase_ids: return False
        
        # 1. Calculate the Scaling Factor
        batch_base = self.bom_id.recipe_batch_size or 1.0
        scaling_factor = self.product_qty / batch_base

        for m_phase in self.bom_id.master_recipe_phase_ids:
            r_phase = self.env['precision.recipe.phase'].create({
                'production_id': self.id, 'master_phase_id': m_phase.id,
                'name': m_phase.name, 'sequence': m_phase.sequence,
                'duration_planned': m_phase.duration_expected,
                'required_workcenter_id': m_phase.required_workcenter_id.id,
                'required_role': m_phase.required_role,
            })
            
            # 2. Scale Parameters
            for m_param in m_phase.master_parameter_ids:
                target = m_param.target_value
                if m_param.is_scalable:
                    target = target * scaling_factor
                    
                self.env['precision.recipe.parameter'].create({
                    'phase_id': r_phase.id, 'name': m_param.name,
                    'target_value': target, 'tolerance_percent': m_param.tolerance_percent,
                    'uom_id': m_param.uom_id.id,
                })
            
            # 3. Scale Materials
            for m_mat in m_phase.master_material_ids:
                scaled_qty = m_mat.quantity * scaling_factor
                
                # [PREPARATION] Create Raw Material Stock Moves at MO Confirmation
                move = self.env['stock.move'].create({
                    'name': _("Recipe Phase: %s") % m_phase.name, 'product_id': m_mat.product_id.id,
                    'product_uom_qty': scaled_qty, 'product_uom': m_mat.uom_id.id,
                    'location_id': self.location_src_id.id,
                    'location_dest_id': m_mat.product_id.with_company(self.company_id).property_stock_production.id,
                    'raw_material_production_id': self.id, 'company_id': self.company_id.id,
                    'origin': f"{self.name} Phase: {m_phase.name}",
                })
                self.env['precision.recipe.material'].create({
                    'phase_id': r_phase.id, 'product_id': m_mat.product_id.id,
                    'quantity_planned': scaled_qty, 'uom_id': m_mat.uom_id.id, 'move_id': move.id,
                })
        return True

    def action_start_recipe(self):
        """ Global start: Marks MO in progress and triggers first phase. """
        self.ensure_one()
        if not self.recipe_phase_ids: self._instantiate_recipe_entity()
        self.write({'phase_start_datetime': fields.Datetime.now(), 'state': 'progress'})
        if self.recipe_phase_ids:
            self.recipe_phase_ids[0].action_start_phase()
        # Notify KPI updates
        self.notify_kpi_update([self.id])
        return True

    def action_next_phase(self):
        """
        [ADAPTIVE UX] Sequential helper.
        Finishes current active and starts next, but doesn't block parallel ones.
        """
        self.ensure_one()
        current = self.active_recipe_phase_id
        if current:
            current.action_end_phase()

        phases = self.recipe_phase_ids
        idx = list(phases.ids).index(current.id) if current else -1
        if idx < len(phases) - 1:
            next_p = phases[idx + 1]
            next_p.action_start_phase()

        # Notify KPI updates
        self.notify_kpi_update([self.id])
        return True

    def _check_phase_readiness(self, phase):
        if phase.required_role == 'specialist' and not self.env.user.has_group('mrp.group_mrp_manager'):
            raise UserError(_("PERSONNEL BLOCK: Stage '%s' requires Specialist.") % phase.name)
        if phase.required_workcenter_id and self.assigned_workcenter_id != phase.required_workcenter_id:
             raise UserError(_("EQUIPMENT BLOCK: Stage '%s' requires %s.") % (phase.name, phase.required_workcenter_id.name))
        return True

    # ---------------------------------------------------------
    # PROCESS CONTROL INTEGRATION: Active Stability Monitoring
    # ---------------------------------------------------------
    def process_precision_metrology(self, parameter_name, actual_value, phase_id=False):
        """
        [SPC Process Control]
        Analyzes stability and triggers Execution Hold on critical deviations.
        """
        self.ensure_one()
        phase = self.env['precision.recipe.phase'].browse(phase_id) or self.active_recipe_phase_id
        param_inst = phase.recipe_parameter_ids.filtered(lambda p: p.name.lower() == parameter_name.lower())[:1]

        if param_inst:
            deviation_pct = abs(actual_value - param_inst.target_value) / (param_inst.target_value or 1.0) * 100

            # 1. Automatic Process Control Locking (Critical Gating)
            if deviation_pct > 25.0: # Critical threshold
                self.process_status = 'out_of_control'
                self.action_hold_execution(_("CRITICAL DEVIATION: %s%% in %s") % (round(deviation_pct, 1), parameter_name))
            elif deviation_pct > 10.0:
                self.process_status = 'drifting'
            else:
                self.process_status = 'stable'

            # 2. [LOSSLESS] Adaptation Logic
            if actual_value < param_inst.min_value or actual_value > param_inst.max_value:
                basis = self.env['precision.intervention.basis'].create({
                    'name': _("Adaptation Triggered: %s") % parameter_name,
                    'parameter_name': parameter_name,
                    'recipe_standard_value': param_inst.target_value,
                    'actual_measured_value': actual_value,
                    'res_model': self._name, 'res_id': self.id
                })
                # Setpoint Adaptation
                new_target = param_inst.target_value - ((actual_value - param_inst.target_value) * 0.5)
                param_inst.write({'target_value': new_target})
                self.action_log_intervention(_("ADAPTIVE SETPOINT: %s to %s") % (parameter_name, new_target), intervention_type='active', basis_id=basis.id)

                # Timing & Material Adaptation (LOSSLESS Retention)
                if 'reaction' in parameter_name.lower() and (actual_value < param_inst.target_value):
                    extension = abs(actual_value - param_inst.target_value) * 0.1
                    phase.write({'duration_planned': phase.duration_planned + extension})
                    self.action_log_intervention(_("ADAPTIVE TIMING: +%s hrs") % extension, intervention_type='active', basis_id=basis.id)
                if 'concentration' in parameter_name.lower() and (actual_value < param_inst.target_value):
                    reagent = phase.recipe_material_ids[:1]
                    if reagent:
                        reagent.write({'quantity_planned': reagent.quantity_planned * 1.1})
                        self.action_log_intervention(_("ADAPTIVE MATERIAL: Scaling %s") % reagent.product_id.name, intervention_type='active', basis_id=basis.id)

        self.last_telemetry_data = _("Param: %s | Val: %s | Status: %s") % (parameter_name, actual_value, self.process_status)

        # Notify KPI updates
        self.notify_kpi_update([self.id])
        return True

    def action_calibrate_yield(self, new_qty=0.0):
        self.ensure_one()
        diff = self.product_qty - new_qty
        if diff > 0:
            self.env['stock.scrap'].create({
                'production_id': self.id, 'product_id': self.product_id.id,
                'scrap_qty': diff, 'product_uom_id': self.product_uom_id.id, 'location_id': self.location_src_id.id,
            })
        self.product_qty = new_qty
        self.last_calibration_date = fields.Datetime.now()
        rec_qty = self.bom_id.product_qty or 1.0
        self.yield_confidence = max(0, 100 - (abs(new_qty - rec_qty) / rec_qty * 100))

        # Notify KPI updates
        self.notify_kpi_update([self.id])
        return True

    def button_mark_done(self):
        """ [LOSSLESS] Completes MO and triggers Multi-grade grading logic. """
        for rec in self:
            if rec.production_drive_type == 'parameter' and rec.graded_output_ids:
                rec.action_generate_graded_lots()
        return super(MrpProduction, self).button_mark_done()

    def action_open_metrology_wizard(self):
        self.ensure_one()
        return {
            'name': _('Input Measurement'), 'type': 'ir.actions.act_window',
            'res_model': 'precision.metrology.wizard', 'view_mode': 'form', 'target': 'new',
            'context': {'default_production_id': self.id, 'default_phase_id': self.active_recipe_phase_id.id}
        }

    # [US-81-01] Dynamic VRA-L3 Linkage Logic
    def action_calculate_spatial_setpoint(self, lat, lng):
        """
        [DYNAMIC VRA LINK]
        1. Find matching grid cell in the VRA Prescription.
        2. Retrieve target rate.
        3. Update 'is_vra_dynamic' parameters.
        4. Trigger Hardware Setpoint Command.
        """
        self.ensure_one()
        if not self.vra_prescription_id or not self.active_recipe_phase_id:
            return False

        # Find nearest grid cell in the prescription
        best_line = False
        min_dist = float('inf')
        
        # Use simple Euclidean distance for grid matching
        for line in self.vra_prescription_id.line_ids:
            cell = line.grid_cell_id
            dist = (cell.center_lat - lat)**2 + (cell.center_lng - lng)**2
            if dist < min_dist:
                min_dist = dist
                best_line = line
        
        if best_line:
            target_rate = best_line.target_rate
            
            # Update all dynamic parameters in the active phase
            dynamic_params = self.active_recipe_phase_id.recipe_parameter_ids.filtered(lambda p: p.is_vra_dynamic)
            for param in dynamic_params:
                if param.target_value != target_rate:
                    param.write({'target_value': target_rate})
                    
                    # [HARDWARE LOOP] Send command to linked IoT devices
                    for device in self.active_recipe_phase_id.iot_device_ids:
                        device.send_control_command('set_point', value=target_rate, target_phase_id=self.active_recipe_phase_id)
            
            self.action_log_intervention(
                _("VRA SPATIAL AUTO-ADJUST: Setpoint updated to %s based on GPS [%s, %s]") % (target_rate, lat, lng),
                intervention_type='active'
            )
        return True