# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
import json

_logger = logging.getLogger(__name__)

class FarmFlowerBom(models.Model):
    _name = 'farm.flower.bom'
    _description = 'Floral Recipe (ISL Layer)'
    _inherits = {'mrp.bom': 'bom_id'}
    _inherit = ['agri.bom.mixin']

    bom_id = fields.Many2one('mrp.bom', string='Base BOM', required=True, ondelete='cascade')

    # Recipe Type [US-FLOR-06]
    recipe_type = fields.Selection([
        ('growth', 'Growing Recipe'),
        ('preservation', 'Preservation Treatment (Post-harvest)')
    ], string="Recipe Type", default='growth', required=True)

    # Bloom Control (Growth Type)
    target_light_hours = fields.Float("Target Light Hours")
    target_temp_day = fields.Float("Target Day Temp")
    target_temp_night = fields.Float("Target Night Temp")
    target_temp_diff = fields.Float("Target DIF", compute='_compute_dif', store=True, precompute=True)

    # Preservation Parameters (Treatment Type) [US-FLOR-06]
    target_hydration_hours = fields.Float("Required Hydration (Hours)", help="Pulse treatment duration.")
    preservative_formula_notes = fields.Text("Preservative Formula Notes")
    target_storage_temp = fields.Float("Target Storage Temp (℃)", default=2.0)

    @api.depends('target_temp_day', 'target_temp_night')
    def _compute_dif(self):
        for rec in self:
            rec.target_temp_diff = rec.target_temp_day - rec.target_temp_night

    def write(self, vals):
        if 'industry_type' not in vals and not self.industry_type:
            vals['industry_type'] = 'floriculture'
        return super().write(vals)

class FarmLotFlower(models.Model):
    _name = 'farm.lot.flower'
    _description = 'Floral Batch (ISL Layer)'
    _inherits = {'stock.lot': 'lot_id'}
    _inherit = ['agri.traceability.mixin', 'agri.incident.alert.mixin']

    lot_id = fields.Many2one('stock.lot', string='Base Lot', required=True, ondelete='cascade')

    # Status & Quality
    bloom_stage_at_harvest = fields.Selection([
        ('bud', 'Tight Bud'), ('showing', 'Color Showing'), ('half', 'Half Open'), ('full', 'Full Bloom')
    ], string="Bloom Stage at Harvest")
    
    predicted_vase_life = fields.Integer("Predicted Vase-life (Days)", compute='_compute_vase_life', store=True, precompute=True)
    
    # Preservation Status [US-FLOR-06]
    is_preserved = fields.Boolean("Preservation Completed", default=False)
    hydration_end_time = fields.Datetime("Hydration Completed At")
    preservative_used = fields.Char("Preservative Agent")

    # Cold-chain Monitoring
    max_transport_temp = fields.Float("Cold-chain Redline", default=5.0)
    current_batch_temp = fields.Float("Latest Recorded Temp (℃)")
    temperature_violation = fields.Boolean("Violation Detected", default=False)

    @api.depends('bloom_stage_at_harvest', 'current_batch_temp', 'is_preserved')
    def _compute_vase_life(self):
        for rec in self:
            base_life = 14
            # Bonus for proper preservation
            preservation_bonus = 3 if rec.is_preserved else 0
            stage_reduction = {'bud': 0, 'showing': 2, 'half': 5, 'full': 8}
            temp_penalty = max(0, (rec.current_batch_temp - 5.0) * 0.5) if rec.current_batch_temp else 0
            rec.predicted_vase_life = max(1, int(base_life + preservation_bonus - stage_reduction.get(rec.bloom_stage_at_harvest, 0) - temp_penalty))

    def action_complete_preservation(self, agent_name):
        """ [US-FLOR-06] Mark preservation as done and update quality DNA. """
        self.ensure_one()
        self.write({
            'is_preserved': True,
            'preservative_used': agent_name,
            'hydration_end_time': fields.Datetime.now()
        })
        self.generate_quality_fingerprint()

class FarmFlowerOrder(models.Model):
    _name = 'farm.flower.order'
    _description = 'Floral Growing/Treatment Order (ISL Layer)'
    _inherits = {'mrp.production': 'production_id'}
    _inherit = [
        'agri.intervention.mixin', 
        'agri.growth.cycle.mixin', 
        'agri.quality.gate.mixin', 
        'agri.weather.sensitive.mixin', 
        'agri.agent.instruction.mixin'
    ]

    production_id = fields.Many2one('mrp.production', string='Base Order', required=True, ondelete='cascade')
    source_nursery_batch_id = fields.Many2one('farm.nursery.batch', string="Source Seedlings")
    
    # Technical fields for treatment [US-FLOR-06]
    actual_hydration_hours = fields.Float("Actual Hydration Duration")

    def action_confirm(self):
        """ [DNA Gate] Specialized validation based on Order Type. """
        for order in self:
            flower_bom = self.env['farm.flower.bom'].search([('bom_id', '=', order.bom_id.id)], limit=1)
            if flower_bom and flower_bom.recipe_type == 'preservation':
                # Preservation Gate: Check if equipment/solution is ready
                order.validate_quality_gate()
            else:
                # Growth Gate: Check weather and ESG
                order.check_operation_esg_gate()
                order.check_weather_window('general')
        return super(FarmFlowerOrder, self).action_confirm()

    def button_mark_done(self):
        """ [US-FLOR-06] Auto-update Lot preservation status on completion. """
        res = super(FarmFlowerOrder, self).button_mark_done()
        for order in self:
            flower_bom = self.env['farm.flower.bom'].search([('bom_id', '=', order.bom_id.id)], limit=1)
            if flower_bom and flower_bom.recipe_type == 'preservation' and order.lot_producing_id:
                # Up-cast to ISL Lot
                isl_lot = self.env['farm.lot.flower'].search([('lot_id', '=', order.lot_producing_id.id)], limit=1)
                if isl_lot:
                    isl_lot.action_complete_preservation(flower_bom.preservative_formula_notes or 'Standard Solution')
        return res
