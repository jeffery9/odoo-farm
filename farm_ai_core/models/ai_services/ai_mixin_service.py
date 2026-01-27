# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
import json
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class AIBaseMixinService(models.AbstractModel):
    """
    AI Base Mixin Service - Provides core AI functionality
    """
    _name = 'ai.base.mixin.service'
    _description = 'AI Base Mixin Service'

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

    def get_active_ai_config(self):
        """Get the active AI configuration for this record - abstract method"""
        # Use reflection/self-discovery to find all models that extend ai.configuration

        # First, try to get the base ai.configuration if it exists
        try:
            base_config = self.env['ai.configuration'].sudo().search([('is_active', '=', True)], limit=1)
            if base_config:
                return base_config
        except KeyError:
            pass

        # Use reflection to find all models that might inherit or extend ai.configuration
        # Search through the Odoo registry for models that could be AI configurations
        all_models = list(self.env.registry.keys())

        # Filter for models that are likely AI configurations
        ai_config_models = []
        for model_name in all_models:
            try:
                model = self.env[model_name]
                # Check if this model could be an AI configuration implementation
                # Look for models that have the necessary fields (like ai_provider, is_active, etc.)
                if (hasattr(model, '_fields') and
                    'is_active' in model._fields and
                    'ai_provider' in model._fields and
                    model_name != 'ai.configuration'):  # Exclude the base model itself
                    ai_config_models.append(model_name)
            except:
                # Skip if there's an issue accessing the model
                continue

        # Try each discovered AI configuration model
        for model_name in ai_config_models:
            try:
                if model_name in self.env:
                    config = self.env[model_name].sudo().search([('is_active', '=', True)], limit=1)
                    if config:
                        return config
            except (KeyError, AttributeError):
                # Model or field doesn't exist or isn't accessible, continue to next
                continue

        return None

    def call_llm_service(self, prompt, context_data=None):
        """Generic method to call LLM service if available"""
        if not context_data:
            context_data = {}

        # Use reflection to find all service models that might implement AI services
        all_models = list(self.env.registry.keys())

        # Find models that could be AI service implementations (have call_llm method)
        ai_service_models = []
        for model_name in all_models:
            try:
                model = self.env[model_name]
                # Check if this model has a call_llm method (indicating it's an AI service)
                if (hasattr(model, 'call_llm') or
                    (hasattr(model, '_fields') and 'config_id' in model._fields)):
                    ai_service_models.append(model_name)
            except:
                # Skip if there's an issue accessing the model
                continue

        # Try each discovered AI service model
        for service_model in ai_service_models:
            try:
                if service_model in self.env:
                    service = self.env[service_model].sudo().search([], limit=1)
                    if service and hasattr(service, 'call_llm'):
                        result = service.call_llm(prompt, context_data)
                        return result
            except (KeyError, AttributeError):
                # Model or method doesn't exist or isn't accessible, continue to next
                continue

        # If no service is available, use reflection to find any AI configurations
        # that might exist to give a more informative error
        all_config_models = list(self.env.registry.keys())
        ai_config_models = []
        for model_name in all_config_models:
            try:
                model = self.env[model_name]
                if (hasattr(model, '_fields') and
                    'is_active' in model._fields and
                    'ai_provider' in model._fields and
                    model_name != 'ai.configuration'):
                    ai_config_models.append(model_name)
            except:
                continue

        # Try to find any active configuration
        for model_name in ai_config_models:
            try:
                if model_name in self.env:
                    config = self.env[model_name].sudo().search([
                        ('is_active', '=', True),
                        ('is_default', '=', True)
                    ], limit=1)
                    if config:
                        _logger.warning(f"No active service found but {model_name} configuration exists")
                        return {
                            'success': False,
                            'error': f'No active service available, but {model_name} configuration exists',
                            'response': None,
                            'config_available': bool(config)
                        }
            except (KeyError, AttributeError):
                continue

        _logger.warning("No active AI configuration found")
        return {
            'success': False,
            'error': 'No active AI configuration',
            'response': None
        }

    def call_ai_service(self, service_type, prompt, context_data=None, model_override=None):
        """
        Generic method to call any type of AI service (LLM, Vision, ML, etc.)

        Args:
            service_type (str): Type of AI service ('llm', 'vision', 'ml', etc.)
            prompt (str): The input to process
            context_data (dict): Additional context information
            model_override (str): Specific model to use instead of default

        Returns:
            dict: Response from the AI service
        """
        if not context_data:
            context_data = {}

        # Use reflection to discover all AI service models
        all_models = list(self.env.registry.keys())

        # Find service models based on the requested type
        target_service_model = None
        for model_name in all_models:
            if service_type.lower() in model_name.lower() and 'service' in model_name.lower():
                try:
                    model = self.env[model_name]
                    if hasattr(model, 'call_llm') or hasattr(model, f'call_{service_type}_service'):
                        target_service_model = model_name
                        break
                except:
                    continue

        # If direct service type model not found, look for any service that can handle the request
        if not target_service_model:
            for model_name in all_models:
                try:
                    model = self.env[model_name]
                    # Look for models that look like AI services
                    if ('service' in model_name.lower() and
                        (hasattr(model, 'call_llm') or hasattr(model, 'call_ai_service'))):
                        target_service_model = model_name
                        break
                except:
                    continue

        if target_service_model and target_service_model in self.env:
            try:
                service = self.env[target_service_model].sudo().search([], limit=1)
                if service:
                    # Try calling the appropriate method based on service type
                    if hasattr(service, f'call_{service_type}_service'):
                        call_method = getattr(service, f'call_{service_type}_service')
                        return call_method(prompt, context_data, model_override)
                    elif hasattr(service, 'call_llm') and service_type.lower() == 'llm':
                        return service.call_llm(prompt, context_data)
                    elif hasattr(service, 'call_ai_service'):
                        return service.call_ai_service(service_type, prompt, context_data, model_override)
                    else:
                        # Try the generic call method if available
                        return service.call_llm(prompt, context_data)
            except (KeyError, AttributeError):
                pass

        # If no specific service found, return error
        return {
            'success': False,
            'error': f'No {service_type} service available',
            'response': None
        }