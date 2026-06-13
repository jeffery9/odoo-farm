# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
import json

_logger = logging.getLogger(__name__)

class FarmCropRecipe(models.Model):
    """
    Crop Farming Recipe (ISL Layer) [De-industrialized]
    """
    _name = 'farm.crop.recipe'
    _description = 'Crop Farming Recipe'
    _inherits = {'mrp.bom': 'recipe_id'}
    _inherit = ['agri.bom.mixin', 'agri.nutrient.mixin']

    recipe_id = fields.Many2one('mrp.bom', string='Base Recipe', required=True, ondelete='cascade')

    # Crop Specifics [US-CROP-02]
    target_yield_mu = fields.Float("Target Yield per Mu (kg)")
    growing_season = fields.Selection([
        ('spring', 'Spring'), ('summer', 'Summer'), ('autumn', 'Autumn'), ('winter', 'Winter')
    ], string="Growing Season")

    phi_days = fields.Integer("Pre-Harvest Interval (PHI) Days")

class FarmCropTask(models.Model):
    """
    Crop Farming Task (ISL Layer) - Precision Intervention [De-industrialized]
    """
    _name = 'farm.crop.task'
    _description = 'Crop Farming Task'
    _inherits = {'mrp.production': 'intervention_id'}
    _inherit = [
        'agri.intervention.mixin',
        'agri.agent.instruction.mixin',
    ]

    intervention_id = fields.Many2one('mrp.production', string='Base Intervention', required=True, ondelete='cascade')

    # [US-CROP-02] VRA Prescription Mapping
    is_vra_enabled = fields.Boolean("Enable Variable Rate Application", default=False)
    prescription_json = fields.Text("Prescription Map (JSON)")

    def action_confirm(self):
        """ [Level 2 DNA] Precision Gating for Field Crops. """
        self.ensure_one()
        
        # 1. Base Engine Logic (triggers Compliance, Nutrient, Weather plugins)
        res = super(FarmCropTask, self).action_confirm()
        
        # 2. VRA Instruction generation [US-CROP-02]
        if self.is_vra_enabled:
            self.apply_vra_instruction_skill()
            
        return res

    def apply_vra_instruction_skill(self):
        """ Transforms Prescription into Machine Instruction (Level 4 DNA). """
        self.ensure_one()
        payload = {
            'action': 'execute_vra',
            'base_rate': 15.0,
            'map_ref': self.prescription_json or 'standard_grid',
            'target_area': self.production_id.location_src_id.name
        }
        self.agent_instruction_json = json.dumps(payload, indent=2)
        self.agent_status_feedback = 'pending'

class FarmCropLot(models.Model):
    """
    Crop Harvest Batch (ISL Layer)
    """
    _name = 'farm.crop.lot'
    _description = 'Crop Harvest Batch (ISL Layer)'
    _inherits = {'stock.lot': 'lot_id'}
    _inherit = ['agri.traceability.mixin', 'agri.nutrient.mixin']

    lot_id = fields.Many2one('stock.lot', string='Base Lot', required=True, ondelete='cascade')

    # [US-CROP-03] DNA Inheritance
    plot_origin_id = fields.Many2one('farm.location', string='Origin Plot')
    moisture_content = fields.Float("Grain Moisture (%)")
    protein_content = fields.Float("Protein Content (%)")