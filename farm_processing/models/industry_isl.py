# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class FarmPharmaBom(models.Model):
    """ Pharmaceutical Processing BOM [US-14-24] """
    _name = 'farm.pharma.bom'
    _description = 'Pharmaceutical Processing BOM (ISL Layer)'
    _inherits = {'mrp.bom': 'bom_id'}
    _inherit = ['farm.agri.bom.mixin']

    bom_id = fields.Many2one('mrp.bom', string='Base BOM', required=True, ondelete='cascade')
    
    gmp_standard = fields.Char("GMP Standard Reference")
    active_ingredient_id = fields.Many2one('product.product', string="Primary Active Ingredient")
    concentration_target = fields.Float("Target Concentration (%)")
    safety_data_sheet = fields.Binary("MSDS Document")

class FarmPharmaProduction(models.Model):
    """ Pharmaceutical Production Order [US-14-24] """
    _name = 'farm.pharma.production'
    _description = 'Pharmaceutical Production Order (ISL Layer)'
    _inherits = {'mrp.production': 'production_id'}
    _inherit = ['farm.agri.production.mixin']

    production_id = fields.Many2one('mrp.production', string='Base Production Order', required=True, ondelete='cascade')
    
    batch_record_ref = fields.Char("Electronic Batch Record (EBR) ID")
    potency_verified = fields.Boolean("Potency Verified", default=False)
    impurity_level = fields.Float("Impurity Level (%)")

class FarmChemicalBom(models.Model):
    """ Chemical Processing BOM [US-14-25] """
    _name = 'farm.chemical.bom'
    _description = 'Chemical Processing BOM (ISL Layer)'
    _inherits = {'mrp.bom': 'bom_id'}
    _inherit = ['farm.agri.bom.mixin']

    bom_id = fields.Many2one('mrp.bom', string='Base BOM', required=True, ondelete='cascade')
    
    hazard_class = fields.Selection([
        ('explosive', 'Explosive'),
        ('oxidizing', 'Oxidizing'),
        ('toxic', 'Toxic'),
        ('corrosive', 'Corrosive'),
        ('none', 'Non-Hazardous')
    ], string="Hazard Classification")
    reaction_temperature_limit = fields.Float("Max Reaction Temp (℃)")

class FarmChemicalProduction(models.Model):
    """ Chemical Production Order [US-14-25] """
    _name = 'farm.chemical.production'
    _description = 'Chemical Production Order (ISL Layer)'
    _inherits = {'mrp.production': 'production_id'}
    _inherit = ['farm.agri.production.mixin']

    production_id = fields.Many2one('mrp.production', string='Base Production Order', required=True, ondelete='cascade')
    
    leak_test_passed = fields.Boolean("Leak Test Passed", default=True)
    solvent_recovery_qty = fields.Float("Solvent Recovered (L)")
