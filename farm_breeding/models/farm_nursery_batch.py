# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class FarmNurseryBatch(models.Model):
    """
    [ISL Layer] Digital Twin of a Nursery Seedling Batch.
    Proxies stock.lot to hold biological DNA and lineage.
    """
    _name = 'farm.nursery.batch'
    _description = 'Breeding Nursery Batch'
    _inherits = {'stock.lot': 'lot_id'}
    _inherit = [
        'mail.thread', 
        'mail.activity.mixin',
        'agri.growth.cycle.mixin',
        'agri.biological.inventory.mixin',
        'agri.traceability.mixin'
    ]

    lot_id = fields.Many2one('stock.lot', string='Base Lot', required=True, ondelete='cascade')

    # Lineage DNA [US-BREED-01]
    parent_p1_id = fields.Many2one('stock.lot', string="Parent P1 (Sire/Male)")
    parent_p2_id = fields.Many2one('stock.lot', string="Parent P2 (Dam/Female)")
    
    # Nursery Specifics [US-BREED-02]
    sowing_date = fields.Date("Sowing Date", default=fields.Date.today)
    estimated_transplant_gdd = fields.Float("Target GDD for Transplant", default=200.0)

    # Transition Math [US-BREED-03]
    target_land_area = fields.Float("Target Field Area (mu/ha)")
    target_density = fields.Float("Target Planting Density")

    def action_create_transplant_task(self):
        """ [Authoring-Style: To Field] Seamlessly transitions seedlings to Field Crops. """
        self.ensure_one()
        # 1. Create Field Operation Order (mrp.production proxy)
        # 2. Inherit DNA (Lineage, GDD, Traceability Hash)
        _logger.info("BREEDING: Batch %s ready for field entry.", self.name)
        return True

class FarmBreedingOrder(models.Model):
    """
    [ISL Layer] Nursery Instruction Packet.
    Proxies mrp.production to manage the germination and growth workstream.
    """
    _name = 'farm.breeding.order'
    _description = 'Nursery Growing Order'
    _inherits = {'mrp.production': 'production_id'}
    _inherit = ['farm.agri.production.mixin', 'agri.quality.gate.mixin']

    production_id = fields.Many2one('mrp.production', string='Base Order', required=True, ondelete='cascade')

    # Germination Logic [US-BREED-04]
    target_germination_rate = fields.Float("Target Germination (%)", default=95.0)
    actual_germination_rate = fields.Float("Actual Germination (%)")

    def action_confirm(self):
        """ DNA Gate: Check variety purity before starting nursery. """
        self.validate_quality_gate()
        return super(FarmBreedingOrder, self).action_confirm()