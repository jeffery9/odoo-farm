from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging
import json
from datetime import datetime, timedelta
import random

_logger = logging.getLogger(__name__)


class AgriAiBaseMixin(models.AbstractModel):
    """
    Agri Domain Level: AI Base Capabilities. [US-58-01, US-104-2026]
    Provides universal AI interfaces for all agricultural sub-sectors.
    Follows the 'Agri as Domain, Farm as Entity' semantic strategy.
    Replaces the legacy ai.base.mixin.
    """
    _name = 'agri.ai.base.mixin'
    _description = 'Agricultural Domain AI Base Mixin'

    # Common AI fields
    ai_model_used = fields.Char('AI Model Used', help='Name of the AI model used for processing')
    ai_confidence_score = fields.Float('AI Confidence Score', help='Confidence score from 0-100', default=50.0)
    ai_processing_time = fields.Float('Processing Time (ms)', help='Time taken by AI to process')
    ai_input_data = fields.Text('AI Input Data', help='Raw input data sent to AI')
    ai_output_data = fields.Text('AI Output Data', help='Raw output data from AI')
    ai_status = fields.Selection([
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], string='AI Status', default='pending')
    ai_feedback_score = fields.Float('AI Feedback Score', help='Score based on user feedback (0-100)')

    def action_process_with_ai(self):
        """Process the record with AI and update fields"""
        # This method is now available via the AIBaseMixinService abstract model
        mixin_service = self.env['agri.ai.base.mixin.service']
        return mixin_service.action_process_with_ai()

    def _process_ai(self):
        """Override in specific models to implement AI processing logic"""
        return {
            'model_used': 'Default Agri-AI Model',
            'confidence': 0.0,
            'processing_time': 0.0,
            'input_data': {},
            'output_data': {},
        }

    def _update_from_ai_result(self, result):
        """Override in specific models to update fields from AI result"""
        pass

    def get_active_ai_config(self):
        """Get the active AI configuration for this record - abstract method"""
        # This method is now available via the AIBaseMixinService abstract model
        mixin_service = self.env['agri.ai.base.mixin.service']
        return mixin_service.get_active_ai_config()

    def call_llm_service(self, prompt, context_data=None):
        """Generic method to call LLM service if available"""
        # This method is now available via the AIBaseMixinService abstract model
        mixin_service = self.env['agri.ai.base.mixin.service']
        return mixin_service.call_llm_service(prompt, context_data)

    def call_ai_service(self, service_type, prompt, context_data=None, model_override=None):
        """
        Generic method to call any type of AI service (LLM, Vision, ML, etc.)
        """
        # This method is now available via the AIBaseMixinService abstract model
        mixin_service = self.env['agri.ai.base.mixin.service']
        return mixin_service.call_ai_service(service_type, prompt, context_data, model_override)

    def process_with_ai_decision_engine(self, data, decision_type='classification'):
        """
        Use domain-level AI decision engine to process data and make decisions

        Args:
            data (dict): Input data to process
            decision_type (str): Type of decision to make

        Returns:
            dict: Decision result with confidence
        """
        # Find available AI decision engines
        all_models = list(self.env.registry.keys())

        for model_name in all_models:
            if 'decision' in model_name.lower() or 'engine' in model_name.lower():
                try:
                    model = self.env[model_name]
                    if hasattr(model, 'make_decision') or hasattr(model, 'process_decision'):
                        service = self.env[model_name].sudo().search([], limit=1)
                        if service:
                            if hasattr(service, 'make_decision'):
                                return service.make_decision(data, decision_type)
                            elif hasattr(service, 'process_decision'):
                                return service.process_decision(data, decision_type)
                except (KeyError, AttributeError, TypeError):
                    continue

        # Default fallback - return a basic decision structure
        return {
            'success': False,
            'error': 'No Agri AI decision engine available',
            'decision': None,
            'confidence': 0.0
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
        # This method is now available via the AIDecisionEngine abstract model
        decision_engine = self.env['agri.ai.decision.engine']
        return decision_engine.get_best_model_for_task(task_type, performance_threshold)

    def run_model_inference(self, model_id, input_data):
        """
        Run inference on a specific AI model

        Args:
            model_id (int): ID of the AI model to use
            input_data: Input data for the model

        Returns:
            dict: Inference result with output and metadata
        """
        # This method is now available via the AIDecisionEngine abstract model
        decision_engine = self.env['agri.ai.decision.engine']
        return decision_engine.run_model_inference(model_id, input_data)

    def evaluate_ai_model_performance(self, model_id, test_dataset):
        """
        Evaluate the performance of an AI model on a test dataset

        Args:
            model_id (int): ID of the model to evaluate
            test_dataset: Dataset to evaluate the model on

        Returns:
            dict: Performance metrics
        """
        # This method is now available via the AIDecisionEngine abstract model
        decision_engine = self.env['agri.ai.decision.engine']
        return decision_engine.evaluate_ai_model_performance(model_id, test_dataset)

    def get_ai_recommendations(self, context_data, recommendation_type='general'):
        """
        Get AI-powered recommendations based on context data

        Args:
            context_data (dict): Contextual information for recommendations
            recommendation_type (str): Type of recommendation ('farming', 'resource', 'risk', etc.)

        Returns:
            dict: AI-powered recommendations
        """
        # This method is now available via the AIDecisionEngine abstract model
        decision_engine = self.env['agri.ai.decision.engine']
        return decision_engine.get_ai_recommendations(context_data, recommendation_type)

    def analyze_with_ai(self, data, analysis_type='classification'):
        """
        Perform AI-powered analysis on provided data

        Args:
            data: Data to analyze
            analysis_type (str): Type of analysis to perform

        Returns:
            dict: Analysis results
        """
        # This method is now available via the AIDecisionEngine abstract model
        decision_engine = self.env['agri.ai.decision.engine']
        return decision_engine.analyze_with_ai(data, analysis_type)

    def get_ai_system_health(self):
        """
        Get an overview of the AI system's health and performance

        Returns:
            dict: Health metrics for the AI system
        """
        # This method is now available via the AIDecisionEngine abstract model
        decision_engine = self.env['agri.ai.decision.engine']
        return decision_engine.get_ai_system_health()


class AgriAiConfiguration(models.AbstractModel):
    """
    AI Configuration and Settings - Abstract interface for AI configurations
    Implementation should be provided by specialized AI modules like farm_ai_llm_integration
    """
    _name = 'agri.ai.configuration'
    _description = 'AI Configuration Interface'

    name = fields.Char('Configuration Name', required=True)
    ai_provider = fields.Selection([
        ('llm', 'LLM Service'),
        ('vision', 'Computer Vision'),
        ('ml', 'Machine Learning'),
        ('custom', 'Custom AI Service'),
    ], string='AI Provider Type', required=True, default='llm')

    # Common configuration fields
    api_key = fields.Char('API Key', help='API key for the AI service')
    base_url = fields.Char('Base URL', help='Base URL for the AI service API')
    default_model = fields.Char('Default Model', help='Default model to use')
    is_active = fields.Boolean('Is Active', default=False)
    is_default = fields.Boolean('Is Default', default=False)

    # Common performance settings
    timeout = fields.Integer('Timeout (seconds)', default=30, help='Request timeout in seconds')
    max_retries = fields.Integer('Max Retries', default=3, help='Number of retries on failure')

    # Statistics
    total_requests = fields.Integer('Total Requests', default=0, readonly=True)
    successful_requests = fields.Integer('Successful Requests', default=0, readonly=True)
    failed_requests = fields.Integer('Failed Requests', default=0, readonly=True)
    last_used = fields.Datetime('Last Used', readonly=True)

    _name_unique = models.Constraint(
        'UNIQUE(name)',
        'Configuration name must be unique!'
    )

    def test_connection(self):
        """
        Test the AI service connection - should be implemented by specialized modules
        """
        raise NotImplementedError(_("This method should be implemented by the specific AI module"))

    def increment_request_stats(self, success=True):
        """Increment request statistics"""
        for config in self:
            vals = {
                'total_requests': config.total_requests + 1,
                'last_used': fields.Datetime.now()
            }
            if success:
                vals['successful_requests'] = config.successful_requests + 1
            else:
                vals['failed_requests'] = config.failed_requests + 1
            config.write(vals)




class AgriAiModelRegistry(models.Model):
    """
    AI Model Registry.
    Integrated with domain-level decision capabilities via Mixins.
    """
    _name = 'agri.ai.model.registry'
    _description = 'AI Model Registry'
    _inherit = [
        'agri.ai.decision.engine', 
        'agri.ai.base.mixin' # [Refactored to Agri Domain Mixin]
    ]

    name = fields.Char('Model Name', required=True)
    model_type = fields.Selection([
        ('classification', 'Classification'),
        ('detection', 'Object Detection'),
        ('segmentation', 'Image Segmentation'),
        ('generation', 'Content Generation'),
        ('prediction', 'Time Series Prediction'),
        ('analysis', 'Data Analysis'),
        ('vision', 'Computer Vision'),
        ('nlp', 'Natural Language Processing'),
        ('recommendation', 'Recommendation System'),
        ('regression', 'Regression Analysis'),
        ('clustering', 'Clustering'),
        ('anomaly_detection', 'Anomaly Detection'),
    ], string='Model Type', required=True)

    description = fields.Text('Description')
    version = fields.Char('Version', required=True, default='1.0.0')

    # Performance metrics
    accuracy = fields.Float('Accuracy (%)')
    precision = fields.Float('Precision (%)')
    recall = fields.Float('Recall (%)')
    f1_score = fields.Float('F1 Score (%)')
    mae = fields.Float('Mean Absolute Error', help='For regression models')
    mse = fields.Float('Mean Squared Error', help='For regression models')
    rmse = fields.Float('Root Mean Squared Error', help='For regression models')

    last_trained = fields.Datetime('Last Trained')
    training_dataset = fields.Char('Training Dataset')
    training_samples_count = fields.Integer('Training Samples Count', help='Number of samples used for training')

    # Agricultural-specific performance metrics
    domain_specific_metrics = fields.Text('Domain-specific Metrics', help='JSON format for domain-specific metrics')

    # Model metadata
    input_format = fields.Char('Input Format', help='Expected input format (e.g., image, text, structured data)')
    output_format = fields.Char('Output Format', help='Expected output format')
    hardware_requirements = fields.Char('Hardware Requirements', help='Recommended hardware (e.g., GPU, RAM)')

    # Model configuration
    config_params = fields.Text('Configuration Parameters', help='JSON configuration for the model')
    preprocessing_steps = fields.Text('Preprocessing Steps', help='Steps required to preprocess input data')
    postprocessing_steps = fields.Text('Postprocessing Steps', help='Steps required to process model output')

    is_active = fields.Boolean('Is Active', default=True)
    is_default = fields.Boolean('Is Default', default=False)
    is_agricultural_model = fields.Boolean('Is Agricultural Model', default=True,
        help="Indicates if this model is specifically designed for agricultural applications")

    # Performance and usage statistics
    inference_count = fields.Integer('Inference Count', default=0, readonly=True)
    avg_inference_time = fields.Float('Avg Inference Time (ms)', readonly=True)
    last_used = fields.Datetime('Last Used', readonly=True)

    # Agricultural domain-specific fields
    target_crops = fields.Char('Target Crops', help='Comma-separated list of crops this model targets')
    target_conditions = fields.Char('Target Conditions', help='Environmental conditions this model is optimized for')
    recommended_use_cases = fields.Text('Recommended Use Cases', help='Specific use cases this model is recommended for')

    _name_version_unique = models.Constraint(
        'UNIQUE(name, version)',
        'Model name and version must be unique!'
    )
    _name_required = models.Constraint(
        'CHECK(name != \'\')',
        'Model name is required!'
    )
    _version_required = models.Constraint(
        'CHECK(version != \'\')',
        'Version is required!'
    )

    @api.constrains('accuracy', 'precision', 'recall', 'f1_score')
    def _check_performance_metrics(self):
        """Ensure performance metrics are within valid range"""
        for record in self:
            if record.accuracy and (record.accuracy < 0 or record.accuracy > 100):
                raise ValidationError(_("Accuracy must be between 0 and 100."))
            if record.precision and (record.precision < 0 or record.precision > 100):
                raise ValidationError(_("Precision must be between 0 and 100."))
            if record.recall and (record.recall < 0 or record.recall > 100):
                raise ValidationError(_("Recall must be between 0 and 100."))
            if record.f1_score and (record.f1_score < 0 or record.f1_score > 100):
                raise ValidationError(_("F1 Score must be between 0 and 100."))

    def load_model(self):
        """
        Load the Agri AI model for inference.
        """
        _logger.info(f"Loading Agri AI model {self.name} (version {self.version})")
        return {
            'model_loaded': True,
            'model_name': self.name,
            'model_type': self.model_type,
            'config': self.config_params
        }

    def update_inference_stats(self, inference_time_ms):
        """Update model inference statistics"""
        for model in self:
            total_inferences = model.inference_count + 1
            new_avg_time = ((model.avg_inference_time * model.inference_count) + inference_time_ms) / total_inferences

            model.write({
                'inference_count': total_inferences,
                'avg_inference_time': new_avg_time,
                'last_used': fields.Datetime.now()
            })

    @api.model
    def get_default_model_for_type(self, model_type):
        """Get the default model for a specific model type"""
        return self.search([
            ('model_type', '=', model_type),
            ('is_default', '=', True),
            ('is_active', '=', True)
        ], limit=1)

    @api.model
    def get_agricultural_models_for_task(self, task_type):
        """
        Get agricultural-specific models for a particular task
        """
        return self.search([
            ('model_type', '=', task_type),
            ('is_agricultural_model', '=', True),
            ('is_active', '=', True)
        ])

    def action_evaluate_model(self):
        """Action to evaluate model performance on test dataset"""
        for model in self:
            _logger.info(f"Evaluating model {model.name}")
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Model Evaluation'),
                    'message': f"Model {model.name} evaluation started in background",
                    'type': 'info',
                    'sticky': False,
                }
            }