# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class LLMConfiguration(models.Model):
    """
    Configuration for LLM providers
    """
    _name = 'llm.configuration'
    _description = 'LLM Provider Configuration'

    name = fields.Char('Configuration Name', required=True)
    provider = fields.Selection([
        ('openai', 'OpenAI'),
        ('anthropic', 'Anthropic'),
        ('google', 'Google'),
        ('huggingface', 'Hugging Face'),
        ('custom', 'Custom API'),
        ('ollama', 'Ollama'),
    ], string='LLM Provider', required=True)

    api_key = fields.Char('API Key', help="API key for the LLM provider")
    api_base_url = fields.Char('API Base URL', help="Base URL for API requests")
    default_model = fields.Char('Default Model', help="Default model to use, e.g. gpt-4, claude-3-opus")
    temperature = fields.Float('Temperature', default=0.7, help="Controls randomness (0.0-1.0)")
    max_tokens = fields.Integer('Max Tokens', default=1024, help="Maximum tokens in response")
    timeout = fields.Integer('Timeout (seconds)', default=30, help="API call timeout")

    is_active = fields.Boolean('Is Active', default=True, help="Whether this configuration is active")
    is_default = fields.Boolean('Is Default', help="Only one configuration can be default")

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

    @api.model
    def get_active_default(self):
        """Get the active default LLM configuration"""
        return self.search([('is_default', '=', True), ('is_active', '=', True)], limit=1)