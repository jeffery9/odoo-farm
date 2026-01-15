# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class FarmAgriBomMixin(models.AbstractModel):
    _name = 'farm.agri.bom.mixin'
    _description = 'Agricultural BOM Shared Logic'

    # --- Generic Agri Fields ---
    dilution_ratio = fields.Float("Dilution Ratio", help="1:X ratio for tank mix.")
    solution_volume_per_hectare = fields.Float("Solution Volume per Hectare")
    
    # --- Potency & Standardization ---
    is_potency_controlled = fields.Boolean("Potency Controlled", default=False)
    target_active_content = fields.Float("Target Active Content (%)")

    # --- Compliance & Safety ---
    max_loss_rate = fields.Float("Max Allowed Loss Rate (%)", default=5.0)
    is_blind_mixing = fields.Boolean("Blind Mixing Mode", default=False)

class FarmAgriProductionMixin(models.AbstractModel):
    _name = 'farm.agri.production.mixin'
    _description = 'Agricultural Production Shared Logic'

    # --- Quality & Process Interception ---
    quality_gate_status = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rework', 'Rework'),
        ('rejected', 'Rejected'),
    ], string='Quality Gate Status', default='pending', copy=False)

    # --- Common Lifecycle Tracking ---
    processing_type = fields.Selection([
        ('primary', 'Primary Processing'),
        ('deep', 'Deep Processing'),
        ('fattening', 'Growth/Fattening'),
        ('breeding', 'Breeding Operations')
    ], string='Agricultural Process Type')

    def isl_post_confirm(self):
        """ US-TECH-06-27: Hook triggered after standard MO confirmation. """
        pass

    def isl_post_done(self):
        """ US-TECH-06-27: Hook triggered after standard MO completion. """
        pass
