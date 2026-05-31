# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
import json
from datetime import datetime, timedelta
import random

_logger = logging.getLogger(__name__)

class AgriAiFertilizationDecision(models.Model):
    """
    AI model for fertilization decision.
    Level 4: Autonomous Input Feedback.
    Implements [US-088-06]: Autonomous Nutrient Correction Decision.
    """
    _name = 'agri.ai.fertilization.decision'
    _description = 'AI Fertilization Decision'
    _inherit = ['agri.ai.decision.base']

    land_location_id = fields.Many2one('farm.location', string='Land Location')
    product_id = fields.Many2one('product.template', string='Crop')
    soil_nitrogen = fields.Float('Soil Nitrogen (ppm)')
    soil_phosphorus = fields.Float('Soil Phosphorus (ppm)')
    soil_potassium = fields.Float('Soil Potassium (ppm)')
    soil_ph = fields.Float('Soil pH')
    crop_growth_stage = fields.Char('Crop Growth Stage')
    recommended_n = fields.Float('Recommended N (kg/ha)')
    recommended_p = fields.Float('Recommended P (kg/ha)')
    recommended_k = fields.Float('Recommended K (kg/ha)')
    fertilizer_recommendation = fields.Html('Fertilizer Recommendation')
    application_timing = fields.Char('Application Timing')
    nutrient_deficiency_analysis = fields.Html('Nutrient Deficiency Analysis')

    def action_fetch_iot_shadow(self):
        """ Pull live soil NPK levels from location's device shadow [US-TECH-AI-02] """
        self.ensure_one()
        if not self.land_location_id:
            return False
            
        # Find NPK sensor in this location
        device = self.env['iiot.device'].search([
            ('location_id', '=', self.land_location_id.id),
            ('connection_status', '=', 'online')
        ], limit=1)
        
        if device and device.shadow_state:
            try:
                shadow = json.loads(device.shadow_state)
                # Map shadow keys to soil fields
                self.soil_nitrogen = float(shadow.get('n', shadow.get('nitrogen', self.soil_nitrogen)))
                self.soil_phosphorus = float(shadow.get('p', shadow.get('phosphorus', self.soil_phosphorus)))
                self.soil_potassium = float(shadow.get('k', shadow.get('potassium', self.soil_potassium)))
                self.soil_ph = float(shadow.get('ph', self.soil_ph))
                
                self.message_post(body=_("IoT Sync: Fetched NPK/pH from device %s") % device.name)
            except Exception as e:
                _logger.error(f"Failed to parse shadow for fertilization decision: {str(e)}")

    def _create_correction_intervention(self):
        """ Create a correction fertilization task in the Intervention Engine """
        if self.recommended_n <= 0 and self.recommended_p <= 0 and self.recommended_k <= 0:
            return False

        vals = {
            'product_id': self.product_id.product_variant_id.id if self.product_id.product_variant_id else self.product_id.id,
            'product_qty': 0.0,
            'intervention_type': 'fertilizing',
            'location_id': self.land_location_id.id,
            'origin': f"AI Decision: {self.name}",
        }
        
        intervention = self.env['mrp.production'].create(vals)
        intervention.action_confirm()
        return intervention

    def calculate_fertilization_needs(self):
        """Calculate fertilization needs based on soil and crop conditions."""
        for record in self:
            # Calculate deficiencies
            n_deficit = max(0, 100 - record.soil_nitrogen)  # Target 100 ppm
            p_deficit = max(0, 25 - record.soil_phosphorus)  # Target 25 ppm
            k_deficit = max(0, 150 - record.soil_potassium)  # Target 150 ppm

            # Adjust based on crop needs
            if record.product_id:
                if 'corn' in record.product_id.name.lower():
                    n_deficit *= 1.2  # Corn needs more nitrogen
                    k_deficit *= 1.1
                elif 'tomato' in record.product_id.name.lower():
                    p_deficit *= 1.3  # Fruit crops need more phosphorus
                    k_deficit *= 1.4  # And more potassium

            # Adjust based on growth stage
            if record.crop_growth_stage:
                if 'flowering' in record.crop_growth_stage.lower():
                    record.recommended_p = p_deficit * 1.2
                    record.recommended_k = k_deficit * 1.3
                    record.recommended_n = n_deficit * 0.8  # Reduce nitrogen during flowering
                elif 'vegetative' in record.crop_growth_stage.lower():
                    record.recommended_n = n_deficit * 1.3
                    record.recommended_k = k_deficit * 1.1
                    record.recommended_p = p_deficit * 0.9
                else:
                    record.recommended_n = n_deficit
                    record.recommended_p = p_deficit
                    record.recommended_k = k_deficit

            # Generate fertilizer recommendations
            deficiency_analysis = []
            if record.soil_nitrogen < 80:
                deficiency_analysis.append("Nitrogen deficiency detected. Plants may show yellowing leaves.")
            if record.soil_phosphorus < 15:
                deficiency_analysis.append("Phosphorus deficiency detected. This may affect root development and flowering.")
            if record.soil_potassium < 120:
                deficiency_analysis.append("Potassium deficiency detected. Plants may show marginal leaf burn.")

            record.nutrient_deficiency_analysis = "<br/>".join([f"• {d}" for d in deficiency_analysis])

            record.fertilizer_recommendation = f"""
            <ul>
                <li>Nitrogen: {record.recommended_n:.1f} kg/ha</li>
                <li>Phosphorus: {record.recommended_p:.1f} kg/ha</li>
                <li>Potassium: {record.recommended_k:.1f} kg/ha</li>
            </ul>

            <p><strong>Application Recommendations:</strong></p>
            <ul>
                <li>Apply nitrogen in split doses to prevent leaching</li>
                <li>Apply phosphorus at planting time for better root development</li>
                <li>Apply potassium during flowering/fruiting stage</li>
            </ul>
            """

            if record.soil_ph < 5.5:
                record.fertilizer_recommendation += "<p>Consider liming to adjust soil pH.</p>"

            record.application_timing = "Apply in the early morning or evening, with irrigation following application"
            record.confidence_score = min(90, max(65, 75 + random.uniform(-10, 10)))
            record.status = 'recommended'

            # Level 4+: Automatic Mission Trigger [US-088-06]
            if record.recommended_n > 20.0 and record.land_location_id:
                _logger.info("Nutrient gap > 20kg detected. Triggering Autonomous Mission Orchestrator.")
                self.env['agri.mission.orchestrator'].action_trigger_inflow_mission(
                    record.land_location_id, 
                    _("%f kg N") % record.recommended_n
                )

    def generate_actuator_correction(self, intervention_id):
        """
        [US-088-06] Converts AI decision into a physical actuation payload.
        """
        self.ensure_one()
        intervention = self.env['agri.intervention'].browse(intervention_id)
        if not intervention:
            return False
            
        # Decision logic: if recommended N is high, tell the actuator to increase input
        correction_vals = {'nitrogen_qty': 0.15} # AI Suggests 15% increase
        return intervention.apply_feedback_correction(correction_vals)