# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
import json

_logger = logging.getLogger(__name__)

class FarmEssentialOilRecipe(models.Model):
    """
    [ISL Layer] Essential Oil Extraction Protocol.
    Proxies mrp.bom to handle distillation parameters.
    """
    _name = 'farm.essential_oil.recipe'
    _description = 'Essential Oil Protocol'
    _inherits = {'mrp.bom': 'bom_id'}
    _inherit = ['agri.bom.mixin']

    bom_id = fields.Many2one('mrp.bom', string='Base BOM', required=True, ondelete='cascade')

    # Distillation Parameters [US-112-01]
    target_distillation_temp = fields.Float("Target Temp (℃)")
    target_pressure_bar = fields.Float("Target Pressure (bar)")
    standard_yield_percent = fields.Float("Standard Yield (%)", help="Expected Oil/Material ratio")

class FarmEssentialOilProduction(models.Model):
    """
    [ISL Layer] Distillation Order.
    Proxies mrp.production to track extraction yield.
    """
    _name = 'farm.essential_oil.production'
    _description = 'Distillation Order'
    _inherits = {'mrp.production': 'production_id'}
    _inherit = ['agri.quality.gate.mixin']

    production_id = fields.Many2one('mrp.production', string='Base Order', required=True, ondelete='cascade')

    # Yield Tracking [US-112-02]
    total_material_input_kg = fields.Float("Material Input (kg)", compute='_compute_yield_metrics', store=True)
    actual_oil_output_l = fields.Float("Oil Output (L)", related='production_id.product_qty')
    extraction_yield = fields.Float("Extraction Yield (%)", compute='_compute_yield_metrics', store=True)

    @api.depends('production_id.move_raw_ids.product_uom_qty', 'production_id.product_qty')
    def _compute_yield_metrics(self):
        for rec in self:
            input_qty = sum(rec.production_id.move_raw_ids.mapped('product_uom_qty'))
            rec.total_material_input_kg = input_qty
            if input_qty > 0:
                rec.extraction_yield = (rec.production_id.product_qty / input_qty) * 100.0
            else:
                rec.extraction_yield = 0.0

    def action_confirm(self):
        """ DNA Gate: Validate raw material batch readiness. """
        self.validate_quality_gate()
        return super(FarmEssentialOilProduction, self).action_confirm()

class FarmLotEssentialOil(models.Model):
    """
    [ISL Layer] Concentrated Essence Batch.
    Inherits DNA from multiple raw material batches.
    """
    _name = 'farm.lot.essential_oil'
    _description = 'Essential Oil Batch'
    _inherits = {'stock.lot': 'lot_id'}
    _inherit = ['agri.traceability.mixin', 'agri.biological.valuation.mixin']

    lot_id = fields.Many2one('stock.lot', string='Base Lot', required=True, ondelete='cascade')

    # [US-112-04] Quality Profile
    terpene_content_percent = fields.Float("Total Terpenes (%)")
    is_medical_grade = fields.Boolean("Medical Grade", compute='_compute_grade', store=True)

    @api.depends('terpene_content_percent')
    def _compute_grade(self):
        for rec in self:
            rec.is_medical_grade = rec.terpene_content_percent > 45.0 # Example threshold

    def _compute_trace_hash(self):
        """ [US-112-03] Specialized Hash: Aggregates all material source fingerprints. """
        res = super(FarmLotEssentialOil, self)._compute_trace_hash()
        # Custom logic would iterate through production moves to aggregate hashes
        return res
