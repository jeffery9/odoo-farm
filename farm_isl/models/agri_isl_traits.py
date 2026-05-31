# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class AgriISLFoodSafetyTrait(models.AbstractModel):
    """ [ISP Trait] Food Safety Compliance (HACCP) """
    _name = 'agri.isl.trait.food_safety'
    _description = 'ISL Trait: Food Safety'

    haccp_plan = fields.Html('HACCP Plan')
    allergen_control = fields.Boolean('Allergen Control')
    allergen_information = fields.Html('Allergen Information')
    quality_gate_checks = fields.Text('Quality Gate Checks')
    ccp_monitoring = fields.Html('CCP Monitoring')

class AgriISLLivestockTrait(models.AbstractModel):
    """ [ISP Trait] Livestock & Pharma Compliance (GMP) """
    _name = 'agri.isl.trait.livestock'
    _description = 'ISL Trait: Livestock'

    gmp_compliance = fields.Boolean('GMP Compliance')
    active_ingredient = fields.Char('Active Ingredient')
    sterility_date = fields.Date('Sterility Date')
    kill_date = fields.Date('Kill Date')
    batch_record = fields.Html('Batch Record')
    pharmacological_class = fields.Char('Pharmacological Class')

class AgriISLAquacultureTrait(models.AbstractModel):
    """ [ISP Trait] Aquaculture & Water Quality """
    _name = 'agri.isl.trait.aquaculture'
    _description = 'ISL Trait: Aquaculture'

    safety_procedures = fields.Html('Safety Procedures')
    water_quality_standard = fields.Char('Water Quality Standard')

class AgriISLChemicalTrait(models.AbstractModel):
    """ [ISP Trait] Chemical & Controlled Substance Handling """
    _name = 'agri.isl.trait.chemical'
    _description = 'ISL Trait: Chemical'

    explosion_proof = fields.Boolean('Explosion Proof')
    safety_coefficient = fields.Float('Safety Coefficient', default=1.0)
    hazard_class = fields.Char('Hazard Class')

class AgriISLTraceabilityTrait(models.AbstractModel):
    """ [ISP Trait] General Traceability & Logistics """
    _name = 'agri.isl.trait.traceability'
    _description = 'ISL Trait: Traceability'

    traceability_requirements = fields.Html('Traceability Requirements')
    chain_of_custody = fields.Html('Chain of Custody')
    temperature_log = fields.Html('Temperature Log')
    humidity_log = fields.Html('Humidity Log')
    security_seal = fields.Char('Security Seal')
