# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from datetime import timedelta
import json
import logging

_logger = logging.getLogger(__name__)

class AgriBiologicalTwin(models.Model):
    """
    Biological Digital Twin Engine. [US-014-2026]
    Domain Role: Universal digital reflection of a living asset's physical state.
    Refactored from farm.biological.twin with 100% logic and comment retention.
    """
    _name = 'agri.biological.twin'
    _description = 'Biological Digital Twin Engine'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'agri.biological.asset.mixin']

    name = fields.Char("Twin Ref", required=True, copy=False, readonly=True, default=lambda self: _('New'))
    product_id = fields.Many2one('product.template', string="Variety Standard", required=True)
    location_id = fields.Many2one('farm.location', string="Monitoring Parcel", required=True)
    
    # Timeline
    start_date = fields.Date("Sowing/Start Date", default=fields.Date.today)
    expected_harvest_date = fields.Date("Target Harvest Date", compute='_compute_harvest_prediction', store=True, precompute=True)
    
    # L3: Thermal Intelligence
    accumulated_gdd = fields.Float("Accumulated GDD (℃)", help="Growing Degree Days accumulation")
    base_temp = fields.Float("Base Temperature (℃)", default=10.0, help="Min temp for growth")
    target_gdd_harvest = fields.Float("Target GDD for Harvest")
    
    # Current Status
    current_stage_id = fields.Many2one('agri.industry.physio.stage', string="Current Physio-Stage")
    health_score = fields.Float("Growth Health Score (0-100)", compute='_compute_health_score', store=True, precompute=True)
    
    # Prediction
    predicted_yield = fields.Float("Predicted Yield (kg)", digits=(12, 2))
    confidence_level = fields.Selection([
        ('low', 'Low (Initial)'),
        ('med', 'Medium (Mid-season)'),
        ('high', 'High (Near-harvest)')
    ], string="Confidence Level", default='low')

    # L4: ESG Integration (Carbon Footprint)
    accumulated_carbon = fields.Float("Accumulated Carbon (kg CO2e)", compute='_compute_carbon_footprint')
    carbon_intensity = fields.Float("Carbon Intensity (kg CO2e/kg yield)", compute='_compute_carbon_footprint')

    # --- 100% Original Logic Retention (RESTORED) ---

    def _compute_carbon_footprint(self):
        """
        L4 Logic: Aggregates real-time carbon data from the ledger for this specific location/cycle.
        Refactored to target the agri.carbon.ledger namespace.
        """
        for rec in self:
            ledger_entries = self.env['agri.carbon.ledger'].sudo().search([
                ('location_id', '=', rec.location_id.id),
                ('date', '>=', rec.start_date)
            ])
            total_co2 = sum(ledger_entries.mapped('total_co2e'))
            rec.accumulated_carbon = total_co2
            rec.carbon_intensity = total_co2 / rec.predicted_yield if rec.predicted_yield > 0 else 0.0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('agri.biological.twin') or _('TWIN')
        return super(AgriBiologicalTwin, self).create(vals_list)

    @api.depends('accumulated_gdd', 'target_gdd_harvest', 'start_date')
    def _compute_harvest_prediction(self):
        """
        L3 Intelligence: Predict harvest date based on thermal accumulation rate.
        """
        for rec in self:
            if rec.accumulated_gdd > 0 and rec.target_gdd_harvest > 0:
                days_elapsed = (fields.Date.today() - rec.start_date).days or 1
                daily_gdd_avg = rec.accumulated_gdd / days_elapsed
                remaining_gdd = rec.target_gdd_harvest - rec.accumulated_gdd
                if daily_gdd_avg > 0:
                    days_to_harvest = remaining_gdd / daily_gdd_avg
                    rec.expected_harvest_date = fields.Date.today() + timedelta(days=int(days_to_harvest))

    @api.depends('accumulated_gdd', 'location_id.grid_cell_ids.ndvi_index')
    def _compute_health_score(self):
        """
        Compares spatial NDVI vs. expected growth stage.
        """
        for rec in self:
            # Average NDVI from all grid cells in the location
            cells = rec.location_id.grid_cell_ids
            avg_ndvi = sum(cells.mapped('ndvi_index')) / len(cells) if cells else 0.5
            
            # Simple health formula: NDVI + GDD consistency
            # If GDD is progressing but NDVI is low, health score drops
            rec.health_score = avg_ndvi * 100.0  # Basic for prototype

    def action_update_gdd(self):
        """
        Mock: Fetch GDD from weather service integration.
        """
        self.ensure_one()
        # In real production, this would sum (Daily Max Temp + Daily Min Temp) / 2 - Base Temp
        self.accumulated_gdd += 15.5 # Simulated daily gain
        return True

    def action_run_yield_prediction_ai(self):
        """
        L3 AI Logic: Yield Forecasting.
        Uses NDVI distribution, GDD, and historical variety performance.
        """
        for rec in self:
            # Prediction Logic: Area * Density * Health * Environmental Correction
            area = rec.location_id.land_area or 1000.0
            rec.predicted_yield = area * (rec.health_score / 100.0) * 0.8 # Simulated kg/sqm
            rec.confidence_level = 'med'
            
            # If health is low, auto-generate an 'Anomaly Investigation' task
            if rec.health_score < 60:
                self.env['project.task'].create({
                    'name': _("Growth Anomaly Detected: %s") % rec.location_id.name,
                    'project_id': self.env.ref('farm_operation.project_farm_operations').id,
                    'description': _("Biological twin detected low health score. Visual inspection required.")
                })

    def action_optimize_environment(self):
        """
        L5 Autonomous Logic Hook:
        This method is intended to be overridden by specific environment control modules
        (e.g., farm_greenhouse, farm_irrigation) to implement automated adjustments.
        
        Base implementation does nothing.
        """
        return True
    # --- END OF ORIGINAL LOGIC AND COMMENTS ---
