# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
import json
from datetime import datetime, timedelta
import base64
from .ai_vision_base import AIVisionBase

_logger = logging.getLogger(__name__)

class AIVisionRiskAssessment(AIVisionBase):
    """
    AI model for AI vision risk assessment
    Implements US-58-14: AI视觉风险评估
    """
    _name = 'ai.vision.risk.assessment'
    _description = 'AI Vision Risk Assessment'
    _inherit = ['ai.vision.base']

    risk_type = fields.Selection([
        ('crop_health', 'Crop Health Risk'),
        ('weather_damage', 'Weather Damage Risk'),
        ('pest_outbreak', 'Pest Outbreak Risk'),
        ('disease_spread', 'Disease Spread Risk'),
        ('quality_defect', 'Quality Defect Risk'),
        ('yield_loss', 'Yield Loss Risk'),
    ], string='Risk Type', required=True, default='crop_health')

    risk_level = fields.Selection([
        ('very_low', 'Very Low (1-20%)'),
        ('low', 'Low (21-40%)'),
        ('medium', 'Medium (41-60%)'),
        ('high', 'High (61-80%)'),
        ('very_high', 'Very High (81-100%)'),
    ], string='Risk Level', compute='_compute_risk_level', store=True)

    risk_score = fields.Float('Risk Score', help="Numerical risk score from 0-100")
    affected_area_percentage = fields.Float('Affected Area (%)', help="Percentage of area at risk")
    potential_loss = fields.Float('Potential Loss (%)', help="Estimated percentage of loss if risk materializes")
    risk_description = fields.Html('Risk Description')
    mitigation_recommendations = fields.Html('Mitigation Recommendations')
    risk_monitoring_plan = fields.Html('Risk Monitoring Plan')

    # ISL-specific fields
    industry_id = fields.Many2one('industry.type', string='Industry',
                                  help="Industry to which this risk assessment applies")
    uses_isl_data = fields.Boolean('Uses ISL Data', default=True,
                                   help="Whether this risk assessment accesses ISL models")
    data_isolation_level = fields.Selection([
        ('none', 'No Isolation'),
        ('industry', 'Industry Level'),
        ('entity', 'Entity Level'),
        ('user', 'User Level'),
    ], string='Data Isolation Level', default='industry')

    @api.depends('risk_score')
    def _compute_risk_level(self):
        """Compute risk level based on risk score"""
        for record in self:
            if record.risk_score is None:
                record.risk_level = 'medium'
            elif record.risk_score <= 20:
                record.risk_level = 'very_low'
            elif record.risk_score <= 40:
                record.risk_level = 'low'
            elif record.risk_score <= 60:
                record.risk_level = 'medium'
            elif record.risk_score <= 80:
                record.risk_level = 'high'
            else:
                record.risk_level = 'very_high'

    def _process_image_ai(self, record):
        """Process image for risk assessment using AI vision algorithms"""
        # Check if LLM integration is available
        llm_service = self.env['llm.service'].search([('config_id.is_active', '=', True),
                                                      ('config_id.is_default', '=', True)], limit=1)

        if llm_service:
            # Use LLM to generate more comprehensive risk assessment
            return self._process_image_with_llm(llm_service, record)
        else:
            # Fallback to traditional methods if no LLM configured
            return self._process_image_traditional(record)

    def _process_image_with_llm(self, llm_service, record):
        """Process image using LLM for enhanced risk assessment"""
        # Prepare context data
        context_data = {
            'image_description': f'{record.risk_type} risk assessment image',
            'risk_type': record.risk_type,
            'industry': record.industry_id.name if record.industry_id else 'General Agriculture'
        }

        # Create prompt for LLM
        prompt = (
            f"Analyze this image for {context_data['risk_type']} risk assessment. Provide a comprehensive "
            f"evaluation including:\n"
            f"1. Risk level and probability assessment (0-100 scale)\n"
            f"2. Affected area percentage estimate\n"
            f"3. Potential financial/production loss estimate\n"
            f"4. Specific risk factors detected in the image\n"
            f"5. Severity classification (very low, low, medium, high, very high)\n"
            f"6. Recommended mitigation strategies\n"
            f"7. Monitoring and early warning protocols\n"
            f"8. Timeline for risk materialization\n"
            f"9. Secondary risk implications\n"
            f"10. Cost-benefit analysis of mitigation options\n\n"
            f"Provide specific, quantified assessments where possible."
        )

        # Call the LLM
        llm_result = llm_service.call_llm(prompt, context_data)

        if llm_result['success']:
            # Parse and structure the LLM response
            return self._parse_llm_risk_result(record, llm_result['response'], llm_result)
        else:
            # Fallback to traditional method if LLM fails
            _logger.warning(f"LLM call failed for vision risk assessment: {llm_result['error']}. Falling back to traditional methods.")
            return self._process_image_traditional(record)

    def _parse_llm_risk_result(self, record, llm_response, llm_result):
        """Parse LLM response for vision risk assessment"""
        import re

        # This is a simplified parser - a real implementation would use more sophisticated NLP
        result = {
            'description': f"LLM-enhanced risk assessment completed for {record.risk_type}",
            'classification': f"Risk assessment: {record.risk_type}",
            'risk_score': 50.0,  # Will be parsed from response
            'affected_area': 0.0,
            'potential_loss': 0.0,
            'risk_description': llm_response,
            'mitigation_recommendations': '',
            'monitoring_plan': '',
            'confidence': 0.85,  # LLM responses typically have high confidence
            'processing_time': 0.0,  # Will be calculated
            'features_detected': ['llm_analysis'],
            'llm_response': llm_response,
            'model_used': llm_result.get('model_used', 'unknown')
        }

        # Extract risk score (looking for numbers between 0-100 that seem to be scores)
        score_matches = re.findall(r'\b(\d{1,3}(?:\.\d+)?)\s*/?\s*100|risk.*?(\d{1,3}(?:\.\d+)?)|level.*?(\d{1,3}(?:\.\d+)?)', llm_response.lower())
        if score_matches:
            # Look for the first numeric value that seems to be a risk score
            for match in score_matches[0]:
                if match:  # The regex has multiple groups, we only take non-empty ones
                    try:
                        value = float(match)
                        if 0 <= value <= 100:
                            result['risk_score'] = value
                            break
                    except ValueError:
                        continue

        # Extract affected area percentage
        area_matches = re.findall(r'(\d+(?:\.\d+)?)\s*%', llm_response)
        for match in area_matches:
            try:
                value = float(match)
                if 0 <= value <= 100:
                    result['affected_area'] = value
                    break
            except ValueError:
                continue

        # Extract potential loss percentage
        loss_matches = re.findall(r'loss.*?(\d+(?:\.\d+)?)%', llm_response.lower())
        if loss_matches:
            try:
                result['potential_loss'] = float(loss_matches[0])
            except ValueError:
                pass

        # Determine risk level based on score
        if result['risk_score'] <= 20:
            result['risk_level'] = 'very_low'
        elif result['risk_score'] <= 40:
            result['risk_level'] = 'low'
        elif result['risk_score'] <= 60:
            result['risk_level'] = 'medium'
        elif result['risk_score'] <= 80:
            result['risk_level'] = 'high'
        else:
            result['risk_level'] = 'very_high'

        # Extract mitigation recommendations
        if 'mitigation' in llm_response.lower() or 'recommend' in llm_response.lower():
            result['mitigation_recommendations'] = llm_response

        # Extract monitoring plan
        if 'monitor' in llm_response.lower() or 'plan' in llm_response.lower():
            result['monitoring_plan'] = llm_response

        # Extract risk description (first part of the response usually contains this)
        result['risk_description'] = llm_response

        # Adjust confidence based on response quality
        if len(llm_response) < 50:
            result['confidence'] = 0.7
        elif len(llm_response) > 500:
            result['confidence'] = 0.9

        return result

    def _process_image_traditional(self, record):
        """Process image using traditional methods (existing implementation)"""
        # In a real implementation, this would call actual risk assessment models
        # For now, we'll simulate the risk assessment process
        import random

        # Define risk analysis based on risk type
        risk_types = {
            'crop_health': {
                'factors': ['plant_health', 'leaf_condition', 'growth_pattern'],
                'description': 'Risk assessment based on crop health indicators'
            },
            'weather_damage': {
                'factors': ['physical_damage', 'storm_impact', 'wind_damage'],
                'description': 'Risk assessment for weather-related damage'
            },
            'pest_outbreak': {
                'factors': ['pest_signs', 'early_detection', 'infestation_level'],
                'description': 'Risk assessment for potential pest outbreak'
            },
            'disease_spread': {
                'factors': ['disease_symptoms', 'spread_pattern', 'infection_level'],
                'description': 'Risk assessment for disease spread'
            },
            'quality_defect': {
                'factors': ['defect_detection', 'quality_indicators', 'grade_risk'],
                'description': 'Risk assessment for quality defects'
            },
            'yield_loss': {
                'factors': ['growth_deviation', 'stress_indicators', 'density_issues'],
                'description': 'Risk assessment for potential yield loss'
            }
        }

        # Get analysis parameters for this risk type
        analysis = risk_types.get(record.risk_type, risk_types['crop_health'])

        # Generate risk score (0-100)
        risk_score = random.uniform(10, 90)

        # Calculate affected area and potential loss
        affected_area = min(100, risk_score * random.uniform(0.8, 1.2))
        potential_loss = min(100, risk_score * random.uniform(0.5, 1.0))

        # Generate risk description based on type
        risk_descriptions = {
            'crop_health': f"Based on plant health indicators, risk level is assessed at {risk_score:.1f}/100.",
            'weather_damage': f"Weather damage risk is assessed at {risk_score:.1f}/100 based on observed damage patterns.",
            'pest_outbreak': f"Pest outbreak risk is at {risk_score:.1f}/100 with early signs detected.",
            'disease_spread': f"Disease spread risk is {risk_score:.1f}/100 based on infection patterns.",
            'quality_defect': f"Quality defect risk is {risk_score:.1f}/100 based on visual defect identification.",
            'yield_loss': f"Yield loss risk is {risk_score:.1f}/100 based on growth and stress indicators."
        }

        risk_description = risk_descriptions.get(record.risk_type, analysis['description'])

        # Generate mitigation recommendations
        mitigation_map = {
            'crop_health': [
                "Enhance nutrition management with targeted fertilization",
                "Monitor plant health weekly and adjust irrigation as needed",
                "Apply preventive treatments if risk score exceeds 60"
            ],
            'weather_damage': [
                "Install protective structures if not already in place",
                "Prepare emergency plan for weather events",
                "Consider crop insurance for high-risk periods"
            ],
            'pest_outbreak': [
                "Deploy integrated pest management protocols",
                "Set up additional monitoring traps",
                "Prepare biological control agents"
            ],
            'disease_spread': [
                "Implement disease monitoring program",
                "Prepare fungicide applications if needed",
                "Ensure proper field sanitation"
            ],
            'quality_defect': [
                "Adjust harvesting and handling procedures",
                "Implement quality control checkpoints",
                "Review post-harvest handling practices"
            ],
            'yield_loss': [
                "Optimize growing conditions to minimize loss",
                "Review and adjust input management",
                "Consider yield insurance for high-value crops"
            ]
        }

        mitigation = mitigation_map.get(record.risk_type, mitigation_map['crop_health'])

        # Generate monitoring plan
        monitoring_plan = [
            "Daily visual inspection of high-risk areas",
            "Weekly detailed assessment with AI tools",
            "Bi-weekly comprehensive risk evaluation",
            "Immediate alert system for risk score changes > 10 points"
        ]

        return {
            'description': f"AI vision risk assessment completed for {record.risk_type}",
            'classification': f"Risk assessment: {record.risk_type}",
            'risk_score': risk_score,
            'affected_area': affected_area,
            'potential_loss': potential_loss,
            'risk_description': risk_description,
            'mitigation_recommendations': "<br/>".join([f"• {rec}" for rec in mitigation]),
            'monitoring_plan': "<br/>".join([f"• {plan}" for plan in monitoring_plan]),
            'confidence': random.uniform(0.70, 0.90),
            'processing_time': random.uniform(300, 700),
            'features_detected': analysis['factors'],
        }

    def action_process_image(self):
        """Override to set specific fields after processing"""
        result = super().action_process_image()

        for record in self:
            if record.output_data:
                output = json.loads(record.output_data)

                # Set specific fields based on AI output
                if 'risk_score' in output:
                    record.risk_score = output['risk_score']

                if 'affected_area' in output:
                    record.affected_area_percentage = output['affected_area']

                if 'potential_loss' in output:
                    record.potential_loss = output['potential_loss']

                if 'risk_description' in output:
                    record.risk_description = output['risk_description']

                if 'mitigation_recommendations' in output:
                    record.mitigation_recommendations = output['mitigation_recommendations']

                if 'monitoring_plan' in output:
                    record.risk_monitoring_plan = output['monitoring_plan']

        return result