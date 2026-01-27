from odoo import models, fields, api, _
from odoo.exceptions import UserError
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

    def test_connection(self):
        """Test the AI service connection"""
        # Implementation would test the connection to the AI service
        return True


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
    ], string='Model Type', required=True)

    description = fields.Text('Description')
    version = fields.Char('Version', required=True)

    # Performance metrics
    accuracy = fields.Float('Accuracy (%)')
    precision = fields.Float('Precision (%)')
    recall = fields.Float('Recall (%)')

    last_trained = fields.Datetime('Last Trained')
    training_dataset = fields.Char('Training Dataset')

    is_active = fields.Boolean('Is Active', default=True)
    is_default = fields.Boolean('Is Default', default=False)

    def load_model(self):
        """Load the AI model for inference"""
        # Implementation would load the model
        pass