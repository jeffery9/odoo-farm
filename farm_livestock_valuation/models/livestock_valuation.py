# -*- coding: utf-8 -*-
from odoo import models, fields, api

class FarmLivestock(models.Model):
    _name = 'farm.livestock'
    _description = 'Farm Livestock'

    name = fields.Char("Name", required=True)
    breed_coefficient = fields.Float("Breed Coefficient", default=1.0)

class LivestockWeightRecord(models.Model):
    _name = 'livestock.weight.record'
    _description = 'Livestock Weight Record'

    livestock_id = fields.Many2one('farm.livestock', string="Livestock", required=True)
    measured_weight = fields.Float("Measured Weight (kg)", required=True)
    rfid_tag = fields.Char("RFID Tag")
    telemetry_time = fields.Datetime("Telemetry Time", default=fields.Datetime.now)

class LivestockBiomassValuator(models.Model):
    _inherit = 'farm.financial.asset.valuation'

    livestock_asset_id = fields.Many2one('farm.livestock', string="Livestock Asset")

    @api.model
    def _get_specialized_algorithms(self):
        """ Register the vertical livestock weight-growth curve valuation strategy """
        res = {}
        if hasattr(super(LivestockBiomassValuator, self), '_get_specialized_algorithms'):
            res = super(LivestockBiomassValuator, self)._get_specialized_algorithms()
        res['livestock'] = self._calculate_livestock_growth_valuation
        return res

    def _calculate_livestock_growth_valuation(self):
        self.ensure_one()
        if not self.livestock_asset_id:
            return 0.0
            
        # 1. Fetch L1 raw weight telemetry records
        weight_record = self.env['livestock.weight.record'].search([
            ('livestock_id', '=', self.livestock_asset_id.id)
        ], order='telemetry_time desc', limit=1)
        
        # 2. Execute biomass dynamic curve computation: Weight * Breed Coeff * Base Rate (12.5)
        if weight_record:
            return weight_record.measured_weight * self.livestock_asset_id.breed_coefficient * 12.5
        return 0.0

    def action_compute_biomass_valuation(self):
        self.ensure_one()
        algorithms = self._get_specialized_algorithms()
        if 'livestock' in algorithms:
            return algorithms['livestock']()
        return 0.0
