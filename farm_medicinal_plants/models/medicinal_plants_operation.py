# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class FarmMedicinalProduction(models.Model):
    """
    [ISL Layer] GMP Medicinal Processing & Cultivation Order.
    Proxies mrp.production to handle complex extraction and drying.
    """
    _name = 'farm.medicinal.production'
    _description = 'Medicinal Processing Order'
    _inherits = {'mrp.production': 'production_id'}
    _inherit = [
        'agri.intervention.mixin',
        'agri.growth.cycle.mixin',
        'agri.quality.gate.mixin'
    ]

    production_id = fields.Many2one('mrp.production', string='Base Order', required=True, ondelete='cascade')

    # Active Compound Monitoring [US-106-02]
    current_compound_level = fields.Float("Active Compound (%)", group_operator='avg')
    target_compound_level = fields.Float("Standard Threshold (%)")
    
    is_daodi_verified = fields.Boolean("Daodi Origin Verified", default=False)

    def action_confirm(self):
        """ [Level 2 DNA] Enforce Daodi and PHI checks. """
        self.ensure_one()
        # Quality Gate check for GMP compliance
        self.validate_quality_gate()
        return super(FarmMedicinalProduction, self).action_confirm()

class FarmLotMedicinal(models.Model):
    """
    [ISL Layer] Digital Twin of a Medicinal Asset.
    """
    _name = 'farm.lot.medicinal'
    _description = 'Medicinal Asset/Batch'
    _inherits = {'stock.lot': 'lot_id'}
    _inherit = ['agri.traceability.mixin']

    lot_id = fields.Many2one('stock.lot', string='Base Lot', required=True, ondelete='cascade')

    # [US-106-01] Traceability context
    altitude_meters = fields.Float("Harvest Altitude (m)")
    soil_ph_at_origin = fields.Float("Origin Soil pH")
    
    analysis_date = fields.Date("Last Analysis")
    certified_compound_level = fields.Float("Certified Active Compound (%)")

class FarmMedicinalRecipe(models.Model):
    """
    [ISL Layer] Processing Protocol (炮制规范).
    """
    _name = 'farm.medicinal.recipe'
    _description = 'Medicinal Processing Protocol'
    _inherits = {'mrp.bom': 'bom_id'}
    
    bom_id = fields.Many2one('mrp.bom', string='Base BOM', required=True, ondelete='cascade')
    
    drying_temperature = fields.Float("Drying Target Temp (℃)")
    max_humidity_threshold = fields.Float("Max Humidity (%)")
