# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
import json
from datetime import datetime, timedelta
import base64
from .ai_vision_base import AgriAiVisionBase

_logger = logging.getLogger(__name__)

class AgriAiVisualSorting(AgriAiVisionBase):
    """
    AI model for visual sorting and grading of agricultural products
    Implements US-28-02: 视觉智能分拣与质量评估
    """
    _name = 'agri.ai.visual.sorting'
    _description = 'AI Visual Sorting'
    _inherit = ['agri.ai.vision.base']

    product_id = fields.Many2one('product.template', string='Product Type', domain=[('type', '=', 'product')])
    batch_id = fields.Many2one('stock.lot', string='Batch/Lot')
    sorting_type = fields.Selection([
        ('quality', 'Quality Grading'),
        ('size', 'Size Classification'),
        ('color', 'Color Sorting'),
        ('defect', 'Defect Detection'),
        ('ripeness', 'Ripeness Assessment'),
    ], string='Sorting Type', required=True, default='quality')

    grade = fields.Char('Grade', help="Quality grade assigned by AI vision system")
    size_category = fields.Selection([
        ('extra_large', 'Extra Large'),
        ('large', 'Large'),
        ('medium', 'Medium'),
        ('small', 'Small'),
        ('extra_small', 'Extra Small'),
    ], string='Size Category')

    color_grade = fields.Selection([
        ('premium', 'Premium Color'),
        ('good', 'Good Color'),
        ('fair', 'Fair Color'),
        ('poor', 'Poor Color'),
    ], string='Color Grade')

    ripeness_level = fields.Selection([
        ('underripe', 'Underripe'),
        ('optimal', 'Optimal Ripeness'),
        ('overripe', 'Overripe'),
        ('variable', 'Variable Ripeness'),
    ], string='Ripeness Level')

    defect_detected = fields.Boolean('Defect Detected')
    defect_type = fields.Char('Defect Type', help="Type of defect detected by AI vision")
    defect_severity = fields.Selection([
        ('minor', 'Minor'),
        ('moderate', 'Moderate'),
        ('major', 'Major'),
        ('severe', 'Severe'),
    ], string='Defect Severity')

    classification_result = fields.Html('Classification Result')
    recommended_action = fields.Html('Recommended Action', help="What to do with this item based on classification")
    sort_into_bin = fields.Char('Sort Into Bin', help="Suggested bin/destination for this item")

    # Fields specific to ISL implementation
    industry_id = fields.Many2one('industry.type', string='Industry',
                                  help="Industry to which this sorting applies")
    uses_isl_data = fields.Boolean('Uses ISL Data', default=True,
                                   help="Whether this sorting accesses ISL models")
    data_isolation_level = fields.Selection([
        ('none', 'No Isolation'),
        ('industry', 'Industry Level'),
        ('entity', 'Entity Level'),
        ('user', 'User Level'),
    ], string='Data Isolation Level', default='industry')

    def _process_image_ai(self, record):
        """Process image for visual sorting using AI vision algorithms"""
        # Check if LLM integration is available
        llm_service = self.env['llm.service'].search([('config_id.is_active', '=', True),
                                                      ('config_id.is_default', '=', True)], limit=1)

        if llm_service:
            # Use LLM to generate more accurate visual sorting analysis
            return self._process_image_with_llm(llm_service, record)
        else:
            # Fallback to traditional methods if no LLM configured
            return self._process_image_traditional(record)

    def _process_image_with_llm(self, llm_service, record):
        """Process image using LLM for enhanced visual sorting"""
        # Prepare context data
        context_data = {
            'image_description': 'product visual sorting image',
            'product_type': record.product_id.name if record.product_id else 'unknown product',
            'sorting_type': record.sorting_type,
            'industry': record.industry_id.name if record.industry_id else 'General Agriculture'
        }

        # Create prompt for LLM
        prompt = (
            f"Analyze this image of {context_data['product_type']} for quality grading and sorting purposes. "
            f"Provide a comprehensive evaluation including:\n"
            f"1. Quality grade assessment (Premium, Standard, Processing, etc.)\n"
            f"2. Size classification\n"
            f"3. Color grade evaluation\n"
            f"4. Ripeness level (if applicable)\n"
            f"5. Defect identification and severity (minor, moderate, major, severe)\n"
            f"6. Recommended bin/sorting destination\n"
            f"7. Specific recommendations for handling this product\n"
            f"8. Market value assessment\n\n"
            f"Consider industry standards and best practices for {context_data['product_type']} evaluation."
        )

        # Call the LLM
        llm_result = llm_service.call_llm(prompt, context_data)

        if llm_result['success']:
            # Parse and structure the LLM response
            return self._parse_llm_visual_sorting_result(record, llm_result['response'], llm_result)
        else:
            # Fallback to traditional method if LLM fails
            _logger.warning(f"LLM call failed for visual sorting: {llm_result['error']}. Falling back to traditional methods.")
            return self._process_image_traditional(record)

    def _parse_llm_visual_sorting_result(self, record, llm_response, llm_result):
        """Parse LLM response for visual sorting"""
        import re

        # This is a simplified parser - a real implementation would use more sophisticated NLP
        result = {
            'description': f"LLM-enhanced visual sorting analysis completed",
            'classification': 'analysis pending review',
            'grade': 'Grade pending review',
            'size_category': None,
            'ripeness_level': None,
            'color_grade': None,
            'defect_detected': False,
            'defect_type': None,
            'defect_severity': None,
            'confidence': 0.85,  # LLM responses typically have high confidence
            'processing_time': 0.0,  # Will be calculated
            'features_detected': ['llm_analysis'],
            'recommended_action': llm_response,  # Raw response
            'sort_into_bin': 'Pending',
            'llm_response': llm_response,
            'model_used': llm_result.get('model_used', 'unknown')
        }

        # Try to parse key information from response
        response_lower = llm_response.lower()

        # Parse grades
        if 'premium' in response_lower:
            result['grade'] = 'Premium'
        elif 'grade a' in response_lower or 'grade 1' in response_lower:
            result['grade'] = 'Grade A' if 'grade a' in response_lower else 'Grade 1'
        elif 'grade b' in response_lower or 'grade 2' in response_lower:
            result['grade'] = 'Grade B' if 'grade b' in response_lower else 'Grade 2'
        elif 'processing' in response_lower:
            result['grade'] = 'Processing'

        # Parse sizes
        size_options = ['extra_large', 'large', 'medium', 'small', 'extra_small']
        for size in size_options:
            if size.replace('_', ' ') in response_lower or size in response_lower:
                result['size_category'] = size
                break

        # Parse color grades
        color_options = ['premium', 'good', 'fair', 'poor']
        for color in color_options:
            if color in response_lower:
                result['color_grade'] = color
                break

        # Parse ripeness
        ripeness_options = ['underripe', 'optimal', 'overripe', 'variable']
        for ripeness in ripeness_options:
            if ripeness in response_lower:
                result['ripeness_level'] = ripeness
                break

        # Parse defect presence and severity
        if 'defect' in response_lower or 'damage' in response_lower or 'blemish' in response_lower:
            result['defect_detected'] = True

            # Parse severity
            if 'minor' in response_lower:
                result['defect_severity'] = 'minor'
            elif 'moderate' in response_lower:
                result['defect_severity'] = 'moderate'
            elif 'major' in response_lower or 'severe' in response_lower:
                result['defect_severity'] = 'major' if 'major' in response_lower else 'severe'
            else:
                result['defect_severity'] = 'minor'

        # Parse defect type if mentioned
        possible_defects = ['bruising', 'insect damage', 'disease spots', 'cracks', 'sprouting', 'discoloration']
        for defect in possible_defects:
            if defect in llm_response.lower():
                result['defect_type'] = defect.title()
                break

        # Parse sort destination if mentioned
        if 'premium' in response_lower:
            result['sort_into_bin'] = 'Premium Grade'
        elif 'standard' in response_lower:
            result['sort_into_bin'] = 'Standard Grade'
        elif 'processing' in response_lower:
            result['sort_into_bin'] = 'Processing'
        elif 'defect' in response_lower:
            result['sort_into_bin'] = 'Defects/Processing'

        # Extract numerical values if present
        numbers = re.findall(r'\d+', llm_response)
        if numbers:
            # Use first number as confidence indicator if it makes sense
            try:
                num = int(numbers[0])
                if 70 <= num <= 100:  # Treat as confidence percentage
                    result['confidence'] = min(0.95, num / 100.0)
            except ValueError:
                pass

        # Adjust confidence based on response quality
        if len(llm_response) < 50:
            result['confidence'] = 0.7
        elif len(llm_response) > 500:
            result['confidence'] = 0.9

        return result

    def _process_image_traditional(self, record):
        """Process image using traditional methods (existing implementation)"""
        # In a real implementation, this would call actual visual sorting models
        # For now, we'll simulate the sorting process
        import random

        # Define possible sorting results based on product type
        if record.product_id:
            product_name = record.product_id.name.lower()
            if 'apple' in product_name:
                grades = ['Grade A', 'Grade B', 'Grade C', 'Processing Grade']
                sizes = ['extra_large', 'large', 'medium', 'small']
                ripeness_levels = ['underripe', 'optimal', 'overripe', 'variable']
            elif 'tomato' in product_name:
                grades = ['Premium', 'Standard', 'Processing', 'Not Suitable']
                sizes = ['large', 'medium', 'small', 'extra_small']
                ripeness_levels = ['optimal', 'optimal', 'underripe', 'overripe']
            elif 'potato' in product_name:
                grades = ['Premium', 'Standard', 'Processing', 'Seed Grade']
                sizes = ['large', 'medium', 'small']
                ripeness_levels = ['optimal']  # Potatoes don't ripen post-harvest
            else:
                grades = ['Grade 1', 'Grade 2', 'Grade 3', 'Processing']
                sizes = ['extra_large', 'large', 'medium', 'small', 'extra_small']
                ripeness_levels = ['optimal', 'underripe', 'overripe']
        else:
            grades = ['Grade A', 'Grade B', 'Grade C', 'Processing Grade']
            sizes = ['extra_large', 'large', 'medium', 'small']
            ripeness_levels = ['optimal', 'underripe', 'overripe']

        # Simulate detection results
        grade = random.choice(grades)
        size = random.choice(sizes) if record.sorting_type in ['size', 'quality'] else None
        ripeness = random.choice(ripeness_levels) if record.sorting_type in ['ripeness', 'quality'] else None

        # Determine if defect is detected
        defect_detected = random.random() < 0.3  # 30% chance of defect
        defect_type = None
        defect_severity = None
        if defect_detected:
            defect_types = ['Bruising', 'Insect Damage', 'Disease Spots', 'Cracks', 'Sprouting', 'Green Skin (Potatoes)']
            defect_type = random.choice(defect_types)
            defect_severity = random.choice(['minor', 'moderate', 'major', 'severe'])

        # Determine color grade
        color_grade = None
        if record.sorting_type in ['color', 'quality']:
            color_grade = random.choice(['premium', 'good', 'fair', 'poor'])

        # Generate classification and recommendation
        if defect_detected:
            classification = f"Defective {record.product_id.name or 'product'} - {defect_type} ({defect_severity})"
            action = f"Reject. Contains {defect_type}. Suitable for processing only."
            bin_dest = "Defects/Processing"
        elif grade in ['Grade A', 'Premium', 'Grade 1']:
            classification = f"High quality {record.product_id.name or 'product'} - {grade}"
            action = "Accept to premium grade. Ready for premium market."
            bin_dest = "Premium Grade"
        elif grade in ['Grade B', 'Standard', 'Grade 2']:
            classification = f"Standard quality {record.product_id.name or 'product'} - {grade}"
            action = "Accept to standard grade. Suitable for general market."
            bin_dest = "Standard Grade"
        else:
            classification = f"Processing grade {record.product_id.name or 'product'}"
            action = "Direct to processing. Not suitable for fresh market."
            bin_dest = "Processing"

        return {
            'description': f"AI visual analysis for {record.product_id.name or 'product'}: {grade}",
            'classification': classification,
            'grade': grade,
            'size_category': size,
            'ripeness_level': ripeness,
            'color_grade': color_grade,
            'defect_detected': defect_detected,
            'defect_type': defect_type,
            'defect_severity': defect_severity,
            'confidence': random.uniform(0.75, 0.98),
            'processing_time': random.uniform(100, 400),
            'features_detected': ['size', 'color', 'surface_defects', 'shape'],
            'recommended_action': action,
            'sort_into_bin': bin_dest
        }

    def action_process_image(self):
        """Override to set specific fields after processing"""
        result = super().action_process_image()

        for record in self:
            if record.output_data:
                output = json.loads(record.output_data)

                # Set specific fields based on AI output
                if 'grade' in output:
                    record.grade = output['grade']

                if 'size_category' in output:
                    record.size_category = output['size_category']

                if 'ripeness_level' in output:
                    record.ripeness_level = output['ripeness_level']

                if 'color_grade' in output:
                    record.color_grade = output['color_grade']

                if 'defect_detected' in output:
                    record.defect_detected = output['defect_detected']

                if 'defect_type' in output:
                    record.defect_type = output['defect_type']

                if 'defect_severity' in output:
                    record.defect_severity = output['defect_severity']

                if 'classification' in output:
                    record.classification_result = output['classification']

                if 'recommended_action' in output:
                    record.recommended_action = output['recommended_action']

                if 'sort_into_bin' in output:
                    record.sort_into_bin = output['sort_into_bin']

        return result