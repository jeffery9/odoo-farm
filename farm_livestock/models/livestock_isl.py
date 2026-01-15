# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class FarmLivestockBom(models.Model):
    _name = 'farm.livestock.bom'
    _description = 'Livestock Breeding BOM (ISL Layer)'
    _inherits = {'mrp.bom': 'bom_id'}
    _inherit = ['farm.agri.bom.mixin']

    bom_id = fields.Many2one('mrp.bom', string='Base BOM', required=True, ondelete='cascade')
    
    # Livestock Specifics
    growth_days_expected = fields.Integer("Expected Growth Days")
    daily_feed_intake = fields.Float("Avg Daily Feed (kg)")

class FarmLivestockProduction(models.Model):
    _name = 'farm.livestock.production'
    _description = 'Livestock Growth Order (ISL Layer)'
    _inherits = {'mrp.production': 'production_id'}
    _inherit = ['farm.agri.production.mixin']

    production_id = fields.Many2one('mrp.production', string='Base Production Order', required=True, ondelete='cascade')

    # Weight Gain & Efficiency (Moved from Base)
    initial_total_weight = fields.Float("Initial Total Weight (kg)")
    final_total_weight = fields.Float("Final Total Weight (kg)")
    fcr = fields.Float("Feed Conversion Ratio (FCR)", compute='_compute_fcr_isl')

    # --- Polymorphic Link (US-TECH-06-26) ---
    livestock_bom_id = fields.Many2one('farm.livestock.bom', string='Livestock Recipe', compute='_compute_livestock_bom_id')

    def _compute_livestock_bom_id(self):
        """ Automatically up-cast base bom_id to ISL livestock.bom. """
        for rec in self:
            if rec.bom_id:
                rec.livestock_bom_id = self.env['farm.livestock.bom'].search([('bom_id', '=', rec.bom_id.id)], limit=1)
            else:
                rec.livestock_bom_id = False

    @api.depends('initial_total_weight', 'final_total_weight')
    def _compute_fcr_isl(self):
        for rec in self:
            gain = rec.final_total_weight - rec.initial_total_weight
            # Basic FCR placeholder
            rec.fcr = (rec.product_qty / gain) if gain > 0 else 0.0

    def isl_post_done(self):
        """ US-TECH-06-27: Update resulting lot metadata with ISL weight data. """
        self.ensure_one()
        if self.production_id.lot_producing_id:
            lot = self.production_id.lot_producing_id
            # Search for ISL lot record
            isl_lot = self.env['farm.lot.livestock'].search([('lot_id', '=', lot.id)], limit=1)
            if isl_lot:
                isl_lot.current_weight = self.final_total_weight / (self.production_id.product_qty or 1.0)
