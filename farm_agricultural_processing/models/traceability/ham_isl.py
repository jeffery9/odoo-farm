# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
import json

_logger = logging.getLogger(__name__)

class FarmHamRecipe(models.Model):
    """
    [ISL Layer] Ham Curing Protocol. [De-industrialized]
    Proxies mrp.bom to handle salting ratio and aging duration.
    """
    _name = 'farm.ham.recipe'
    _description = 'Ham Curing Protocol'
    _inherits = {'mrp.bom': 'bom_id'}
    
    bom_id = fields.Many2one('mrp.bom', string='Base Recipe', required=True, ondelete='cascade')

    # Process Setpoints [US-117-03]
    target_aging_months = fields.Integer("Target Aging (Months)", default=24)
    target_dehydration_pct = fields.Float("Expected Weight Loss (%)", default=30.0)
    salt_ratio_pct = fields.Float("Salt Ratio (%)", default=8.0)

class FarmLotHam(models.Model):
    """
    [ISL Layer] Dry-Cured Ham Asset. [De-industrialized]
    Inherits DNA from specific livestock lot (Pig).
    """
    _name = 'farm.lot.ham'
    _description = 'Ham Batch/Asset'
    _inherits = {'stock.lot': 'lot_id'}
    _inherit = ['agri.traceability.mixin', 'agri.biological.valuation.mixin']

    lot_id = fields.Many2one('stock.lot', string='Base Lot', required=True, ondelete='cascade')

    # [US-117-01] Lineage
    source_pig_lot_id = fields.Many2one('stock.lot', string="Source Pig Lot", domain=[('industry_type', '=', 'livestock')])
    
    # [US-117-02] Physical Status
    fresh_weight = fields.Float("Fresh Weight (kg)")
    current_weight = fields.Float("Current Weight (kg)")
    dehydration_rate = fields.Float("Dehydration Rate (%)", compute='_compute_ham_kpi', store=True, precompute=True)
    
    aging_start_date = fields.Date("Aging Start Date")
    aging_age_months = fields.Integer("Vintage (Months)", compute='_compute_ham_kpi', store=True, precompute=True)

    @api.depends('fresh_weight', 'current_weight', 'aging_start_date')
    def _compute_ham_kpi(self):
        today = fields.Date.today()
        for rec in self:
            # 1. Weight loss calculation
            if rec.fresh_weight > 0:
                rec.dehydration_rate = (rec.fresh_weight - rec.current_weight) / rec.fresh_weight * 100.0
            
            # 2. Aging duration calculation
            if rec.aging_start_date:
                delta = today - rec.aging_start_date
                rec.aging_age_months = int(delta.days / 30)

    @api.depends('aging_age_months', 'dehydration_rate')
    def _compute_fair_value(self):
        """ [Level 3 DNA] Asset value increases with vintage age. """
        res = super(FarmLotHam, self)._compute_fair_value()
        for rec in self:
            # Multiplier: +5% value for each 6 months of aging
            age_multiplier = 1.0 + (rec.aging_age_months / 6.0) * 0.05
            rec.total_asset_value *= age_multiplier
        return res

class FarmHamProduction(models.Model):
    """
    [ISL Layer] Curing/Aging Order. [De-industrialized]
    Proxies mrp.production to manage environment checkpoints.
    """
    _name = 'farm.ham.production'
    _description = 'Ham Curing Order'
    _inherits = {'mrp.production': 'production_id'}
    _inherit = ['agri.quality.gate.mixin', 'agri.incident.alert.mixin']

    production_id = fields.Many2one('mrp.production', string='Base Order', required=True, ondelete='cascade')

    # [US-117-03] Environment Control
    cellar_humidity = fields.Float("Current Humidity (%)")
    cellar_temp = fields.Float("Current Temp (℃)")

    def action_confirm(self):
        """ DNA Gate: Validate salt quality and leg weight. """
        self.validate_quality_gate()
        return super(FarmHamProduction, self).action_confirm()
