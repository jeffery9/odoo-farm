# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class FarmLotHarvest(models.Model):
    _name = 'farm.lot.harvest'
    _description = 'Land Harvest Lot (ISL Layer)'
    _inherits = {'stock.lot': 'lot_id'}

    lot_id = fields.Many2one('stock.lot', string='Base Lot', required=True, ondelete='cascade')
    
    # Harvest Specifics (Moved from Base)
    plot_id = fields.Many2one('farm.land', string='Origin Plot')
    terroir_attributes_json = fields.Text("Terroir Attributes (JSON)")

class FarmLotLivestock(models.Model):
    _name = 'farm.lot.livestock'
    _description = 'Livestock Asset Lot (ISL Layer)'
    _inherits = {'stock.lot': 'lot_id'}

    lot_id = fields.Many2one('stock.lot', string='Base Lot', required=True, ondelete='cascade')
    
    # Livestock Specifics (Moved from Base)
    birth_date = fields.Date("Birth Date")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    current_weight = fields.Float("Weight (kg)")

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

