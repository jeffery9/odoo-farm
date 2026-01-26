# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class FarmProcessingBom(models.Model):
    """
    Food Processing BOM that extends ISL architecture with farm-specific features
    """
    _name = 'farm.processing.bom'
    _description = 'Farm Food Processing BOM (ISL Layer)'
    _inherit = ['farm.mrp.bom', 'farm.agri.bom.mixin']

    # Processing Specifics
    is_parameter_required = fields.Boolean('Require Process Parameters', default=False)
    target_temp = fields.Float('Standard Temperature (℃)')
    target_ph = fields.Float("Target pH")
    target_brix = fields.Float("Target Brix")
    target_proofing_time = fields.Float("Target Proofing Time (Min)")
    standard_duration = fields.Float('Standard Duration (Minutes)')
    haccp_instructions = fields.Html("HACCP Critical Instructions")

    def write(self, vals):
        # Ensure industry type is set to food processing
        if 'industry_type' not in vals and not self.industry_type:
            vals['industry_type'] = 'food_processing'
        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        # Ensure industry type is set to food processing
        for vals in vals_list:
            if 'industry_type' not in vals or not vals.get('industry_type'):
                vals['industry_type'] = 'food_processing'
        return super().create(vals_list)


class FarmProcessingProduction(models.Model):
    """
    Food Processing Production Order that extends ISL architecture with farm-specific features
    """
    _name = 'farm.processing.production'
    _description = 'Farm Food Processing Order (ISL Layer)'
    _inherit = ['farm.mrp.production', 'farm.agri.production.mixin']

    # Energy Tracking (Processing Specific)
    energy_reading_start = fields.Float(string='Energy Reading Start', copy=False)
    energy_reading_end = fields.Float(string='Energy Reading End', copy=False)
    energy_cost_total = fields.Float(string='Total Energy Cost', compute='_compute_energy_cost_isl')

    # --- Polymorphic Link (US-TECH-06-26) ---
    processing_bom_id = fields.Many2one('farm.processing.bom', string='Processing Recipe', compute='_compute_processing_bom_id')

    def _compute_processing_bom_id(self):
        for rec in self:
            # Link to the farm-specific processing BOM
            if rec.bom_id:
                # Find the corresponding farm.processing.bom for this farm.mrp.bom
                farm_bom = self.env['farm.processing.bom'].search([('bom_id', '=', rec.bom_id.id)], limit=1)
                rec.processing_bom_id = farm_bom
            else:
                rec.processing_bom_id = False

    @api.depends('energy_reading_start', 'energy_reading_end')
    def _compute_energy_cost_isl(self):
        for rec in self:
            rec.energy_cost_total = (rec.energy_reading_end - rec.energy_reading_start) * 1.0  # Placeholder logic

    def isl_post_done(self):
        """ US-14-13: Material Conservation / Mass Balance Algorithm. """
        self.ensure_one()
        order = self.mrp_production_id  # Base production order via _inherits in ISL
        bom = self.env['farm.processing.bom'].search([('bom_id', '=', self.bom_id.id)], limit=1)

        if not bom:
            return

        total_consumed_qty = sum(move.quantity_done * move.product_uom.factor_inv for move in order.move_raw_ids)
        total_produced_qty = sum(move_line.quantity_done * move_line.product_uom.factor_inv
                               for move_line in order.finished_move_line_ids
                               if move_line.product_id == order.product_id or move_line.product_id in order.bom_id.byproduct_ids.mapped('product_id'))

        if total_consumed_qty > 0:
            actual_loss_percentage = ((total_consumed_qty - total_produced_qty) / total_consumed_qty) * 100
            if hasattr(bom, 'max_loss_rate') and actual_loss_percentage > bom.max_loss_rate:
                # In Odoo, by the time post_done is called, the transaction is already being committed.
                # However, we can log a warning or trigger an approval if we were in a pre-done hook.
                # For now, we log it and potentially mark the quality gate as rejected.
                self.quality_gate_status = 'rejected'
                order.message_post(body=_("MASS BALANCE ALERT: Actual loss of %.2f%% exceeds limit of %.2f%%.") % (actual_loss_percentage, bom.max_loss_rate))
            else:
                self.quality_gate_status = 'approved'

    def write(self, vals):
        # Ensure industry type is set to food processing
        if 'industry_type' not in vals and not self.industry_type:
            vals['industry_type'] = 'food_processing'
        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        # Ensure industry type is set to food processing
        for vals in vals_list:
            if 'industry_type' not in vals or not vals.get('industry_type'):
                vals['industry_type'] = 'food_processing'
        return super().create(vals_list)