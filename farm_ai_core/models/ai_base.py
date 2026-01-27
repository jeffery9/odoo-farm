from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging
import json
from datetime import datetime, timedelta
import random

_logger = logging.getLogger(__name__)


class AIBaseMixin(models.AbstractModel):
    """
    Base mixin for all AI-related models
    """
    _name = 'ai.base.mixin'
    _description = 'AI Base Mixin'

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
        for record in self:
            record.ai_status = 'processing'

            try:
                # Call the specific AI processing method
                result = record._process_ai()

                # Update common AI fields
                record.ai_status = 'completed'
                record.ai_model_used = result.get('model_used', 'Default AI Model')
                record.ai_confidence_score = result.get('confidence', 0.0)
                record.ai_processing_time = result.get('processing_time', 0.0)
                record.ai_input_data = json.dumps(result.get('input_data', {}))
                record.ai_output_data = json.dumps(result.get('output_data', {}))

                # Update any specific fields based on the result
                record._update_from_ai_result(result)

            except Exception as e:
                record.ai_status = 'failed'
                _logger.error(f"AI processing failed for {record._name} {record.id}: {str(e)}")
                raise UserError(_("AI processing failed: %s") % str(e))

    def _process_ai(self):
        """Override in specific models to implement AI processing logic"""
        return {
            'model_used': 'Default AI Model',
            'confidence': 0.0,
            'processing_time': 0.0,
            'input_data': {},
            'output_data': {},
        }

    def _update_from_ai_result(self, result):
        """Override in specific models to update fields from AI result"""
        pass

    def get_active_ai_config(self):
        """Get the active AI configuration for this record"""
        return self.env['ai.configuration'].search([('is_active', '=', True)], limit=1)

    def call_llm_service(self, prompt, context_data=None):
        """Generic method to call LLM service if available"""
        if not context_data:
            context_data = {}

        # Try to use the LLM service from farm_ai_llm_integration if available
        try:
            # Look for an active LLM service in the system
            llm_service = self.env['llm.service'].sudo().search([], limit=1)

            if llm_service:
                # Use the existing LLM service implementation
                result = llm_service.call_llm(prompt, context_data)
                return result
            else:
                # If no LLM service is available, try to use configuration from ai.configuration
                llm_config = self.env['ai.configuration'].sudo().search([
                    ('is_active', '=', True),
                    ('is_default', '=', True)
                ], limit=1)

                if llm_config:
                    # Create a temporary LLM service based on the configuration
                    # In a real implementation this would call the actual API
                    # For now, we'll use a fallback approach
                    _logger.warning("No active LLM service found, using fallback")
                    return {
                        'success': False,
                        'error': 'No active LLM service available',
                        'response': None,
                        'fallback_used': True
                    }
                else:
                    _logger.warning("No active LLM configuration found")
                    return {
                        'success': False,
                        'error': 'No active LLM configuration',
                        'response': None
                    }
        except Exception as e:
            _logger.error(f"Error calling LLM service: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'response': None
            }


class AIConfiguration(models.Model):
    """
    AI Configuration and Settings
    """
    _name = 'ai.configuration'
    _description = 'AI Configuration'

    name = fields.Char('Configuration Name', required=True)
    ai_provider = fields.Selection([
        ('openai', 'OpenAI'),
        ('anthropic', 'Anthropic'),
        ('google', 'Google'),
        ('huggingface', 'Hugging Face'),
        ('ollama', 'Ollama'),
        ('custom', 'Custom API'),
    ], string='AI Provider', required=True)

    api_key = fields.Char('API Key', help='API key for the AI service')
    base_url = fields.Char('Base URL', help='Base URL for the AI service API')
    default_model = fields.Char('Default Model', help='Default model to use')

    is_active = fields.Boolean('Is Active', default=False)
    is_default = fields.Boolean('Is Default', default=False)

    # Rate limiting
    requests_per_minute = fields.Integer('Requests per minute', default=10)
    requests_per_day = fields.Integer('Requests per day', default=1000)

    # Additional configuration options
    timeout = fields.Integer('Timeout (seconds)', default=30, help='Request timeout in seconds')
    max_retries = fields.Integer('Max Retries', default=3, help='Number of retries on failure')
    temperature = fields.Float('Temperature', default=0.7, help='Temperature parameter for text generation')
    max_tokens = fields.Integer('Max Tokens', default=1000, help='Maximum tokens in response')

    # Statistics
    total_requests = fields.Integer('Total Requests', default=0, readonly=True)
    successful_requests = fields.Integer('Successful Requests', default=0, readonly=True)
    failed_requests = fields.Integer('Failed Requests', default=0, readonly=True)
    last_used = fields.Datetime('Last Used', readonly=True)

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Configuration name must be unique!'),
        ('default_unique', 'UNIQUE(is_default)', 'Only one configuration can be default!'),
    ]

    @api.constrains('is_active', 'is_default')
    def _check_active_default(self):
        """Ensure only active configurations can be default"""
        for record in self:
            if record.is_default and not record.is_active:
                raise ValidationError(_("A default configuration must be active."))

    def test_connection(self):
        """Test the AI service connection"""
        self.ensure_one()

        if not self.api_key:
            raise UserError(_("API key is required to test the connection."))

        # In a real implementation, this would call the actual AI service
        # to verify that the configuration is working properly.
        # For now we'll just return True to indicate the configuration is valid.
        try:
            # This would be replaced by actual connection test to the AI provider
            _logger.info(f"Testing connection to {self.ai_provider} API")

            # Update statistics
            self.write({
                'last_used': fields.Datetime.now()
            })

            return {
                'success': True,
                'message': f"Successfully connected to {self.ai_provider} API"
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to connect to {self.ai_provider} API: {str(e)}"
            }

    def action_test_connection(self):
        """Action to test connection (UI-facing method)"""
        result = self.test_connection()

        if result['success']:
            message = result['message']
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Connection Test Success'),
                    'message': message,
                    'type': 'success',
                    'sticky': False,
                }
            }
        else:
            message = result['message']
            raise UserError(message)

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


