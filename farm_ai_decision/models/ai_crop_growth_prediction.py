# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
import json
from datetime import datetime, timedelta
import random

_logger = logging.getLogger(__name__)

class AgriAiCropGrowthPrediction(models.Model):
    """
    AI model for crop growth prediction
    Implements US-58-04: Intelligent planting scheme recommendation
    """
    _name = 'agri.ai.crop.growth.prediction'
    _description = 'AI Crop Growth Prediction'
    _inherit = ['agri.ai.decision.base']

    product_id = fields.Many2one('product.template', string='Crop Type')
    land_location_id = fields.Many2one('farm.location', string='Land Location')
    planting_date = fields.Date('Planting Date')
    expected_harvest_date = fields.Date('Expected Harvest Date')
    current_growth_stage = fields.Char('Current Growth Stage')
    predicted_yield = fields.Float('Predicted Yield')
    growth_deviation = fields.Float('Growth Deviation', help="Deviation from normal growth curve")
    environmental_factors = fields.Text('Environmental Factors Analysis')
    growth_curve_data = fields.Text('Growth Curve Data', help="JSON data for growth curve analysis")
    growth_recommendation = fields.Html('Growth Optimization Recommendation')

    def calculate_growth_prediction(self):
        """Calculate crop growth prediction based on various factors"""
        # Check if LLM integration is available
        llm_service = self.env['agri.ai.llm.service'].search([('config_id.is_active', '=', True),
                                                              ('config_id.is_default', '=', True)], limit=1)

        for record in self:
            if llm_service:
                # Use LLM for enhanced growth prediction
                self._calculate_growth_prediction_with_llm(llm_service, record)
            else:
                # Fallback to traditional methods if no LLM configured
                self._calculate_growth_prediction_traditional(record)

    def _calculate_growth_prediction_with_llm(self, llm_service, record):
        """Calculate growth prediction using LLM for enhanced analysis"""
        # Prepare context data
        context_data = {
            'crop_type': record.product_id.name if record.product_id else 'unknown crop',
            'location': record.land_location_id.name if record.land_location_id else 'unknown location',
            'planting_date': record.planting_date,
            'industry': record.base_id.industry_id.name if record.base_id.industry_id else 'General Agriculture'
        }

        # Create prompt for LLM
        prompt = (
            f"Provide a comprehensive crop growth prediction for {context_data['crop_type']} "
            f"planted at {context_data['location']}. Consider:\n"
            f"1. Expected growth stages and timeline\n"
            f"2. Optimal harvest date estimation\n"
            f"3. Predicted yield with environmental factors\n"
            f"4. Growth deviation from standard curves\n"
            f"5. Environmental factors affecting growth (soil, water, nutrients)\n"
            f"6. Recommendations for growth optimization\n"
            f"7. Potential challenges and mitigation strategies\n"
            f"8. Weather and seasonal impact considerations\n\n"
            f"Be specific about numbers and provide actionable recommendations."
        )

        # Call the LLM
        llm_result = llm_service.call_llm(prompt, context_data)

        if llm_result['success']:
            # Parse and apply the LLM response
            self._apply_llm_growth_prediction_result(record, llm_result['response'], llm_result)
        else:
            # Fallback to traditional method if LLM fails
            _logger.warning(f"LLM call failed for growth prediction: {llm_result['error']}. Falling back to traditional methods.")
            self._calculate_growth_prediction_traditional(record)

    def _apply_llm_growth_prediction_result(self, record, llm_response, llm_result):
        """Apply LLM response to the record fields"""
        import re
        from datetime import datetime, timedelta

        # Extract yield prediction (looking for numbers followed by units like tons, kg, lbs)
        yield_matches = re.findall(r'(\d+(?:\.\d+)?)\s*(?:tons|kg|lbs|bushels)', llm_response)
        if yield_matches:
            try:
                record.predicted_yield = float(yield_matches[0])
            except ValueError:
                pass

        # Extract harvest date (looking for date formats or time periods)
        harvest_matches = re.findall(r'(\d+)\s*(?:day|week|month)', llm_response)
        if harvest_matches and record.planting_date:
            try:
                days = int(harvest_matches[0])
                # Check if it's weeks or months
                unit_match = re.search(r'(\d+)\s*(week|month)', llm_response)
                if unit_match:
                    if 'week' in unit_match.group(2):
                        days = int(unit_match.group(1)) * 7
                    elif 'month' in unit_match.group(2):
                        days = int(unit_match.group(1)) * 30

                harvest_date = fields.Date.from_string(record.planting_date) + timedelta(days=days)
                record.expected_harvest_date = harvest_date
            except ValueError:
                # If we can't process the date, try parsing direct dates
                date_match = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})', llm_response)  # YYYY-MM-DD format
                if date_match:
                    try:
                        year, month, day = date_match.groups()
                        record.expected_harvest_date = f"{year}-{int(month):02d}-{int(day):02d}"
                    except ValueError:
                        pass

        # Extract growth stage information
        growth_stages = ['germination', 'seedling', 'vegetative', 'flowering', 'fruiting', 'maturation']
        for stage in growth_stages:
            if stage in llm_response.lower():
                record.current_growth_stage = stage.title()
                break

        # Use the full response as environmental factors analysis and growth recommendations
        record.environmental_factors = f"LLM Analysis: {llm_response}"
        record.growth_recommendation = llm_response

        # Set confidence to a high value for LLM results
        record.confidence_score = 0.85

        # Add LLM result to output data
        if record.base_id.output_data:
            output = json.loads(record.base_id.output_data)
        else:
            output = {}
        output['llm_analysis'] = llm_response
        output['model_used'] = llm_result.get('model_used', 'unknown')
        record.base_id.output_data = json.dumps(output)

        record.status = 'recommended'

    def _calculate_growth_prediction_traditional(self, record):
        """Calculate growth prediction using traditional methods (existing implementation)"""
        # This is a simplified implementation - in real systems this would use ML models
        # Simulate some basic AI calculations
        if record.product_id and record.land_location_id:
            # Calculate predicted harvest based on variety, location, and weather
            base_days = 90  # Default growth period
            if record.product_id.name:
                if 'tomato' in record.product_id.name.lower():
                    base_days = 70
                elif 'corn' in record.product_id.name.lower():
                    base_days = 120
                elif 'wheat' in record.product_id.name.lower():
                    base_days = 150

            # Calculate environmental factors
            env_factors = {
                'soil_ph': random.uniform(6.0, 7.5),
                'nitrogen_level': random.uniform(20, 50),
                'phosphorus_level': random.uniform(15, 30),
                'potassium_level': random.uniform(100, 200),
                'moisture_level': random.uniform(30, 60),
            }

            # Calculate deviation based on ideal conditions
            deviation = random.uniform(-0.1, 0.1)  # -10% to +10%

            # Calculate expected harvest date
            if record.planting_date:
                expected_harvest = fields.Date.from_string(record.planting_date) + timedelta(days=int(base_days * (1 + deviation)))
                record.expected_harvest_date = expected_harvest

            # Calculate predicted yield based on factors
            base_yield = 5.0  # Base yield in tons per hectare
            yield_factor = (env_factors['nitrogen_level'] / 100) * (env_factors['moisture_level'] / 50)
            record.predicted_yield = base_yield * yield_factor * (1 + deviation)

            # Calculate confidence based on data availability
            record.confidence_score = min(95, max(60, 70 + random.uniform(-10, 10)))

            # Store environmental factors
            record.environmental_factors = json.dumps(env_factors)

            # Generate growth recommendation
            recommendations = []
            if env_factors['soil_ph'] < 6.2:
                recommendations.append("Consider liming to increase soil pH")
            if env_factors['nitrogen_level'] < 30:
                recommendations.append("Apply nitrogen fertilizer to optimize growth")
            if env_factors['moisture_level'] < 40:
                recommendations.append("Irrigation recommended to maintain adequate soil moisture")

            record.growth_recommendation = "<br/>".join([f"• {rec}" for rec in recommendations])

            record.status = 'recommended'
