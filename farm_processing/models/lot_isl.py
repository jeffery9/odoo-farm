# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class FarmLotHarvest(models.Model):
    _name = 'farm.lot.harvest'
    _description = 'Land Harvest Lot (ISL Layer)'
    _inherits = {'stock.lot': 'lot_id'}

    lot_id = fields.Many2one('stock.lot', string='Base Lot', required=True, ondelete='cascade')
    
    # Harvest Specifics (Moved from Base)
    # plot_id = fields.Many2one('farm.land', string='Origin Plot')
    terroir_attributes_json = fields.Text("Terroir Attributes (JSON)")