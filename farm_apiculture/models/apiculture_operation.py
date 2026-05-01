# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class FarmLotHive(models.Model):
    """
    [ISL Layer] Digital Twin of a Bee Hive/Colony.
    Proxies stock.lot to track biological population and queen lineage.
    """
    _name = 'farm.lot.hive'
    _description = 'Bee Hive Asset'
    _inherits = {'stock.lot': 'lot_id'}
    _inherit = [
        'agri.biological.inventory.mixin',
        'agri.geospatial.mixin',
        'agri.traceability.mixin'
    ]

    lot_id = fields.Many2one('stock.lot', string='Base Lot', required=True, ondelete='cascade')

    # Queen Status [US-110-01]
    queen_status = fields.Selection([
        ('good', 'Good'),
        ('queenless', 'Queenless'),
        ('new_queen', 'New Queen'),
        ('supersedure', 'Supersedure')
    ], string="Queen Status", default='good')
    
    queen_age_months = fields.Integer("Queen Age (Months)")
    colony_strength = fields.Selection([
        ('1', 'Weak'), ('2', 'Moderate'), ('3', 'Strong'), ('4', 'Very Strong')
    ], string="Colony Strength", default='2')

class FarmApicultureOrder(models.Model):
    """
    [ISL Layer] Honey Flow / Production Order.
    Proxies mrp.production to manage the foraging and harvesting cycle.
    """
    _name = 'farm.apiculture.order'
    _description = 'Honey Flow Production'
    _inherits = {'mrp.production': 'production_id'}
    _inherit = ['agri.intervention.mixin', 'agri.quality.gate.mixin']

    production_id = fields.Many2one('mrp.production', string='Base Order', required=True, ondelete='cascade')

    # Foraging Context [US-110-02]
    target_nectar_source = fields.Char("Target Nectar Plant")
    foraging_radius_km = fields.Float("Effective Radius (km)", default=3.0)
    
    honey_moisture_target = fields.Float("Target Moisture (%)", default=18.0)

    def action_confirm(self):
        """ [Level 2 DNA] Check hive health before deployment. """
        # Simplified: Check if linked lots (hives) are strong enough
        self.validate_quality_gate()
        return super(FarmApicultureOrder, self).action_confirm()

class FarmHiveInspection(models.Model):
    """
    [ISL Layer] Hive Inspection Task.
    Proxies project.task for regular health and swarm checks.
    """
    _name = 'farm.hive.inspection'
    _description = 'Hive Inspection'
    _inherits = {'project.task': 'task_id'}
    
    task_id = fields.Many2one('project.task', required=True, ondelete='cascade')
    hive_id = fields.Many2one('farm.lot.hive', string="Hive to Inspect")
    
    is_swarm_prevented = fields.Boolean("Swarm Control Done")
    disease_detected = fields.Boolean("Diseases Found", default=False)

    def action_done(self):
        """ Sync inspection results back to Hive Asset. """
        self.ensure_one()
        # Logic: Update hive_id.queen_status based on inspection
        return self.task_id.action_fsm_validate()
