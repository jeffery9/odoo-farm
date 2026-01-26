# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
import json
from datetime import datetime, timedelta
import random

_logger = logging.getLogger(__name__)

class AIFertilizationDecision(models.Model):
    """
    AI model for fertilization decision
    Implements US-58-06: Intelligent fertilization decision
    """
    _name = 'ai.fertilization.decision'
    _description = 'AI Fertilization Decision'
    _inherit = ['ai.decision.base']

    land_location_id = fields.Many2one('stock.location', string='Land Location')
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

    def calculate_fertilization_needs(self):
        """Calculate fertilization needs based on soil and crop conditions"""
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