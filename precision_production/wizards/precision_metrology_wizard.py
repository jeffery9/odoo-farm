# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PrecisionMetrologyWizard(models.TransientModel):
    _name = 'precision.metrology.wizard'
    _description = 'Precision Measurement Input (Production Batch Ready)'

    # Supports single MO or Multiple Phases (for Production batching)
    production_id = fields.Many2one('mrp.production', string="Production Order")
    phase_id = fields.Many2one('precision.recipe.phase', string="Active Phase")
    
    # [NEW] Multi-Phase support for parallel productions
    phase_ids = fields.Many2many('precision.recipe.phase', string="Target Productions/Phases")
    
    parameter_id = fields.Many2one('precision.recipe.parameter', string="Parameter", required=True)
    
    # UI Context
    target_value = fields.Float(related='parameter_id.target_value', readonly=True)
    uom_id = fields.Many2one(related='parameter_id.uom_id', readonly=True)
    actual_value = fields.Float("Measured Value", required=True)

    # Calculated deviation
    deviation_percent = fields.Float("Deviation %", compute="_compute_deviation_percent", store=True, precompute=True)

    @api.onchange('phase_id')
    def _onchange_phase_id(self):
        if self.phase_id:
            return {'domain': {'parameter_id': [('phase_id', '=', self.phase_id.id)]}}

    @api.depends('parameter_id.target_value', 'actual_value')
    def _compute_deviation_percent(self):
        for record in self:
            if record.parameter_id and record.parameter_id.target_value:
                target = record.parameter_id.target_value
                actual = record.actual_value or 0.0
                record.deviation_percent = abs((actual - target) / target) * 100
            else:
                record.deviation_percent = 0.0

    def action_apply_and_calculate(self):
        """ 
        [ADAPTIVE] Processes measurement for a single production OR a batch of parallel productions.
        """
        self.ensure_one()
        
        # Determine the target phases (either the single one or the batch selected)
        target_phases = self.phase_ids or self.phase_id
        
        if not target_phases:
            raise UserError(_("No target productions/phases selected for data entry."))

        for phase in target_phases:
            # Distribute the measurement data to each production's MO
            phase.production_id.process_precision_metrology(
                parameter_name=self.parameter_id.name,
                actual_value=self.actual_value,
                phase_id=phase.id
            )
            
        return {'type': 'ir.actions.act_window_close'}