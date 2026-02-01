# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class FarmSymbioticPlot(models.Model):
    """
    [ISL Layer] Digital Twin of a Symbiotic Field.
    Proxies farm.location to manage water levels and trench ratio.
    """
    _name = 'farm.symbiotic.plot'
    _description = 'Symbiotic Field'
    _inherits = {'farm.location': 'location_id'}
    _inherit = ['agri.geospatial.mixin']

    location_id = fields.Many2one('farm.location', required=True, ondelete='cascade')

    # Symbiotic Parameters [US-121-01]
    trench_area_ratio = fields.Float("Trench Area Ratio (%)", default=10.0)
    target_water_depth_cm = fields.Float("Target Water Depth (cm)")

class FarmSymbioticRecipe(models.Model):
    """
    [ISL Layer] Co-culture Recipe (BOM).
    """
    _name = 'farm.symbiotic.recipe'
    _description = 'Co-culture Recipe'
    _inherits = {'mrp.bom': 'bom_id'}
    _inherit = ['farm.agri.bom.mixin', 'agri.nutrient.mixin']

    bom_id = fields.Many2one('mrp.bom', string='Base BOM', required=True, ondelete='cascade')

    # Nutrient Recirculation [US-121-02]
    fish_manure_nitrogen_credit = fields.Float("Fertilizer Credit from Fish (kg/mu)")

class FarmSymbioticOrder(models.Model):
    """
    [ISL Layer] Symbiotic Cycle Order.
    Proxies mrp.production to manage both Rice and Fish growth.
    """
    _name = 'farm.symbiotic.order'
    _description = 'Symbiotic Cycle'
    _inherits = {'mrp.production': 'production_id'}
    _inherit = [
        'farm.agri.production.mixin',
        'agri.quality.gate.mixin',
        'agri.weather.sensitive.mixin'
    ]

    production_id = fields.Many2one('mrp.production', string='Base Order', required=True, ondelete='cascade')

    # [US-121-03] Pesticide Safety DNA
    contains_aquatic_toxins = fields.Boolean("High Aquatic Toxicity Detected", compute='_compute_toxin_risk')

    @api.depends('production_id.move_raw_ids.product_id')
    def _compute_toxin_risk(self):
        for rec in self:
            # Check raw materials for toxic flags
            toxins = rec.production_id.move_raw_ids.filtered(lambda m: m.product_id.is_toxic_to_fish)
            rec.contains_aquatic_toxins = bool(toxins)

    def action_confirm(self):
        """ [Level 2 DNA] Hard-gate against fish poisoning. """
        self.ensure_one()
        # 1. Toxin check
        if self.contains_aquatic_toxins:
            raise UserError(_("ECOLOGICAL BLOCK: Pesticide %s is toxic to fish/shrimp! Operation cancelled to protect aquatic life.") % 
                           ", ".join(self.production_id.move_raw_ids.filtered(lambda m: m.product_id.is_toxic_to_fish).mapped('product_id.name')))
        
        # 2. Standard gates
        self.validate_quality_gate()
        return super(FarmSymbioticOrder, self).action_confirm()

class FarmLotRice(models.Model):
    """
    [ISL Layer] Ecological Rice Batch.
    """
    _name = 'farm.lot.rice'
    _description = 'Symbiotic Rice Batch'
    _inherits = {'stock.lot': 'lot_id'}
    _inherit = ['agri.traceability.mixin']

    lot_id = fields.Many2one('stock.lot', string='Base Lot', required=True, ondelete='cascade')
    linked_fish_lot_id = fields.Many2one('stock.lot', string="Co-cultured Aquatic Lot")
