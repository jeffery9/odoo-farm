# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class FarmNetVegRecipe(models.Model):
    """
    [ISL Layer] Net Vegetable Preparation Standard.
    Proxies mrp.bom to handle expected yield and washing specs.
    """
    _name = 'farm.net_vegetable.recipe'
    _description = 'Net Veg Prep Standard'
    _inherits = {'mrp.bom': 'bom_id'}
    
    bom_id = fields.Many2one('mrp.bom', string='Base BOM', required=True, ondelete='cascade')

    # Prep Specifics [US-113-01]
    expected_net_yield_percent = fields.Float("Expected Yield (%)", default=85.0)
    required_chlorine_ppm = fields.Float("Target Chlorine (ppm)", default=100.0)
    cutting_spec = fields.Char("Cutting Specification (e.g. 5mm Shredded)")

class FarmNetVegProduction(models.Model):
    """
    [ISL Layer] Net Vegetable Preparation Order.
    Proxies mrp.production to track real-time processing loss.
    """
    _name = 'farm.net_vegetable.production'
    _description = 'Net Veg Prep Order'
    _inherits = {'mrp.production': 'production_id'}
    _inherit = ['agri.quality.gate.mixin']

    production_id = fields.Many2one('mrp.production', string='Base Order', required=True, ondelete='cascade')

    # Yield Analysis [US-113-01]
    raw_input_weight = fields.Float("Raw Input (kg)", compute="_compute_yield", store=True, precompute=True)
    actual_net_yield = fields.Float("Actual Yield (%)", compute='_compute_yield', store=True, precompute=True)
    
    # Safety Records [US-113-03]
    actual_chlorine_ppm = fields.Float("Actual Chlorine (ppm)")

    @api.depends('production_id.move_raw_ids.product_uom_qty', 'production_id.product_qty')
    def _compute_yield(self):
        for rec in self:
            raw_weight = sum(rec.production_id.move_raw_ids.mapped('product_uom_qty'))
            rec.raw_input_weight = raw_weight
            if raw_weight > 0:
                rec.actual_net_yield = (rec.production_id.product_qty / raw_weight) * 100.0
            else:
                rec.actual_net_yield = 0.0

    def action_confirm(self):
        """ DNA Gate: Validate sanitation parameters. """
        self.validate_quality_gate()
        return super(FarmNetVegProduction, self).action_confirm()

class FarmLotNetVeg(models.Model):
    """
    [ISL Layer] Retail-ready Net Veg Batch.
    Holds packaging hierarchy and shelf-life data.
    """
    _name = 'farm.lot.net_vegetable'
    _description = 'Net Veg Lot'
    _inherits = {'stock.lot': 'lot_id'}
    _inherit = ['agri.traceability.mixin']

    lot_id = fields.Many2one('stock.lot', string='Base Lot', required=True, ondelete='cascade')

    # Packaging Hierarchy [US-113-02]
    parent_crate_id = fields.Many2one('stock.lot', string="Crate/Outer Pack")
    packaging_type = fields.Selection([
        ('bag', 'Retail Bag'), ('crate', 'Crate'), ('pallet', 'Pallet')
    ], string="Pack Level")
    
    expiry_datetime = fields.Datetime("Freshness Deadline", compute='_compute_expiry', store=True, precompute=True)

    @api.depends('create_date')
    def _compute_expiry(self):
        for rec in self:
            # Short cycle: Default 5 days
            if rec.create_date:
                rec.expiry_datetime = fields.Datetime.add(rec.create_date, days=5)
