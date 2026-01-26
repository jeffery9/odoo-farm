# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
import json
from datetime import datetime, timedelta
import random

_logger = logging.getLogger(__name__)

class AIPestDiseaseDetection(models.Model):
    """
    AI model for pest and disease detection
    Implements US-58-05: Pest image recognition & prevention advice
    """
    _name = 'ai.pest.disease.detection'
    _description = 'AI Pest and Disease Detection'
    _inherit = ['ai.decision.base']

    product_id = fields.Many2one('product.template', string='Affected Crop')
    land_location_id = fields.Many2one('stock.location', string='Location')
    detection_date = fields.Datetime('Detection Date', default=fields.Datetime.now)
    pest_disease_name = fields.Char('Pest/Disease Name')
    severity_level = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ], string='Severity Level', default='low')
    affected_area_percentage = fields.Float('Affected Area (%)')
    image_attachment = fields.Binary('Image Attachment')
    image_name = fields.Char('Image Name')
    detection_method = fields.Selection([
        ('image', 'Image Recognition'),
        ('sensor', 'Sensor Data'),
        ('manual', 'Manual Observation'),
        ('combination', 'Combination'),
    ], string='Detection Method', default='image')
    prevention_advice = fields.Html('Prevention Advice')
    treatment_options = fields.Html('Treatment Options')
    risk_assessment = fields.Html('Risk Assessment')

    def analyze_pest_disease(self):
        """Analyze pest/disease data and provide recommendations"""
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

            record.confidence_score = min(95, max(65, 75 + random.uniform(-10, 10)))
            record.status = 'recommended'