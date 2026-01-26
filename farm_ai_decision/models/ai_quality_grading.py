# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
import json
from datetime import datetime, timedelta
import random

_logger = logging.getLogger(__name__)

class AIQualityGrading(models.Model):
    """
    AI model for quality grading
    Implements US-58-12: Intelligent quality grading & sorting
    """
    _name = 'ai.quality.grading'
    _description = 'AI Quality Grading'
    _inherit = ['ai.decision.base']

    product_id = fields.Many2one('product.template', string='Product')
    batch_lot_id = fields.Many2one('stock.lot', string='Batch/Lot')
    sample_size = fields.Integer('Sample Size')
    quality_attributes = fields.Text('Quality Attributes', help="JSON data of measured attributes")
    predicted_grade = fields.Selection([
        ('premium', 'Premium'),
        ('grade_a', 'Grade A'),
        ('grade_b', 'Grade B'),
        ('grade_c', 'Grade C'),
        ('substandard', 'Substandard'),
    ], string='Predicted Grade')
    quality_score = fields.Float('Quality Score (0-100)')
    grading_criteria = fields.Html('Grading Criteria Applied')
    sorting_recommendation = fields.Html('Sorting Recommendation')
    market_suggestion = fields.Html('Market Suggestion')

    def perform_quality_grading(self):
        """Perform AI-based quality grading"""
        for record in self:
            if record.product_id and record.sample_size > 0:
                # Simulate quality attribute analysis
                attributes = {
                    'size': random.uniform(50, 100),  # Size in mm
                    'color_score': random.uniform(70, 100),  # Color quality (0-100)
                    'weight': random.uniform(80, 150),  # Weight in grams
                    'brix_level': random.uniform(8, 15),  # Sugar content
                    'defects_percentage': random.uniform(0, 15),  # Defects
                    'firmness': random.uniform(70, 95),  # Firmness score (0-100)
                }

                record.quality_attributes = json.dumps(attributes)

                # Calculate quality score based on attributes
                score = (
                    (attributes['size'] / 100 * 15) +  # Size contributes 15 points max
                    (attributes['color_score'] / 100 * 20) +  # Color contributes 20 points max
                    (attributes['weight'] / 150 * 15) +  # Weight contributes 15 points max
                    (attributes['brix_level'] / 15 * 15) +  # Brix contributes 15 points max
                    ((15 - attributes['defects_percentage']) / 15 * 20) +  # Defects contribute 20 points max (inversely)
                    (attributes['firmness'] / 100 * 15)  # Firmness contributes 15 points max
                )

                record.quality_score = min(100, max(0, score))

                # Determine grade based on score
                if record.quality_score >= 90:
                    record.predicted_grade = 'premium'
                elif record.quality_score >= 80:
                    record.predicted_grade = 'grade_a'
                elif record.quality_score >= 70:
                    record.predicted_grade = 'grade_b'
                elif record.quality_score >= 60:
                    record.predicted_grade = 'grade_c'
                else:
                    record.predicted_grade = 'substandard'

                # Generate grading criteria
                record.grading_criteria = """
                <ul>
                    <li><strong>Size:</strong> {}mm - Weight: {}g</li>
                    <li><strong>Color Quality:</strong> {}%</li>
                    <li><strong>Sugar Content:</strong> {}°Brix</li>
                    <li><strong>Defects:</strong> {}%</li>
                    <li><strong>Firmness:</strong> {}%</li>
                </ul>
                """.format(
                    round(attributes['size'], 1),
                    round(attributes['weight'], 1),
                    round(attributes['color_score'], 1),
                    round(attributes['brix_level'], 1),
                    round(attributes['defects_percentage'], 1),
                    round(attributes['firmness'], 1)
                )

                # Generate sorting recommendations
                if record.predicted_grade in ['premium', 'grade_a']:
                    record.sorting_recommendation = """
                    <p><strong>Sort as high-value product:</strong></p>
                    <ul>
                        <li>Pack in premium packaging</li>
                        <li>Market as fresh consumption grade</li>
                        <li>Target premium market segments</li>
                    </ul>
                    """
                    record.market_suggestion = "Recommended for premium fresh market or export"
                elif record.predicted_grade in ['grade_b', 'grade_c']:
                    record.sorting_recommendation = """
                    <p><strong>Sort as commercial grade:</strong></p>
                    <ul>
                        <li>Pack in commercial packaging</li>
                        <li>Market as standard grocery grade</li>
                        <li>Consider processing if grades are lower</li>
                    </ul>
                    """
                    record.market_suggestion = "Recommended for standard retail market"
                else:
                    record.sorting_recommendation = """
                    <p><strong>Consider processing or discard:</strong></p>
                    <ul>
                        <li>Assess if processing is viable</li>
                        <li>Check for potential quality improvements</li>
                        <li>Consider as feed or compost material</li>
                    </ul>
                    """
                    record.market_suggestion = "Recommended for processing or industrial use only"

                record.confidence_score = min(95, max(75, 85 + random.uniform(-5, 5)))
                record.status = 'recommended'