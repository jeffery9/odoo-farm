# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class FarmViticulturePlot(models.Model):
    """
    [ISL Layer] Digital Twin of a Vineyard Plot or Row. [De-industrialized]
    Proxies farm.location to hold terroir and trellis metadata.
    """
    _name = 'farm.viticulture.plot'
    _description = 'Vineyard Plot'
    _inherits = {'farm.location': 'location_id'}
    _inherit = ['agri.geospatial.mixin']

    location_id = fields.Many2one('farm.location', required=True, ondelete='cascade')

    # Terroir DNA [US-115-01]
    trellis_system = fields.Selection([
        ('guyot_single', 'Single Guyot'),
        ('guyot_double', 'Double Guyot'),
        ('cordon', 'Cordon de Royat'),
        ('pergola', 'Trellis/Pergola')
    ], string="Trellis System")
    
    vine_spacing = fields.Float("Vine Spacing (m)")
    row_orientation = fields.Float("Row Azimuth (Degree)")

class FarmVineyardTask(models.Model):
    """
    [ISL Layer] Vineyard Nurturing Task. [De-industrialized]
    Proxies mrp.production to manage pruning, canopy management, and harvest.
    """
    _name = 'farm.viticulture.task'
    _description = 'Vineyard Nurturing Task'
    _inherits = {'mrp.production': 'intervention_id'}
    _inherit = [
        'agri.intervention.mixin',
        'agri.growth.cycle.mixin',
    ]

    intervention_id = fields.Many2one('mrp.production', string='Base Intervention', required=True, ondelete='cascade')

    # [US-115-02] Pruning & Yield Control
    pruned_buds_per_vine = fields.Integer("Pruned Buds per Vine")
    target_brix = fields.Float("Target Ripeness (Brix)", default=22.0)

    def action_confirm(self):
        """ DNA Gate: Base logic triggers weather and compliance checks. """
        return super(FarmVineyardTask, self).action_confirm()

class FarmLotGrape(models.Model):
    """
    [ISL Layer] Grape Harvest Batch. [De-industrialized]
    Holds ripeness fingerprints and pressing data.
    """
    _name = 'farm.lot.grape'
    _description = 'Grape Batch'
    _inherits = {'stock.lot': 'lot_id'}
    _inherit = ['agri.traceability.mixin', 'agri.quality.gate.mixin']

    lot_id = fields.Many2one('stock.lot', string='Base Lot', required=True, ondelete='cascade')

    # Ripeness Metadata [US-115-03]
    brix_level = fields.Float("Brix (Sugar)")
    titratable_acidity = fields.Float("TA (g/L)")
    ph_level = fields.Float("Juice pH")
    
    # [US-115-04] Pressing Context
    juice_yield_volume = fields.Float("Extracted Juice (L)")
    pressing_ratio = fields.Float("Pressing Ratio (L/kg)", compute='_compute_pressing_ratio', store=True, precompute=True)

    @api.depends('juice_yield_volume', 'product_qty')
    def _compute_pressing_ratio(self):
        for rec in self:
            rec.pressing_ratio = rec.juice_yield_volume / rec.product_qty if rec.product_qty > 0 else 0.0
