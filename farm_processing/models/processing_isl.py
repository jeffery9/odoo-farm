# -*- coding: utf-8 -*-
from odoo import models, fields, api

class FarmProcessingBom(models.Model):
    """ Food Processing Recipe [US-037-23] """
    _name = 'agri.isl.processing.bom'
    _description = 'Food Processing BOM (ISL Layer)'
    _inherits = {'mrp.bom': 'bom_id'}
    
    bom_id = fields.Many2one('mrp.bom', required=True, ondelete='cascade')
    target_moisture_content = fields.Float("Target Moisture (%)")
    target_temperature = fields.Float("Storage Temp (℃)")
    allergen_ids = fields.Many2many('farm.allergen', string="Allergens")
    expected_yield_rate = fields.Float("Expected Yield Rate", default=100.0)
    industry_type = fields.Selection([
        ('standard', 'Standard'),
        ('food_processing', 'Food Processing'),
        ('pharmaceutical', 'Pharmaceutical'),
        ('chemical', 'Chemical')
    ], string="Industry Standard", default='food_processing')


class FarmProcessingProduction(models.Model):
    """
    Food Processing Production Order that extends ISL architecture with farm-specific features
    """
    _name = 'agri.isl.processing.production'
    _description = 'Farm Food Processing Order (ISL Layer)'
    _inherit = ['agri.isl.mrp.production']

    # Energy Tracking (Processing Specific)
    energy_reading_start = fields.Float(string='Energy Reading Start', copy=False)
    energy_reading_end = fields.Float(string='Energy Reading End', copy=False)
    energy_cost_total = fields.Float(string='Total Energy Cost', compute='_compute_energy_cost_isl')
    water_consumption = fields.Float("Water Consumption")
    electricity_consumption = fields.Float("Electricity Consumption")
    total_energy_cost = fields.Float("Total Energy Cost (Measure)")

    # US-095-02: Artisan Monitoring
    current_moisture_content = fields.Float("Current Moisture (%)", group_operator="avg")
    current_weight_loss_ratio = fields.Float("Current Weight Loss (%)")
    is_ready_for_harvest = fields.Boolean("Ready for Collection", compute='_compute_artisan_readiness', store=True, precompute=True)
    
    processing_bom_id = fields.Many2one('agri.isl.processing.bom', string='Processing Recipe', compute='_compute_processing_bom', store=True, precompute=True)

    @api.depends('bom_id')
    def _compute_processing_bom(self):
        for rec in self:
            if rec.bom_id:
                # Find the corresponding farm.processing.bom for this farm.mrp.bom
                farm_bom = self.env['agri.isl.processing.bom'].search([('bom_id', '=', rec.bom_id.id)], limit=1)
                rec.processing_bom_id = farm_bom
            else:
                rec.processing_bom_id = False

    @api.depends('energy_reading_start', 'energy_reading_end')
    def _compute_energy_cost_isl(self):
        for rec in self:
            rec.energy_cost_total = (rec.energy_reading_end - rec.energy_reading_start) * 1.5 # Fixed price for ISL

    @api.depends('current_moisture_content', 'processing_bom_id.target_moisture_content')
    def _compute_artisan_readiness(self):
        """US-095-02: Automated logic to determine if artisan drying is complete"""
        for rec in self:
            if rec.processing_bom_id and rec.current_moisture_content <= rec.processing_bom_id.target_moisture_content:
                rec.is_ready_for_harvest = True
            else:
                rec.is_ready_for_harvest = False
