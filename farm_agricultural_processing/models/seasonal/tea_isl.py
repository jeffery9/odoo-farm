# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class FarmTeaRecipe(models.Model):
    """
    [ISL Layer] Tea Processing Recipe (Protocol).
    Proxies mrp.bom to handle withering, fixing, and fermentation parameters.
    """
    _name = 'farm.tea.recipe'
    _description = 'Tea Processing Protocol'
    _inherits = {'mrp.bom': 'bom_id'}
    _inherit = ['agri.bom.mixin']

    bom_id = fields.Many2one('mrp.bom', string='Base BOM', required=True, ondelete='cascade')

    # Tea Specific Process Parameters [US-107-02]
    withering_hours = fields.Float("Withering Duration (Hours)")
    fixing_temperature = fields.Float("Fixing Temp (℃)")
    fermentation_degree = fields.Selection([
        ('none', 'None (Green)'),
        ('light', 'Light'),
        ('partial', 'Partial (Oolong)'),
        ('full', 'Full (Red/Black)')
    ], string="Fermentation Target")
    
    rolling_cycles = fields.Integer("Rolling Rounds")

class FarmTeaProduction(models.Model):
    """
    [ISL Layer] Tea Refinement Order.
    Proxies mrp.production to manage the physical transformation of fresh leaves.
    """
    _name = 'farm.tea.production'
    _description = 'Tea Refinement Order'
    _inherits = {'mrp.production': 'production_id'}
    _inherit = ['agri.quality.gate.mixin']

    production_id = fields.Many2one('mrp.production', string='Base Order', required=True, ondelete='cascade')

    # Seasonal Context [US-107-01]
    tea_season_id = fields.Many2one('agri.intervention.seasonal.bom', string="Tea Flush/Season")
    harvest_altitude = fields.Float("Leaf Altitude (m)", related='production_id.location_src_id.altitude_meters')

    def action_confirm(self):
        """ [Level 2 DNA] Quality Gate for Fresh Leaf input. """
        self.validate_quality_gate()
        return super(FarmTeaProduction, self).action_confirm()

class FarmLotTea(models.Model):
    """
    [ISL Layer] Refined Tea Batch.
    Holds sensory evaluation data and multi-stage DNA.
    """
    _name = 'farm.lot.tea'
    _description = 'Tea Batch/Lot'
    _inherits = {'stock.lot': 'lot_id'}
    _inherit = ['agri.traceability.mixin', 'agri.biological.valuation.mixin']

    lot_id = fields.Many2one('stock.lot', string='Base Lot', required=True, ondelete='cascade')

    # Sensory Evaluation [US-107-04]
    liquor_color_score = fields.Integer("Liquor Color (1-10)")
    aroma_intensity = fields.Integer("Aroma Score (1-10)")
    taste_purity = fields.Integer("Taste Score (1-10)")
    leaf_appearance = fields.Integer("Dry Leaf Score (1-10)")
    
    tea_grade = fields.Selection([
        ('super', 'Super Grade'),
        ('grade1', 'Grade 1'),
        ('grade2', 'Grade 2'),
        ('commercial', 'Commercial')
    ], string="Final Quality Grade")

    @api.depends('liquor_color_score', 'aroma_intensity', 'taste_purity')
    def _compute_fair_value(self):
        """ Premium value for high sensory scores. """
        res = super(FarmLotTea, self)._compute_fair_value()
        for rec in self:
            sensory_avg = (rec.liquor_color_score + rec.aroma_intensity + rec.taste_purity) / 3.0
            if sensory_avg > 8:
                rec.total_asset_value *= 1.5 # 50% Quality Premium
        return res
