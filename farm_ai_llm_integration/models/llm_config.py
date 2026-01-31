# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class AgriAiLlmConfiguration(models.Model):
    """
    Configuration for LLM providers - implements the AI Configuration interface
    """
    _name = 'agri.ai.llm.configuration'
    _description = 'LLM Provider Configuration'
    # Use delegation inheritance to properly link to the base interface
    _inherits = {'agri.ai.configuration': 'ai_config_id'}

    # Foreign key to the base agri.ai.configuration
    ai_config_id = fields.Many2one('agri.ai.configuration', string='AI Configuration', required=True, ondelete='cascade', auto_join=True)

    # Provider-specific fields (in addition to inherited ai.configuration fields)
    provider = fields.Selection([
        ('openai', 'OpenAI'),
        ('anthropic', 'Anthropic'),
        ('google', 'Google'),
        ('huggingface', 'Hugging Face'),
        ('custom', 'Custom API'),
        ('ollama', 'Ollama'),
    ], string='LLM Provider', required=True)

    # Performance settings
    rate_limit_requests = fields.Integer('Rate Limit (requests/min)', default=60)
    rate_limit_period = fields.Integer('Rate Limit Period (seconds)', default=60)

    # Agricultural domain-specific settings
    use_agricultural_context = fields.Boolean('Use Agricultural Context', default=True,
        help="Apply agricultural domain knowledge to prompts")
    application_type = fields.Selection([
        ('general', 'General Agricultural Queries'),
        ('pest_disease', 'Pest and Disease Diagnosis'),
        ('crop_recommendation', 'Crop Recommendation'),
        ('market_prediction', 'Market Prediction'),
        ('resource_optimization', 'Resource Optimization'),
        ('risk_assessment', 'Risk Assessment'),
    ], string='Application Type', default='general')

    @api.constrains('is_default')
    def _check_only_one_default(self):
        """Ensure only one configuration is set as default"""
        active_defaults = self.search([('is_default', '=', True), ('is_active', '=', True)])
        if len(active_defaults) > 1:
            raise UserError("Only one LLM configuration can be set as default.")

    def test_connection(self):
        """
        Test the LLM service connection - implementation of abstract method from ai.configuration
        """
        try:
            # Try a simple test using agri.ai.llm.service
            llm_service = self.env['agri.ai.llm.service'].sudo().search([('config_id', '=', self.id)], limit=1)
            if llm_service:
                # Test with a simple prompt
                result = llm_service.call_llm("Say 'connection test' in one word", {})
                if result.get('success'):
                    _logger.info(f"LLM configuration {self.name} connection test successful")
                    return True
                else:
                    _logger.error(f"LLM configuration {self.name} connection test failed: {result.get('error')}")
                    return False
            else:
                # If no service exists, create a temporary one for testing
                service = self.env['agri.ai.llm.service'].sudo().create({
                    'name': f'Test Service for {self.name}',
                    'config_id': self.id,
                })
                result = service.call_llm("Say 'connection test' in one word", {})
                if result.get('success'):
                    _logger.info(f"LLM configuration {self.name} connection test successful")
                    # Clean up the test service
                    service.unlink()
                    return True
                else:
                    _logger.error(f"LLM configuration {self.name} connection test failed: {result.get('error')}")
                    # Clean up the test service
                    service.unlink()
                    return False
        except Exception as e:
            _logger.error(f"LLM configuration {self.name} connection test failed with exception: {str(e)}")
            return False

    def increment_request_stats(self, success=True):
        """Increment request statistics - implementation of method from ai.configuration"""
        # Call the parent implementation to maintain the base functionality
        super(LLMConfiguration, self).increment_request_stats(success=success)

    @api.model
    def get_active_default(self):
        """Get the active default LLM configuration"""
        return self.search([('is_default', '=', True), ('is_active', '=', True)], limit=1)

    def get_ai_provider_type(self):
        """
        Return the AI provider type for reflection/discovery purposes
        """
        return self.ai_provider or 'llm'