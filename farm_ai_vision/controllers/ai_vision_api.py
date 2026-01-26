# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import json
from odoo import http
from odoo.http import request
from odoo.exceptions import UserError
import base64
from datetime import datetime

_logger = logging.getLogger(__name__)


class AIVisionAPIController(http.Controller):
    """
    AI Vision API Controller - provides RESTful OpenAPI endpoints for AI vision services
    """

    @http.route('/api/ai-vision/health', type='http', auth='none', methods=['GET'], csrf=False)
    def health_check(self):
        """Health check endpoint to verify API availability"""
        response = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'service': 'AI Vision Service',
            'version': '1.0.0'
        }
        return http.Response(
            json.dumps(response),
            status=200,
            mimetype='application/json'
        )

    @http.route('/api/ai-vision/detect-pest-disease', type='json', auth='user', methods=['POST'], csrf=False)
    def detect_pest_disease(self, **kwargs):
        """
        Detect pests and diseases from uploaded image
        Expected JSON payload:
        {
            "image_data": "base64_encoded_image_string",
            "image_filename": "optional_filename.jpg",
            "crop_type": "optional_crop_type",
            "location_id": "optional_location_id"
        }
        """
        try:
            # Get parameters from JSON request
            image_data = request.jsonrequest.get('image_data')
            image_filename = request.jsonrequest.get('image_filename', 'uploaded_image.jpg')
            crop_type = request.jsonrequest.get('crop_type')
            location_id = request.jsonrequest.get('location_id')

            if not image_data:
                return {
                    'error': 'Image data is required',
                    'success': False
                }

            # Create a new pest disease detection record
            pest_disease_model = request.env['ai.pest.disease.detection'].sudo()

            # Decode base64 image data
            try:
                image_binary = base64.b64decode(image_data)
            except Exception:
                return {
                    'error': 'Invalid image data format',
                    'success': False
                }

            # Create the record with image
            record = pest_disease_model.create({
                'name': f'Pest Disease Detection - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                'image': base64.b64encode(image_binary),
                'image_filename': image_filename,
                'detection_type': 'pest',  # Default to pest detection
                'status': 'processing'
            })

            # Process the image
            record.action_process_image()

            # Return the analysis results
            return {
                'success': True,
                'detection_id': record.id,
                'detected_pest_disease': record.detected_pest_disease,
                'confidence_score': record.confidence_score,
                'severity_level': record.severity_level,
                'treatment_priority': record.treatment_priority,
                'recommended_treatment': record.recommended_treatment,
                'analysis_result': record.analysis_result,
                'processing_time': record.processing_time
            }

        except Exception as e:
            _logger.error(f"Error in pest disease detection API: {str(e)}")
            return {
                'error': str(e),
                'success': False
            }

    @http.route('/api/ai-vision/visual-sorting', type='json', auth='user', methods=['POST'], csrf=False)
    def visual_sorting(self, **kwargs):
        """
        Perform visual sorting and grading of agricultural products
        Expected JSON payload:
        {
            "image_data": "base64_encoded_image_string",
            "image_filename": "optional_filename.jpg",
            "product_id": "optional_product_id",
            "batch_id": "optional_batch_id"
        }
        """
        try:
            # Get parameters from JSON request
            image_data = request.jsonrequest.get('image_data')
            image_filename = request.jsonrequest.get('image_filename', 'uploaded_image.jpg')
            product_id = request.jsonrequest.get('product_id')
            batch_id = request.jsonrequest.get('batch_id')

            if not image_data:
                return {
                    'error': 'Image data is required',
                    'success': False
                }

            # Create a new visual sorting record
            visual_sorting_model = request.env['ai.visual.sorting'].sudo()

            # Decode base64 image data
            try:
                image_binary = base64.b64decode(image_data)
            except Exception:
                return {
                    'error': 'Invalid image data format',
                    'success': False
                }

            # Create the record with image
            record = visual_sorting_model.create({
                'name': f'Visual Sorting - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                'image': base64.b64encode(image_binary),
                'image_filename': image_filename,
                'sorting_type': 'quality',  # Default to quality sorting
                'status': 'processing'
            })

            # Process the image
            record.action_process_image()

            # Return the analysis results
            return {
                'success': True,
                'sorting_id': record.id,
                'grade': record.grade,
                'size_category': record.size_category,
                'color_grade': record.color_grade,
                'ripeness_level': record.ripeness_level,
                'defect_detected': record.defect_detected,
                'defect_type': record.defect_type,
                'defect_severity': record.defect_severity,
                'confidence_score': record.confidence_score,
                'recommended_action': record.recommended_action,
                'sort_into_bin': record.sort_into_bin,
                'processing_time': record.processing_time
            }

        except Exception as e:
            _logger.error(f"Error in visual sorting API: {str(e)}")
            return {
                'error': str(e),
                'success': False
            }

    @http.route('/api/ai-vision/image-analysis-prediction', type='json', auth='user', methods=['POST'], csrf=False)
    def image_analysis_prediction(self, **kwargs):
        """
        Perform image analysis and predictive analytics
        Expected JSON payload:
        {
            "image_data": "base64_encoded_image_string",
            "image_filename": "optional_filename.jpg",
            "crop_id": "optional_crop_id"
        }
        """
        try:
            # Get parameters from JSON request
            image_data = request.jsonrequest.get('image_data')
            image_filename = request.jsonrequest.get('image_filename', 'uploaded_image.jpg')
            crop_id = request.jsonrequest.get('crop_id')

            if not image_data:
                return {
                    'error': 'Image data is required',
                    'success': False
                }

            # Create a new image analysis prediction record
            prediction_model = request.env['ai.image.analysis.prediction'].sudo()

            # Decode base64 image data
            try:
                image_binary = base64.b64decode(image_data)
            except Exception:
                return {
                    'error': 'Invalid image data format',
                    'success': False
                }

            # Create the record with image
            record = prediction_model.create({
                'name': f'Image Analysis Prediction - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                'image': base64.b64encode(image_binary),
                'image_filename': image_filename,
                'status': 'processing'
            })

            # Process the image
            record.action_process_image()

            # Return the analysis results
            return {
                'success': True,
                'prediction_id': record.id,
                'predicted_yield': record.predicted_yield,
                'growth_stage': record.growth_stage,
                'optimal_harvest_time': record.optimal_harvest_time,
                'confidence_score': record.confidence_score,
                'growth_prediction': record.growth_prediction,
                'potential_issues': record.potential_issues,
                'risk_factors': record.risk_factors,
                'mitigation_strategies': record.mitigation_strategies,
                'processing_time': record.processing_time
            }

        except Exception as e:
            _logger.error(f"Error in image analysis prediction API: {str(e)}")
            return {
                'error': str(e),
                'success': False
            }

    @http.route('/api/ai-vision/risk-assessment', type='json', auth='user', methods=['POST'], csrf=False)
    def vision_risk_assessment(self, **kwargs):
        """
        Perform AI vision-based risk assessment
        Expected JSON payload:
        {
            "image_data": "base64_encoded_image_string",
            "image_filename": "optional_filename.jpg",
            "risk_type": "crop_health|weather_damage|pest_outbreak|disease_spread|quality_defect|yield_loss"
        }
        """
        try:
            # Get parameters from JSON request
            image_data = request.jsonrequest.get('image_data')
            image_filename = request.jsonrequest.get('image_filename', 'uploaded_image.jpg')
            risk_type = request.jsonrequest.get('risk_type', 'crop_health')

            if not image_data:
                return {
                    'error': 'Image data is required',
                    'success': False
                }

            # Validate risk type
            valid_risk_types = ['crop_health', 'weather_damage', 'pest_outbreak', 'disease_spread', 'quality_defect', 'yield_loss']
            if risk_type not in valid_risk_types:
                return {
                    'error': f'Invalid risk type. Must be one of: {", ".join(valid_risk_types)}',
                    'success': False
                }

            # Create a new vision risk assessment record
            risk_model = request.env['ai.vision.risk.assessment'].sudo()

            # Decode base64 image data
            try:
                image_binary = base64.b64decode(image_data)
            except Exception:
                return {
                    'error': 'Invalid image data format',
                    'success': False
                }

            # Create the record with image
            record = risk_model.create({
                'name': f'Vision Risk Assessment - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                'image': base64.b64encode(image_binary),
                'image_filename': image_filename,
                'risk_type': risk_type,
                'status': 'processing'
            })

            # Process the image
            record.action_process_image()

            # Return the analysis results
            return {
                'success': True,
                'risk_assessment_id': record.id,
                'risk_type': record.risk_type,
                'risk_level': record.risk_level,
                'risk_score': record.risk_score,
                'affected_area_percentage': record.affected_area_percentage,
                'potential_loss': record.potential_loss,
                'confidence_score': record.confidence_score,
                'risk_description': record.risk_description,
                'mitigation_recommendations': record.mitigation_recommendations,
                'risk_monitoring_plan': record.risk_monitoring_plan,
                'processing_time': record.processing_time
            }

        except Exception as e:
            _logger.error(f"Error in vision risk assessment API: {str(e)}")
            return {
                'error': str(e),
                'success': False
            }

    @http.route('/api/ai-vision/image-based-planning', type='json', auth='user', methods=['POST'], csrf=False)
    def image_based_planning(self, **kwargs):
        """
        Generate image-based planting recommendations
        Expected JSON payload:
        {
            "image_data": "base64_encoded_image_string",
            "image_filename": "optional_filename.jpg",
            "land_location_id": "optional_location_id"
        }
        """
        try:
            # Get parameters from JSON request
            image_data = request.jsonrequest.get('image_data')
            image_filename = request.jsonrequest.get('image_filename', 'uploaded_image.jpg')
            land_location_id = request.jsonrequest.get('land_location_id')

            if not image_data:
                return {
                    'error': 'Image data is required',
                    'success': False
                }

            # Create a new image-based planning record
            planning_model = request.env['ai.image.based.planning'].sudo()

            # Decode base64 image data
            try:
                image_binary = base64.b64decode(image_data)
            except Exception:
                return {
                    'error': 'Invalid image data format',
                    'success': False
                }

            # Create the record with image
            record = planning_model.create({
                'name': f'Image-Based Planning - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                'image': base64.b64encode(image_binary),
                'image_filename': image_filename,
                'status': 'processing'
            })

            # Process the image
            record.action_process_image()

            # Return the analysis results
            return {
                'success': True,
                'planning_id': record.id,
                'crop_type': record.crop_type.name if record.crop_type else None,
                'soil_condition': record.soil_condition,
                'planting_season': record.planting_season,
                'confidence_score': record.confidence_score,
                'planting_density': record.planting_density,
                'spacing_recommendation': record.spacing_recommendation,
                'field_preparation_needed': record.field_preparation_needed,
                'special_considerations': record.special_considerations,
                'processing_time': record.processing_time
            }

        except Exception as e:
            _logger.error(f"Error in image-based planning API: {str(e)}")
            return {
                'error': str(e),
                'success': False
            }