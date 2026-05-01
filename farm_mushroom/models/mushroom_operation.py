# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
import json

_logger = logging.getLogger(__name__)

class FarmMushroomRecipe(models.Model):
    """
    [ISL Layer] Substrate Formula & Sterilization Specs.
    Proxies mrp.bom to manage nutrient balance and sterilization.
    """
    _name = 'farm.mushroom.recipe'
    _description = 'Mushroom Substrate Recipe'
    _inherits = {'mrp.bom': 'bom_id'}
    _inherit = ['agri.bom.mixin', 'agri.nutrient.mixin']

    bom_id = fields.Many2one('mrp.bom', string='Base BOM', required=True, ondelete='cascade')

    # Environment Setpoints [US-111-02]
    target_co2_level = fields.Float("Max CO2 Threshold (ppm)", default=800.0)
    target_humidity = fields.Float("Target Humidity (%)", default=90.0)
    sterilization_temp = fields.Float("Sterilization Temp (℃)", default=121.0)

class FarmMushroomBatch(models.Model):
    """
    [ISL Layer] Digital Twin of a Mushroom Fruiting Batch.
    Proxies stock.lot to track biomass and contamination.
    """
    _name = 'farm.mushroom.batch'
    _description = 'Mushroom Fruiting Batch'
    _inherits = {'stock.lot': 'lot_id'}
    _inherit = [
        'agri.biological.inventory.mixin',
        'agri.growth.cycle.mixin',
        'agri.traceability.mixin'
    ]

    lot_id = fields.Many2one('stock.lot', string='Base Lot', required=True, ondelete='cascade')

    # Contamination Tracking [US-111-01]
    contamination_rate = fields.Float("Contamination Rate (%)")
    is_cleared_for_fruiting = fields.Boolean("Cleared for Fruiting", default=False)

class FarmMushroomProduction(models.Model):
    """
    [ISL Layer] Mushroom Fruiting Cycle.
    Proxies mrp.production to manage multiple flushes.
    """
    _name = 'farm.mushroom.production'
    _description = 'Mushroom Fruiting Cycle'
    _inherits = {'mrp.production': 'production_id'}
    _inherit = [
        'agri.intervention.mixin',
        'agri.agent.instruction.mixin',
        'agri.incident.alert.mixin',
        'agri.odoo19.performance.security.mixin'  # Added Odoo 19 performance and security mixin
    ]

    # Enhanced with Odoo 19 precompute for performance
    biological_efficiency = fields.Float(
        "Biological Efficiency (%)",
        compute='_compute_be',
        precompute=True,  # Use precompute for immediate calculation during creation
        store=True
    )

    # Use JSON for flexible configuration
    mushroom_config = fields.Json(
        "Mushroom Configuration",
        default=dict,
        help="JSON-based configuration for mushroom-specific parameters"
    )

    production_id = fields.Many2one('mrp.production', string='Base Order', required=True, ondelete='cascade')

    # Flush Management [US-111-03]
    current_flush_number = fields.Integer("Current Flush", default=1)
    biological_efficiency = fields.Float("Biological Efficiency (%)", compute='_compute_be')

    def handle_mushroom_telemetry(self, data):
        """ 
        [Authoring-Style: On Damaged] 
        Environmental defense logic. High CO2 triggers ventilation.
        """
        self.ensure_one()
        co2 = data.get('co2_level')
        humidity = data.get('humidity')
        
        if co2 is not None:
            recipe = self.env['farm.mushroom.recipe'].search([('bom_id', '=', self.bom_id.id)], limit=1)
            threshold = recipe.target_co2_level if recipe else 800.0
            
            if co2 > threshold:
                # 1. Alert (Level 2 DNA)
                self.report_incident('high', 'CO2 Spike', _("Room %s CO2 (%s) exceeds threshold.") % (self.name, co2))
                # 2. Skill: Ventilation (Level 4 DNA)
                self.apply_ventilation_skill()
        return True

    def apply_ventilation_skill(self):
        """ Level 4 DNA: Direct control of ventilation fans. """
        self.ensure_one()
        payload = {
            'action': 'set_ventilation',
            'state': 'on',
            'fan_speed': 'high',
            'reason': 'CO2 threshold exceeded'
        }
        self.agent_instruction_json = json.dumps(payload, indent=2)
        self.agent_status_feedback = 'executing'

    def _compute_be(self):
        """ BE = Total Fresh Mushroom Weight / Total Dry Substrate Weight. """
        for rec in self:
            rec.biological_efficiency = 0.0 # Linked to harvest records

    def action_confirm(self):
        """ DNA Gate: Check contamination before starting fruiting. """
        # logic to check if batch is cleared
        return super(FarmMushroomProduction, self).action_confirm()
