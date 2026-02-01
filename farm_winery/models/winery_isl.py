# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
import json

_logger = logging.getLogger(__name__)

class FarmWineryVessel(models.Model):
    """
    [ISL Layer] Fermentation Tank or Oak Barrel.
    Proxies mrp.workcenter to manage aging assets.
    """
    _name = 'farm.winery.vessel'
    _description = 'Winery Vessel/Barrel'
    _inherits = {'mrp.workcenter': 'workcenter_id'}
    
    workcenter_id = fields.Many2one('mrp.workcenter', required=True, ondelete='cascade')

    vessel_type = fields.Selection([
        ('stainless', 'Stainless Steel Tank'),
        ('oak_new', 'New Oak Barrel'),
        ('oak_used', 'Used Oak Barrel'),
        ('concrete', 'Concrete Egg')
    ], string="Vessel Type", required=True)
    
    capacity_liters = fields.Float("Volume Capacity (L)")
    current_fill_level = fields.Float("Current Fill (%)")

class FarmWineryRecipe(models.Model):
    """
    [ISL Layer] Enology Protocol (BOM).
    """
    _name = 'farm.winery.recipe'
    _description = 'Winery Protocol'
    _inherits = {'mrp.bom': 'bom_id'}
    
    bom_id = fields.Many2one('mrp.bom', string='Base BOM', required=True, ondelete='cascade')
    
    target_alcohol_pct = fields.Float("Target Alcohol (%)")
    fermentation_temp_target = fields.Float("Target Temp (℃)")

class FarmWineryProduction(models.Model):
    """
    [ISL Layer] Vinification / Blending Job.
    """
    _name = 'farm.winery.production'
    _description = 'Vinification Order'
    _inherits = {'mrp.production': 'production_id'}
    _inherit = [
        'farm.agri.production.mixin',
        'agri.agent.instruction.mixin',
        'agri.incident.alert.mixin'
    ]

    production_id = fields.Many2one('mrp.production', string='Base Order', required=True, ondelete='cascade')

    # [US-116-01] Fermentation Real-time Data
    current_brix = fields.Float("Current Brix")
    current_temp = fields.Float("Current Temp (℃)")
    
    def handle_fermentation_telemetry(self, data):
        """ Respond to temperature spikes in the tank. """
        self.ensure_one()
        temp = data.get('temperature')
        if temp and temp > 30.0: # Fermentation thermal limit
            self.report_incident('critical', 'Fermentation Runaway', _("Tank %s temp too high!") % self.name)
        return True

class FarmLotWine(models.Model):
    """
    [ISL Layer] Wine Batch/Lot.
    Holds aging data and final chemistry profile.
    """
    _name = 'farm.lot.wine'
    _description = 'Wine Batch'
    _inherits = {'stock.lot': 'lot_id'}
    _inherit = ['agri.traceability.mixin', 'agri.biological.valuation.mixin']

    lot_id = fields.Many2one('stock.lot', string='Base Lot', required=True, ondelete='cascade')

    # [US-116-02] Aging Status
    barrel_entry_date = fields.Date("Barrel Entry")
    aging_months = fields.Integer("Months in Wood", compute='_compute_aging')
    
    # [US-116-04] Chemistry Profile
    alcohol_final = fields.Float("Alcohol (%)")
    residual_sugar = fields.Float("RS (g/L)")
    free_so2 = fields.Float("Free SO2 (mg/L)")

    @api.depends('barrel_entry_date')
    def _compute_aging(self):
        for rec in self:
            if rec.barrel_entry_date:
                delta = fields.Date.today() - rec.barrel_entry_date
                rec.aging_months = int(delta.days / 30)
            else:
                rec.aging_months = 0
