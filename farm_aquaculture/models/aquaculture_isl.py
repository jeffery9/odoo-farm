# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class FarmAquacultureBom(models.Model):
    _name = 'farm.aquaculture.bom'
    _description = 'Aquaculture Breeding/Growth BOM (ISL Layer)'
    _inherits = {'mrp.bom': 'bom_id'}
    _inherit = ['farm.agri.bom.mixin']

    bom_id = fields.Many2one('mrp.bom', string='Base BOM', required=True, ondelete='cascade')

    # Aquaculture Specifics
    pond_type = fields.Selection([
        ('earthen', 'Earthen Pond'),
        ('concrete', 'Concrete Tank'),
        ('raceway', 'Raceway'),
        ('cage', 'Floating Cage')
    ], string="Pond/Tank Type")
    
    target_dissolved_oxygen = fields.Float("Target Dissolved Oxygen (mg/L)")
    target_ph_range = fields.Char("Target pH Range")
    stocking_density_limit = fields.Float("Max Stocking Density (heads/m³)")

class FarmLotAquaculture(models.Model):
    _name = 'farm.lot.aquaculture'
    _description = 'Aquaculture Asset Lot (ISL Layer)'
    _inherits = {'stock.lot': 'lot_id'}

    lot_id = fields.Many2one('stock.lot', string='Base Lot', required=True, ondelete='cascade')
    
    # Aquaculture Specifics
    stocking_date = fields.Date("Stocking Date")
    initial_count = fields.Integer("Initial Count")
    current_count = fields.Integer("Current Count")
    water_volume_m3 = fields.Float("Water Volume (m³)")

class FarmAquacultureProduction(models.Model):
    _name = 'farm.aquaculture.production'
    _description = 'Aquaculture Growth Order (ISL Layer)'
    _inherits = {'mrp.production': 'production_id'}
    _inherit = ['farm.agri.production.mixin']

    production_id = fields.Many2one('mrp.production', string='Base Production Order', required=True, ondelete='cascade')

    # Water Quality Monitoring (ISL Level)
    water_temp = fields.Float("Water Temperature (℃)")
    dissolved_oxygen = fields.Float("Dissolved Oxygen (mg/L)")
    ph_level = fields.Float("pH Level")
    
    # Growth Stats
    avg_individual_weight = fields.Float("Avg Individual Weight (g)")
    survival_rate = fields.Float("Survival Rate (%)", default=100.0)

    # --- Polymorphic Link ---
    aquaculture_bom_id = fields.Many2one('farm.aquaculture.bom', string='Aquaculture Recipe', compute='_compute_aquaculture_bom_id')

    def _compute_aquaculture_bom_id(self):
        for rec in self:
            if rec.bom_id:
                rec.aquaculture_bom_id = self.env['farm.aquaculture.bom'].search([('bom_id', '=', rec.bom_id.id)], limit=1)
            else:
                rec.aquaculture_bom_id = False