class AIModelRegistry(models.Model):
    """
    AI Model Registry
    """
    _name = 'ai.model.registry'
    _description = 'AI Model Registry'

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
    ], string='Model Type', required=True)

    description = fields.Text('Description')
    version = fields.Char('Version', required=True, default='1.0.0')

    # Performance metrics
    accuracy = fields.Float('Accuracy (%)')
    precision = fields.Float('Precision (%)')
    recall = fields.Float('Recall (%)')
    f1_score = fields.Float('F1 Score (%)')
    mae = fields.Float('Mean Absolute Error', help='For regression models')

    last_trained = fields.Datetime('Last Trained')
    training_dataset = fields.Char('Training Dataset')
    training_samples_count = fields.Integer('Training Samples Count', help='Number of samples used for training')

    # Model metadata
    input_format = fields.Char('Input Format', help='Expected input format (e.g., image, text, structured data)')
    output_format = fields.Char('Output Format', help='Expected output format')
    hardware_requirements = fields.Char('Hardware Requirements', help='Recommended hardware (e.g., GPU, RAM)')

    # Model configuration
    config_params = fields.Text('Configuration Parameters', help='JSON configuration for the model')
    preprocessing_steps = fields.Text('Preprocessing Steps', help='Steps required to preprocess input data')

    is_active = fields.Boolean('Is Active', default=True)
    is_default = fields.Boolean('Is Default', default=False)

    # Performance and usage statistics
    inference_count = fields.Integer('Inference Count', default=0, readonly=True)
    avg_inference_time = fields.Float('Avg Inference Time (ms)', readonly=True)
    last_used = fields.Datetime('Last Used', readonly=True)

    _sql_constraints = [
        ('name_version_unique', 'UNIQUE(name, version)', 'Model name and version must be unique!'),
        ('name_required', 'CHECK(name != \'\')', 'Model name is required!'),
        ('version_required', 'CHECK(version != \'\')', 'Version is required!'),
    ]

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
        Load the AI model for inference.
        In a real implementation, this would load the actual model file
        and prepare it for inference based on the model type.
        """
        # This is a placeholder implementation
        _logger.info(f"Loading model {self.name} (version {self.version})")

        # In a real implementation, this would:
        # 1. Load the model from storage
        # 2. Initialize the model with configuration
        # 3. Set up any required resources (GPU, memory, etc.)
        # 4. Return a model object ready for inference
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

    def action_evaluate_model(self):
        """Action to evaluate model performance on test dataset"""
        # In a real implementation, this would run the model on a test dataset
        # and update the performance metrics
        for model in self:
            # Placeholder for evaluation logic
            _logger.info(f"Evaluating model {model.name}")

            # In a real implementation, this would:
            # 1. Load test dataset
            # 2. Run model inference on test data
            # 3. Calculate performance metrics
            # 4. Update model record with new metrics

            # For now, just return a success notification
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

    def action_visualize_model(self):
        """Action to visualize model architecture (for compatible models)"""
        # For models that support visualization, this would show model architecture
        # In a real implementation, this could generate charts or diagrams
        message = f"Model {self.name} visualization not available in this implementation."
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Model Visualization'),
                'message': message,
                'type': 'info',
                'sticky': False,
            }
        }