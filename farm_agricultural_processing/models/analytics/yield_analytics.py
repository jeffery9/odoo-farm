# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class FarmProcessingProductionAnalyticsExtension(models.Model):
    """
    Extension to Processing ISL Production Model for Analytics - US-14-16
    """
    _inherit = 'farm.processing.production'

    # Yield analytics tracking
    yield_rate = fields.Float('Yield Rate (%)', compute='_compute_yield_rate', store=True)

    # @api.depends('final_output_qty', 'raw_material_qty')
    def _compute_yield_rate(self):
        for record in self:
            if record.raw_material_qty > 0:
                record.yield_rate = (record.final_output_qty / record.raw_material_qty) * 100
            else:
                record.yield_rate = 0.0


class AgriProcessingYieldRateAnalytics(models.Model):
    """
    Yield Rate Multi-dimensional Analytics - US-14-16
    """
    _name = 'agri.processing.yield.rate.analytics'
    _description = 'Yield Rate Multi-dimensional Analytics'
    _order = 'production_date desc'

    name = fields.Char('Analytics Record', required=True)
    production_id = fields.Many2one('farm.processing.production', string='Production Order', required=True)
    production_date = fields.Date('Production Date', required=True)

    # Yield metrics
    input_qty = fields.Float('Input Quantity')
    output_qty = fields.Float('Output Quantity')
    yield_rate = fields.Float('Yield Rate (%)', required=True)

    # Dimensions for analysis
    batch_id = fields.Many2one('stock.lot', string='Batch')
    season = fields.Char('Season')
    operator_id = fields.Many2one('res.users', string='Operator')
    equipment_id = fields.Many2one('mrp.workcenter', string='Equipment Used')
    raw_material_source = fields.Many2one('stock.lot', string='Raw Material Source')

    # Benchmarking
    standard_yield_rate = fields.Float('Standard Yield Rate (%)')
    yield_variance = fields.Float('Yield Variance (%)', compute='_compute_yield_variance', store=True)

    # Efficiency factors
    processing_time_hours = fields.Float('Processing Time (hours)')
    energy_consumption_kwh = fields.Float('Energy Consumption (kWh)')
    energy_efficiency = fields.Float('Energy Efficiency (output/kWh)', compute='_compute_efficiency', store=True)

    notes = fields.Text('Analysis Notes')

    @api.model
    def create(self, vals):
        if 'name' not in vals or not vals['name']:
            vals['name'] = 'YIELD/' + fields.Date.to_string(fields.Date.today()) + '/' + str(self.id or 0)
        return super().create(vals)

    @api.depends('yield_rate', 'standard_yield_rate')
    def _compute_yield_variance(self):
        for record in self:
            record.yield_variance = record.yield_rate - record.standard_yield_rate

    @api.depends('output_qty', 'energy_consumption_kwh')
    def _compute_efficiency(self):
        for record in self:
            if record.energy_consumption_kwh > 0:
                record.energy_efficiency = record.output_qty / record.energy_consumption_kwh
            else:
                record.energy_efficiency = 0.0