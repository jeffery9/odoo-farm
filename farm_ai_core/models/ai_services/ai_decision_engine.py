# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging
import time
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class AgriAiDecisionEngine(models.AbstractModel):
    """
    AI Decision Engine - Provides advanced decision-making capabilities
    """
    _name = 'agri.ai.decision.engine'
    _description = 'AI Decision Engine'

    def get_ai_recommendations(self, context_data, recommendation_type='general'):
        """
        Get AI-powered recommendations based on context data

        Args:
            context_data (dict): Contextual information for recommendations
            recommendation_type (str): Type of recommendation ('farming', 'resource', 'risk', etc.)

        Returns:
            dict: AI-powered recommendations
        """
        try:
            # Find the best model for the recommendation type
            task_mapping = {
                'farming': 'recommendation',
                'resource': 'analysis',
                'risk': 'prediction',
                'disease': 'detection',
                'yield': 'prediction',
                'market': 'prediction',
                'pest': 'detection'
            }

            model_type = task_mapping.get(recommendation_type, 'recommendation')
            best_model = self.get_best_model_for_task(model_type, performance_threshold=60.0)

            if best_model:
                # Run inference with the best model
                result = self.run_model_inference(best_model.id, context_data)
                if result.get('success'):
                    # Format the result as recommendations
                    recommendations = {
                        'success': True,
                        'model_used': best_model.name,
                        'recommendations': [
                            f"Based on AI analysis of type '{recommendation_type}': {result.get('output', 'AI analysis completed')}"
                        ],
                        'confidence': best_model.accuracy or 75.0,  # Default confidence if not set
                        'timestamp': fields.Datetime.now().isoformat()
                    }
                    return recommendations

            # If no model is available, try to get recommendations via AI service
            prompt = f"Based on this context: {context_data}, provide recommendations for {recommendation_type} management in agriculture."

            ai_result = self.call_ai_service('llm', prompt)
            if ai_result.get('success'):
                return {
                    'success': True,
                    'model_used': 'LLM Service',
                    'recommendations': [ai_result.get('response', 'AI service provided recommendations')],
                    'confidence': ai_result.get('confidence', 80.0),
                    'timestamp': fields.Datetime.now().isoformat()
                }

            return {
                'success': False,
                'error': 'No AI models or services available for recommendations',
                'recommendations': [],
                'timestamp': fields.Datetime.now().isoformat()
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'recommendations': [],
                'timestamp': fields.Datetime.now().isoformat()
            }

    def analyze_with_ai(self, data, analysis_type='classification'):
        """
        Perform AI-powered analysis on provided data

        Args:
            data: Data to analyze
            analysis_type (str): Type of analysis to perform

        Returns:
            dict: Analysis results
        """
        try:
            # Get the best model for the analysis type
            best_model = self.get_best_model_for_task(analysis_type, performance_threshold=65.0)

            if best_model:
                # Run inference using the best model
                result = self.run_model_inference(best_model.id, data)
                return {
                    'success': result.get('success', False),
                    'model_used': best_model.name,
                    'analysis_result': result.get('output'),
                    'confidence': best_model.accuracy or 0.0,
                    'processing_time': result.get('processing_time_ms'),
                    'timestamp': fields.Datetime.now().isoformat()
                }

            # If no model is available, use AI service
            prompt = f"Perform {analysis_type} analysis on: {data}"
            service_result = self.call_ai_service('llm', prompt)

            return {
                'success': service_result.get('success', False),
                'model_used': 'LLM Service',
                'analysis_result': service_result.get('response'),
                'confidence': service_result.get('confidence', 75.0),
                'timestamp': fields.Datetime.now().isoformat()
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'analysis_result': None,
                'timestamp': fields.Datetime.now().isoformat()
            }

    def get_ai_system_health(self):
        """
        Get an overview of the AI system's health and performance

        Returns:
            dict: Health metrics for the AI system
        """
        try:
            # Get statistics about AI configurations
            total_configs = self.env['agri.ai.configuration'].sudo().search_count([])
            active_configs = self.env['agri.ai.configuration'].sudo().search_count([('is_active', '=', True)])

            # Get statistics about AI models
            total_models = self.env['agri.ai.model.registry'].sudo().search_count([])
            active_models = self.env['agri.ai.model.registry'].sudo().search_count([('is_active', '=', True)])

            # Get recent AI activity
            recent_time = datetime.now() - timedelta(hours=24)

            # Find service models that might have activity logs
            all_models = list(self.env.registry.keys())
            total_requests = 0
            successful_requests = 0

            for model_name in all_models:
                if 'service' in model_name.lower():
                    try:
                        model = self.env[model_name]
                        if hasattr(model, '_fields') and 'call_count' in model._fields:
                            records = self.env[model_name].sudo().search([])
                            for record in records:
                                total_requests += getattr(record, 'call_count', 0)
                                successful_requests += getattr(record, 'call_count', 0) - getattr(record, 'error_count', 0)
                    except (KeyError, AttributeError, TypeError):
                        continue

            health_report = {
                'overall_status': 'healthy' if active_configs > 0 and active_models > 0 else 'needs_attention',
                'configurations': {
                    'total': total_configs,
                    'active': active_configs,
                },
                'models': {
                    'total': total_models,
                    'active': active_models,
                },
                'recent_activity': {
                    'total_requests': total_requests,
                    'successful_requests': successful_requests,
                    'success_rate': (successful_requests / total_requests * 100) if total_requests > 0 else 0
                },
                'timestamp': datetime.now().isoformat()
            }

            return health_report
        except Exception as e:
            return {
                'overall_status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def get_best_model_for_task(self, task_type, performance_threshold=70.0):
        """
        Find the best AI model for a specific task based on performance metrics

        Args:
            task_type (str): Type of task ('classification', 'detection', 'prediction', etc.)
            performance_threshold (float): Minimum performance threshold

        Returns:
            AIModelRegistry: Best performing model for the task
        """
        # Find the best model for the given task type
        best_model = self.env['agri.ai.model.registry'].search([
            ('model_type', '=', task_type),
            ('is_active', '=', True),
            ('accuracy', '>=', performance_threshold)
        ], order='accuracy desc', limit=1)

        if not best_model:
            # If no model meets threshold, find the best available one
            best_model = self.env['agri.ai.model.registry'].search([
                ('model_type', '=', task_type),
                ('is_active', '=', True)
            ], order='accuracy desc', limit=1)

        return best_model

    def run_model_inference(self, model_id, input_data):
        """
        Run inference on a specific AI model

        Args:
            model_id (int): ID of the AI model to use
            input_data: Input data for the model

        Returns:
            dict: Inference result with output and metadata
        """
        try:
            model = self.env['agri.ai.model.registry'].browse(model_id)
            if not model.exists() or not model.is_active:
                return {
                    'success': False,
                    'error': 'Model does not exist or is not active',
                    'output': None
                }

            # Load the model and run inference
            load_result = model.load_model()
            if not load_result.get('model_loaded'):
                return {
                    'success': False,
                    'error': 'Failed to load model',
                    'output': None
                }

            # In a real implementation, this would run the actual model inference
            # For now, we'll return a simulated result
            start_time = time.time()

            # Simulate processing time
            time.sleep(0.1)  # Simulate actual processing

            processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds

            # Update model statistics
            model.update_inference_stats(processing_time)

            # This would be replaced with actual model inference in production
            result = {
                'success': True,
                'output': f"Simulated inference result for model {model.name}",
                'model_used': model.name,
                'processing_time_ms': processing_time,
                'input_data': input_data
            }

            return result
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'output': None
            }

    def evaluate_ai_model_performance(self, model_id, test_dataset):
        """
        Evaluate the performance of an AI model on a test dataset

        Args:
            model_id (int): ID of the model to evaluate
            test_dataset: Dataset to evaluate the model on

        Returns:
            dict: Performance metrics
        """
        try:
            model = self.env['agri.ai.model.registry'].browse(model_id)
            if not model.exists():
                return {
                    'success': False,
                    'error': 'Model does not exist',
                    'metrics': None
                }

            # In a real implementation, this would run the model on the test dataset
            # and calculate performance metrics like accuracy, precision, recall, etc.
            # For simulation, we'll return placeholder metrics

            # This is a placeholder implementation showing how a real evaluation would work
            result = {
                'success': True,
                'metrics': {
                    'accuracy': model.accuracy or 0.0,
                    'precision': model.precision or 0.0,
                    'recall': model.recall or 0.0,
                    'f1_score': model.f1_score or 0.0,
                    'mae': model.mae or 0.0,
                    'evaluation_time': 1000,  # milliseconds
                    'samples_evaluated': len(test_dataset) if isinstance(test_dataset, (list, tuple)) else 100
                }
            }

            return result
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'metrics': None
            }