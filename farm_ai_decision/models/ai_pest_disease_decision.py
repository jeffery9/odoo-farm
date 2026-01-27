# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
import json
from datetime import datetime, timedelta
import random

_logger = logging.getLogger(__name__)

class AIPestDiseaseDecision(models.Model):
    """
    AI model for pest and disease treatment decision making
    Implements decision support for pest and disease management
    """
    _name = 'ai.pest.disease.decision'
    _description = 'AI Pest and Disease Decision Support'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'ai.base.mixin']

    pest_disease_detection_id = fields.Many2one('ai.pest.disease.detection', string='Original Detection')
    product_id = fields.Many2one('product.template', string='Affected Crop')
    land_location_id = fields.Many2one('farm.location', string='Location')
    detection_date = fields.Datetime('Detection Date', default=fields.Datetime.now)
    pest_disease_name = fields.Char('Pest/Disease Name')
    severity_level = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ], string='Severity Level', default='low')
    affected_area_percentage = fields.Float('Affected Area (%)')
    detection_method = fields.Selection([
        ('image', 'Image Recognition'),
        ('sensor', 'Sensor Data'),
        ('manual', 'Manual Observation'),
        ('combination', 'Combination'),
    ], string='Detection Method', default='image')
    prevention_advice = fields.Html('Prevention Advice')
    treatment_options = fields.Html('Treatment Options')
    risk_assessment = fields.Html('Risk Assessment')
    economic_impact = fields.Float('Economic Impact ($)', help="Estimated economic impact of the pest/disease")
    treatment_cost = fields.Float('Treatment Cost ($)', help="Estimated cost of recommended treatments")
    roi_impact = fields.Float('ROI Impact ($)', help="Estimated impact on return on investment", compute='_compute_roi_impact')

    @api.depends('economic_impact', 'treatment_cost')
    def _compute_roi_impact(self):
        for record in self:
            record.roi_impact = record.economic_impact - record.treatment_cost if record.economic_impact and record.treatment_cost else 0.0

    def analyze_pest_disease_decision(self):
        """Analyze pest/disease data and provide decision recommendations"""
        for record in self:
            # Simulate AI analysis
            severity = ['low', 'medium', 'high', 'critical'][min(3, int(record.affected_area_percentage / 25))]
            record.severity_level = severity

            # Generate treatment options based on pest/disease type
            if 'aphid' in (record.pest_disease_name or '').lower():
                record.treatment_options = """
                <ul>
                    <li>Natural predators: Ladybugs, lacewings</li>
                    <li>Insecticidal soap spray</li>
                    <li>Neem oil application</li>
                    <li>Crop rotation with non-host plants</li>
                </ul>
                """
                record.prevention_advice = "Monitor regularly for early detection, maintain field hygiene"

            elif 'blight' in (record.pest_disease_name or '').lower():
                record.treatment_options = """
                <ul>
                    <li>Copper-based fungicides</li>
                    <li>Improve air circulation</li>
                    <li>Remove infected plant material</li>
                    <li>Apply protective fungicides preventatively</li>
                </ul>
                """
                record.prevention_advice = "Avoid overhead irrigation, ensure proper spacing for air flow"

            else:
                record.treatment_options = "Consult agricultural specialist for specific treatment options"
                record.prevention_advice = "Implement integrated pest management strategies"

            # Calculate risk assessment
            if severity == 'critical':
                record.risk_assessment = "Immediate action required. Risk of crop loss is high."
                record.priority = 'critical'
            elif severity == 'high':
                record.risk_assessment = "Action needed within 48 hours to prevent spread."
                record.priority = 'high'
            elif severity == 'medium':
                record.risk_assessment = "Monitor closely and implement control measures soon."
                record.priority = 'medium'
            else:
                record.risk_assessment = "Low risk, continue monitoring."
                record.priority = 'low'

            # Calculate economic impact and treatment costs
            record.economic_impact = record.affected_area_percentage * 100  # Simplified calculation
            record.treatment_cost = len(record.treatment_options.split('<li>')) * 50  # Simplified cost estimate

            record.ai_confidence_score = min(95, max(65, 75 + random.uniform(-10, 10)))
            record.ai_status = 'completed'

    def _process_ai(self):
        """Process the AI analysis and return results"""
        self.analyze_pest_disease_decision()
        return {
            'description': f'Decision analysis for {self.pest_disease_name}',
            'confidence': self.ai_confidence_score,
            'processing_time': 50.0,
            'model_used': 'Pest Disease Decision Model',
            'input_data': {
                'pest_disease_name': self.pest_disease_name,
                'severity': self.severity_level,
                'affected_area': self.affected_area_percentage,
            },
            'output_data': {
                'treatment_options': self.treatment_options,
                'prevention_advice': self.prevention_advice,
                'risk_assessment': self.risk_assessment,
                'economic_impact': self.economic_impact,
                'treatment_cost': self.treatment_cost,
            }
        }