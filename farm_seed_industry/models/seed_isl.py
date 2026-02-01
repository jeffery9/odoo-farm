# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
import hashlib

_logger = logging.getLogger(__name__)

class FarmSeedRecipe(models.Model):
    """
    [ISL Layer] Seed Coating/Treatment Recipe.
    Proxies mrp.bom to manage additive ratios and film-forming agents.
    """
    _name = 'farm.seed.recipe'
    _description = 'Seed Treatment Recipe'
    _inherits = {'mrp.bom': 'bom_id'}
    _inherit = ['farm.agri.bom.mixin', 'agri.nutrient.mixin']

    bom_id = fields.Many2one('mrp.bom', string='Base BOM', required=True, ondelete='cascade')

    # Coating Parameters
    film_forming_ratio = fields.Float("Film-forming Ratio (%)")
    target_moisture_content = fields.Float("Target Moisture (%)", default=13.0)

class FarmSeedBatch(models.Model):
    """
    [ISL Layer] Seed Batch/Lot.
    Holds "Four-Testing" metrics and parental lineage DNA.
    """
    _name = 'farm.seed.batch'
    _description = 'Seed Inventory Batch'
    _inherits = {'stock.lot': 'lot_id'}
    _inherit = [
        'agri.traceability.mixin', 
        'agri.biological.inventory.mixin', 
        'agri.certification.status.mixin'
    ]

    lot_id = fields.Many2one('stock.lot', string='Base Lot', required=True, ondelete='cascade')

    # [US-119-01] Lineage DNA
    parent_p1_hash = fields.Char("P1 (Sire) Hash")
    parent_p2_hash = fields.Char("P2 (Dam) Hash")
    
    # [US-119-02] Four-Testing Metrics (种子四检)
    germination_rate = fields.Float("Germination Rate (%)", group_operator='avg')
    purity_rate = fields.Float("Purity Rate (%)", group_operator='avg')
    clarity_rate = fields.Float("Clarity Rate (%)", group_operator='avg')
    moisture_content = fields.Float("Moisture Content (%)")
    
    thousand_seed_weight = fields.Float("Thousand Seed Weight (g)")

    # [US-119-04] PVP Compliance
    pvp_certificate_id = fields.Char("PVP Certificate No.")
    is_pvp_compliant = fields.Boolean("PVP Status OK", compute='_compute_pvp_compliance')

    @api.depends('certification_type', 'cert_expiry_date')
    def _compute_pvp_compliance(self):
        today = fields.Date.today()
        for rec in self:
            rec.is_pvp_compliant = rec.is_certified and rec.cert_expiry_date > today

    def action_verify_seed_quality(self):
        """ Hard block if germination is below standard. """
        self.ensure_one()
        if self.germination_rate < 85.0:
            raise UserError(_("SEED QUALITY BLOCK: Batch %s germination rate (%s%%) is below national standard.") % 
                           (self.lot_id.name, self.germination_rate))
        return True

class FarmSeedProduction(models.Model):
    """
    [ISL Layer] Propagation or Coating Order.
    """
    _name = 'farm.seed.production'
    _description = 'Seed Propagation Order'
    _inherits = {'mrp.production': 'production_id'}
    _inherit = ['farm.agri.production.mixin', 'agri.quality.gate.mixin']

    production_id = fields.Many2one('mrp.production', string='Base Order', required=True, ondelete='cascade')

    def action_confirm(self):
        """ [Level 2 DNA] Enforce Purity checks before propagation. """
        self.validate_quality_gate()
        return super(FarmSeedProduction, self).action_confirm()
