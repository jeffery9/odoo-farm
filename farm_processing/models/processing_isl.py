# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class FarmProcessingBom(models.Model):
    _name = 'farm.processing.bom'
    _description = 'Food Processing BOM (ISL Layer)'
    _inherits = {'mrp.bom': 'bom_id'}
    _inherit = ['farm.agri.bom.mixin']

    bom_id = fields.Many2one('mrp.bom', string='Base BOM', required=True, ondelete='cascade')
    
    # Processing Specifics
    is_parameter_required = fields.Boolean('Require Process Parameters', default=False)
    target_temp = fields.Float('Standard Temperature (℃)')
    target_ph = fields.Float("Target pH")
    target_brix = fields.Float("Target Brix")
    target_proofing_time = fields.Float("Target Proofing Time (Min)")
    standard_duration = fields.Float('Standard Duration (Minutes)')
    haccp_instructions = fields.Html("HACCP Critical Instructions")

class FarmProcessingProduction(models.Model):
    _name = 'farm.processing.production'
    _description = 'Food Processing Order (ISL Layer)'
    _inherits = {'mrp.production': 'production_id'}
    _inherit = ['farm.agri.production.mixin']

    production_id = fields.Many2one('mrp.production', string='Base Production Order', required=True, ondelete='cascade')

    # Energy Tracking (Moved from Base)
    energy_reading_start = fields.Float(string='Energy Reading Start', copy=False)
    energy_reading_end = fields.Float(string='Energy Reading End', copy=False)
    energy_cost_total = fields.Float(string='Total Energy Cost', compute='_compute_energy_cost_isl')

    # --- Polymorphic Link (US-TECH-06-26) ---
    processing_bom_id = fields.Many2one('farm.processing.bom', string='Processing Recipe', compute='_compute_processing_bom_id')

    def _compute_processing_bom_id(self):
        for rec in self:
            if rec.bom_id:
                rec.processing_bom_id = self.env['farm.processing.bom'].search([('bom_id', '=', rec.bom_id.id)], limit=1)
            else:
                rec.processing_bom_id = False

    @api.depends('energy_reading_start', 'energy_reading_end')
    def _compute_energy_cost_isl(self):
        for rec in self:
            rec.energy_cost_total = (rec.energy_reading_end - rec.energy_reading_start) * 1.0 # Placeholder logic

    def isl_post_done(self):
        """ US-14-13: Material Conservation / Mass Balance Algorithm. """
        self.ensure_one()
        order = self.production_id
        bom = self.processing_bom_id
        
        if not bom:
            return
            
        total_consumed_qty = sum(move.quantity_done * move.product_uom.factor_inv for move in order.move_raw_ids)
        total_produced_qty = sum(move_line.quantity_done * move_line.product_uom.factor_inv 
                               for move_line in order.finished_move_line_ids 
                               if move_line.product_id == order.product_id or move_line.product_id in order.bom_id.byproduct_ids.mapped('product_id'))

        if total_consumed_qty > 0:
            actual_loss_percentage = ((total_consumed_qty - total_produced_qty) / total_consumed_qty) * 100
            if actual_loss_percentage > bom.max_loss_rate:
                # In Odoo, by the time post_done is called, the transaction is already being committed.
                # However, we can log a warning or trigger an approval if we were in a pre-done hook.
                # For now, we log it and potentially mark the quality gate as rejected.
                self.quality_gate_status = 'rejected'
                order.message_post(body=_("MASS BALANCE ALERT: Actual loss of %.2f%% exceeds limit of %.2f%%.") % (actual_loss_percentage, bom.max_loss_rate))
            else:
                self.quality_gate_status = 'approved'

