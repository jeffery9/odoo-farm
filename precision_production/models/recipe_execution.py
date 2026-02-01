# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PrecisionRecipePhase(models.Model):
    _name = 'precision.recipe.phase'
    _description = 'Control Recipe Phase (Instance)'
    _order = 'sequence'

    production_id = fields.Many2one('mrp.production', ondelete='cascade', string="Production Order")
    master_phase_id = fields.Many2one('precision.master.recipe.phase', string="Master Process Phase")
    name = fields.Char("Phase Name", required=True)
    sequence = fields.Integer("Sequence", default=10)
    
    recipe_parameter_ids = fields.One2many('precision.recipe.parameter', 'phase_id')
    recipe_material_ids = fields.One2many('precision.recipe.material', 'phase_id')
    
    duration_planned = fields.Float("Adaptive Duration")
    duration_actual = fields.Float("Actual Duration")
    start_datetime = fields.Datetime("Actual Start")
    end_datetime = fields.Datetime("Actual End")

    state = fields.Selection([
        ('pending', 'Pending'), ('progress', 'In Progress'), ('done', 'Done')
    ], default='pending', tracking=True)
    
    inventory_state = fields.Selection([
        ('draft', 'Pending'), ('done', 'Transactions Completed')
    ], default='draft')
    
    required_workcenter_id = fields.Many2one('mrp.workcenter', readonly=True, string="Required Equipment")
    required_role = fields.Selection([
        ('operator', 'Operator'), ('technician', 'Technician'), ('specialist', 'Specialist')
    ], readonly=True)

    # ---------------------------------------------------------
    # PROCESS CONTROL & PERFORMANCE
    # ---------------------------------------------------------
    def action_start_phase(self):
        for rec in self:
            if rec.state != 'pending': continue

            # [PROCESS CONTROL] Safety Gating
            if rec.production_id.is_process_locked:
                raise UserError(_("EXECUTION BLOCKED: The batch is on HOLD due to: %s") % rec.production_id.lock_reason)

            rec.production_id._check_phase_readiness(rec)

            if rec.production_id.state == 'confirmed':
                rec.production_id.write({'state': 'progress', 'date_start': fields.Datetime.now()})

            rec.write({'state': 'progress', 'start_datetime': fields.Datetime.now()})
            rec.production_id.action_log_intervention(_("PHASE STARTED: %s") % rec.name, intervention_type='manual')

        # Notify KPI updates for all productions involved
        production_ids = [phase.production_id.id for phase in self if phase.production_id]
        if production_ids:
            self.env['mrp.production'].browse(production_ids).notify_kpi_update(production_ids)
        return True

    def action_end_phase(self):
        for rec in self:
            if rec.state != 'progress': continue
            delta = fields.Datetime.now() - rec.start_datetime
            actual_hours = delta.total_seconds() / 3600.0

            # [PERFORMANCE] Efficiency Indexing
            if rec.duration_planned > 0:
                rec.production_id.efficiency_index = (rec.production_id.efficiency_index + (rec.duration_planned / actual_hours)) / 2

            rec.action_produce_inventory_transactions()
            rec.write({
                'state': 'done',
                'end_datetime': fields.Datetime.now(),
                'duration_actual': actual_hours
            })
            rec.production_id.action_log_intervention(_("PHASE FINISHED: %s") % rec.name, intervention_type='manual')

        # Notify KPI updates for all productions involved
        production_ids = [phase.production_id.id for phase in self if phase.production_id]
        if production_ids:
            self.env['mrp.production'].browse(production_ids).notify_kpi_update(production_ids)
        return True

    # [LOSSLESS] Original functionality
    def action_produce_inventory_transactions(self):
        self.ensure_one()
        for material in self.recipe_material_ids.filtered(lambda m: m.state == 'planned'):
            material.action_execute_stock_move()
        self.inventory_state = 'done'
        return True

    def action_open_batch_metrology(self):
        if not self: return False
        if len(self.mapped('master_phase_id')) > 1:
            raise UserError(_("Batch data entry requires all productions to be in the same Process Phase."))
        return {
            'name': _('Batch Metrology Entry'), 'type': 'ir.actions.act_window',
            'res_model': 'precision.metrology.wizard', 'view_mode': 'form', 'target': 'new',
            'context': {'default_phase_ids': [(6, 0, self.ids)], 'default_phase_id': self.ids[0]}
        }
    def action_batch_start(self): self.action_start_phase(); return True
    def action_batch_end(self): self.action_end_phase(); return True

# ... (Parameters & Materials remain LOSSLESS)
class PrecisionRecipeParameter(models.Model):
    _name = 'precision.recipe.parameter'
    _description = 'Control Recipe Parameter (Instance)'
    phase_id = fields.Many2one('precision.recipe.phase', ondelete='cascade')
    production_id = fields.Many2one('mrp.production', related='phase_id.production_id', store=True)
    name = fields.Char("Parameter", required=True)
    target_value = fields.Float("Active Target", required=True)
    tolerance_percent = fields.Float("Tolerance (%)")
    uom_id = fields.Many2one('uom.uom', string="Unit")
    min_value = fields.Float("Limit Min", compute='_compute_range', store=True)
    max_value = fields.Float("Limit Max", compute='_compute_range', store=True)

    @api.depends('target_value', 'tolerance_percent')
    def _compute_range(self):
        for rec in self:
            rec.min_value = rec.target_value * (1 - (rec.tolerance_percent or 0) / 100.0)
            rec.max_value = rec.target_value * (1 + (rec.tolerance_percent or 0) / 100.0)

class PrecisionRecipeMaterial(models.Model):
    _name = 'precision.recipe.material'
    _description = 'Control Recipe Material (Instance)'
    phase_id = fields.Many2one('precision.recipe.phase', ondelete='cascade')
    production_id = fields.Many2one('mrp.production', related='phase_id.production_id', store=True)
    product_id = fields.Many2one('product.product', string="Material", readonly=True)
    quantity_planned = fields.Float("Planned Quantity")
    quantity_actual = fields.Float("Actual Consumed")
    uom_id = fields.Many2one('uom.uom', string="Unit", readonly=True)
    move_id = fields.Many2one('stock.move', string="Inventory Move", readonly=True)
    state = fields.Selection([('planned', 'Planned'), ('added', 'Consumed')], default='planned')

    def action_execute_stock_move(self):
        self.ensure_one()
        if self.state == 'added' or not self.move_id: return True
        self.move_id._action_confirm()
        self.move_id._action_assign()
        self.write({'quantity_actual': self.quantity_planned, 'state': 'added'})
        return True
