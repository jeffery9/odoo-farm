# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
import json

_logger = logging.getLogger(__name__)

class FarmAquaticRecipe(models.Model):
    """
    [ISL Layer] Aquatic Processing Standard.
    Proxies mrp.bom to handle target yield and glazing specs.
    """
    _name = 'farm.aquatic_processing.recipe'
    _description = 'Aquatic Prep Standard'
    _inherits = {'mrp.bom': 'bom_id'}
    
    bom_id = fields.Many2one('mrp.bom', string='Base BOM', required=True, ondelete='cascade')

    # Processing Setpoints [US-118-02]
    target_net_yield_percent = fields.Float("Expected Net Yield (%)", default=65.0)
    target_glazing_percent = fields.Float("Target Glazing (%)", default=10.0)
    required_core_temp = fields.Float("Required Core Temp (℃)", default=-18.0)

class FarmLotAquaticProduct(models.Model):
    """
    [ISL Layer] Processed Aquatic Batch.
    Inherits DNA from specific pond/cage catch.
    """
    _name = 'farm.lot.aquatic_product'
    _description = 'Processed Aquatic Batch'
    _inherits = {'stock.lot': 'lot_id'}
    _inherit = ['agri.traceability.mixin']

    lot_id = fields.Many2one('stock.lot', string='Base Lot', required=True, ondelete='cascade')

    # [US-118-01] Origin
    source_catch_lot_id = fields.Many2one('stock.lot', string="Source Catch Lot", domain=[('industry_type', '=', 'aquaculture')])
    
    # [US-118-02] Glazing Data
    net_weight_kg = fields.Float("Net Weight (kg)")
    ice_glaze_weight_kg = fields.Float("Ice Glaze Weight (kg)")
    actual_glazing_percent = fields.Float("Actual Glazing (%)", compute='_compute_glazing', store=True)

    @api.depends('net_weight_kg', 'ice_glaze_weight_kg')
    def _compute_glazing(self):
        for rec in self:
            total = rec.net_weight_kg + rec.ice_glaze_weight_kg
            rec.actual_glazing_percent = (rec.ice_glaze_weight_kg / total * 100.0) if total > 0 else 0.0

class FarmAquaticProduction(models.Model):
    """
    [ISL Layer] Filleting/Freezing Order.
    Proxies mrp.production to monitor cold-chain redlines.
    """
    _name = 'farm.aquatic_processing.production'
    _description = 'Aquatic Processing Order'
    _inherits = {'mrp.production': 'production_id'}
    _inherit = ['farm.agri.production.mixin', 'agri.quality.gate.mixin', 'agri.incident.alert.mixin']

    production_id = fields.Many2one('mrp.production', string='Base Order', required=True, ondelete='cascade')

    # [US-118-03] Flash Freezing Data
    actual_core_temp = fields.Float("Measured Core Temp (℃)")
    freezer_exit_time = fields.Datetime("Exit Time")

    def action_confirm(self):
        """ DNA Gate: Validate raw fish quality and source pond DO history. """
        self.validate_quality_gate()
        return super(FarmAquaticProduction, self).action_confirm()

    def button_mark_done(self):
        """ Enforce core temp check before completion. """
        for rec in self:
            recipe = self.env['farm.aquatic_processing.recipe'].search([('bom_id', '=', rec.bom_id.id)], limit=1)
            threshold = recipe.required_core_temp if recipe else -18.0
            if rec.actual_core_temp > threshold:
                raise UserError(_("SAFETY BLOCK: Core temperature (%s C) is not low enough (Target: %s C)!") % 
                               (rec.actual_core_temp, threshold))
        return super(FarmAquaticProduction, self).button_mark_done()
