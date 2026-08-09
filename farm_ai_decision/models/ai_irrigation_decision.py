# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
import json
from datetime import datetime, timedelta
import random

_logger = logging.getLogger(__name__)

class AgriAiIrrigationDecision(models.Model):
    """
    AI model for irrigation decision
    Implements US-088-07: Precise irrigation decision
    """
    _name = 'agri.ai.irrigation.decision'
    _description = 'AI Irrigation Decision'
    _inherit = ['agri.ai.decision.base']

    land_location_id = fields.Many2one('farm.location', string='Land Location')
    product_id = fields.Many2one('product.template', string='Crop')
    current_soil_moisture = fields.Float('Current Soil Moisture (%)')
    weather_forecast = fields.Text('Weather Forecast Data')
    irrigation_system = fields.Char('Irrigation System Type')
    irrigation_method = fields.Selection([
        ('drip', 'Drip Irrigation'),
        ('sprinkler', 'Sprinkler'),
        ('flood', 'Flood'),
        ('furrow', 'Furrow'),
    ], string='Irrigation Method')
    recommended_water_amount = fields.Float('Recommended Water Amount (mm)')
    recommended_irrigation_time = fields.Datetime('Recommended Time')
    evapotranspiration_rate = fields.Float('Evapotranspiration Rate (mm/day)')
    irrigation_efficiency = fields.Float('Irrigation Efficiency (%)')
    irrigation_advice = fields.Html('Irrigation Advice')
    soil_analysis = fields.Text('Soil Analysis')

    def action_fetch_iot_shadow(self):
        """ Pull live soil moisture from location's device shadow [US-TECH-AI-02] """
        self.ensure_one()
        if not self.land_location_id:
            return False
            
        # Find soil moisture sensor in this location
        device = self.env['iiot.device'].search([
            ('location_id', '=', self.land_location_id.id),
            ('connection_status', '=', 'online')
        ], limit=1)
        
        if device and device.shadow_state:
            try:
                shadow = json.loads(device.shadow_state)
                # Look for typical soil moisture keys
                moisture = shadow.get('moisture') or shadow.get('soil_moisture')
                if moisture is not None:
                    self.current_soil_moisture = float(moisture)
                    self.message_post(body=_("IoT Sync: Fetched soil moisture %s%% from device %s") % (moisture, device.name))
            except Exception as e:
                _logger.error(f"Failed to parse shadow for irrigation decision: {str(e)}")

    def _create_correction_intervention(self):
        """ Create a correction irrigation task in the Intervention Engine """
        if self.recommended_water_amount <= 0:
            return False

        # Use ISA-88/MRP implementation of the engine
        vals = {
            'product_id': self.product_id.product_variant_id.id if self.product_id.product_variant_id else self.product_id.id,
            'product_qty': 1.0, # Service/Intervention has no product output usually
            'intervention_type': 'irrigation',
            'location_id': self.land_location_id.id,
            'origin': f"AI Decision: {self.name}",
        }
        
        # Create and confirm immediately (which triggers engine plugins)
        intervention = self.env['mrp.production'].create(vals)
        intervention.action_confirm()
        return intervention

    def calculate_irrigation_needs(self):
        """Calculate irrigation needs based on multiple factors"""
        for record in self:
            # Simulate calculation using Penman-Monteith method concepts
            if record.current_soil_moisture < 30:  # Very dry
                water_needed = 25.0
                priority = 'high'
            elif record.current_soil_moisture < 45:  # Dry
                water_needed = 15.0
                priority = 'medium'
            else:  # Adequate
                water_needed = 5.0
                priority = 'low'

            # Adjust based on crop and weather
            if record.product_id:
                if 'corn' in record.product_id.name.lower():
                    water_needed += 5.0  # Corn needs more water
                elif 'wheat' in record.product_id.name.lower():
                    water_needed += 3.0

            # Adjust based on weather forecast
            if record.weather_forecast:
                # Simulate parsing weather forecast
                if 'rain' in record.weather_forecast.lower():
                    water_needed *= 0.5  # Less water needed if rain expected

            record.recommended_water_amount = water_needed
            record.irrigation_advice = f"""
            <p>Recommended irrigation: {water_needed}mm of water.</p>
            <p>Best time to irrigate: Early morning or late evening to minimize evaporation.</p>
            """

            if record.irrigation_system == 'drip':
                record.irrigation_advice += "<p>Drip irrigation recommended for efficient water use.</p>"

            record.evapotranspiration_rate = random.uniform(3.0, 8.0)
            record.irrigation_efficiency = random.uniform(70.0, 95.0)
            record.confidence_score = min(90, max(70, 80 + random.uniform(-5, 5)))
            record.priority = priority
            record.status = 'recommended'
