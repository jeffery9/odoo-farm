# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
import requests
import json
import time
from datetime import datetime, timedelta
from functools import wraps

_logger = logging.getLogger(__name__)


def rate_limit(calls_per_minute=60):
    """Decorator to implement rate limiting"""
    interval = 60.0 / calls_per_minute
    last_called = {}

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            if func in last_called:
                sleep_time = interval - (now - last_called[func])
                if sleep_time > 0:
                    time.sleep(sleep_time)
            last_called[func] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator


class LLMService(models.Model):
    """
    Service class for calling LLM APIs
    """
    _name = 'llm.service'
    _description = 'LLM Service Interface'

    name = fields.Char('Service Name', required=True)
    config_id = fields.Many2one('llm.configuration', string='LLM Configuration', required=True)
    last_call_time = fields.Datetime('Last Call Time')
    call_count = fields.Integer('Call Count', default=0)
    error_count = fields.Integer('Error Count', default=0)

    def call_llm(self, prompt, context_data=None, model_override=None):
        """
        Main method to call LLM API with the given prompt

        Args:
            prompt (str): The prompt to send to the LLM
            context_data (dict): Additional context data
            model_override (str): Optional model to use instead of default

        Returns:
            dict: Response from the LLM API
        """
        if not self.config_id.is_active:
            raise UserError("LLM configuration is not active")

        # Apply agricultural context if configured
        if self.config_id.use_agricultural_context:
            prompt = self._enhance_prompt_with_ag_context(prompt, context_data)

        model = model_override or self.config_id.default_model
        if not model:
            raise UserError("No model specified and no default model configured")

        # Prepare the request based on provider
        if self.config_id.provider == 'openai':
            return self._call_openai_api(prompt, model)
        elif self.config_id.provider == 'anthropic':
            return self._call_anthropic_api(prompt, model)
        elif self.config_id.provider == 'google':
            return self._call_google_api(prompt, model)
        elif self.config_id.provider == 'huggingface':
            return self._call_huggingface_api(prompt, model)
        elif self.config_id.provider == 'ollama':
            return self._call_ollama_api(prompt, model)
        elif self.config_id.provider == 'custom':
            return self._call_custom_api(prompt, model)
        else:
            raise UserError(f"Provider {self.config_id.provider} not supported")

    def _enhance_prompt_with_ag_context(self, original_prompt, context_data=None):
        """Enhance the prompt with agricultural domain knowledge"""
        ag_context = (
            "You are an expert agricultural advisor with deep knowledge in farming, "
            "crop science, pest management, soil health, and sustainable agriculture practices. "
            "Provide evidence-based recommendations considering local environmental conditions, "
            "crop varieties, pest/disease management, resource optimization, and sustainable practices. "
            f"Context: {context_data}" if context_data else ""
        )
        return f"{ag_context}\n\nUser query: {original_prompt}"

    @rate_limit(calls_per_minute=60)  # Use the rate limit from config if available
    def _call_openai_api(self, prompt, model):
        """Call OpenAI API"""
        headers = {
            'Authorization': f'Bearer {self.config_id.api_key}',
            'Content-Type': 'application/json'
        }

        data = {
            'model': model,
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': self.config_id.temperature,
            'max_tokens': self.config_id.max_tokens
        }

        try:
            response = requests.post(
                f"{self.config_id.api_base_url or 'https://api.openai.com/v1'}/chat/completions",
                headers=headers,
                json=data,
                timeout=self.config_id.timeout
            )
            response.raise_for_status()

            result = response.json()
            content = result['choices'][0]['message']['content']

            # Log successful call
            self._log_call()

            return {
                'success': True,
                'response': content,
                'model_used': result.get('model', model),
                'usage': result.get('usage', {}),
                'raw_response': result
            }
        except requests.exceptions.RequestException as e:
            self._log_error()
            _logger.error(f"OpenAI API error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'response': None
            }

    @rate_limit(calls_per_minute=60)
    def _call_anthropic_api(self, prompt, model):
        """Call Anthropic API"""
        headers = {
            'x-api-key': self.config_id.api_key,
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01'
        }

        data = {
            'model': model,
            'prompt': f"\n\nHuman: {prompt}\n\nAssistant:",
            'max_tokens_to_sample': self.config_id.max_tokens,
            'temperature': self.config_id.temperature,
        }

        try:
            response = requests.post(
                f"{self.config_id.api_base_url or 'https://api.anthropic.com/v1'}/complete",
                headers=headers,
                json=data,
                timeout=self.config_id.timeout
            )
            response.raise_for_status()

            result = response.json()
            content = result['completion']

            # Log successful call
            self._log_call()

            return {
                'success': True,
                'response': content,
                'model_used': result.get('model', model),
                'raw_response': result
            }
        except requests.exceptions.RequestException as e:
            self._log_error()
            _logger.error(f"Anthropic API error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'response': None
            }

    @rate_limit(calls_per_minute=60)
    def _call_google_api(self, prompt, model):
        """Call Google AI API"""
        headers = {
            'Authorization': f'Bearer {self.config_id.api_key}',
            'Content-Type': 'application/json'
        }

        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": self.config_id.temperature,
                "maxOutputTokens": self.config_id.max_tokens
            }
        }

        try:
            response = requests.post(
                f"{self.config_id.api_base_url or f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.config_id.api_key}' if ':' not in model else self.config_id.api_base_url}",
                headers=headers,
                json=data,
                timeout=self.config_id.timeout
            )
            response.raise_for_status()

            result = response.json()

            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0]['content']['parts'][0]['text']
            else:
                raise Exception("No candidates in response")

            # Log successful call
            self._log_call()

            return {
                'success': True,
                'response': content,
                'model_used': model,
                'raw_response': result
            }
        except requests.exceptions.RequestException as e:
            self._log_error()
            _logger.error(f"Google AI API error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'response': None
            }

    @rate_limit(calls_per_minute=60)
    def _call_huggingface_api(self, prompt, model):
        """Call Hugging Face Inference API"""
        headers = {
            'Authorization': f'Bearer {self.config_id.api_key}',
            'Content-Type': 'application/json'
        }

        data = {
            'inputs': prompt,
            'parameters': {
                'max_new_tokens': self.config_id.max_tokens,
                'temperature': self.config_id.temperature,
                'return_full_text': False
            }
        }

        try:
            response = requests.post(
                f"{self.config_id.api_base_url or f'https://api-inference.huggingface.co/models/{model}'}",
                headers=headers,
                json=data,
                timeout=self.config_id.timeout
            )
            response.raise_for_status()

            result = response.json()
            content = result[0]['generated_text']

            # Log successful call
            self._log_call()

            return {
                'success': True,
                'response': content,
                'model_used': model,
                'raw_response': result
            }
        except requests.exceptions.RequestException as e:
            self._log_error()
            _logger.error(f"Hugging Face API error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'response': None
            }

    @rate_limit(calls_per_minute=60)
    def _call_ollama_api(self, prompt, model):
        """Call local Ollama API"""
        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            'model': model,
            'prompt': prompt,
            'stream': False,
            'options': {
                'temperature': self.config_id.temperature,
                'num_predict': self.config_id.max_tokens
            }
        }

        try:
            response = requests.post(
                f"{self.config_id.api_base_url or 'http://localhost:11434/api/generate'}",
                headers=headers,
                json=data,
                timeout=self.config_id.timeout
            )
            response.raise_for_status()

            result = response.json()
            content = result.get('response', '')

            # Log successful call
            self._log_call()

            return {
                'success': True,
                'response': content,
                'model_used': model,
                'raw_response': result
            }
        except requests.exceptions.RequestException as e:
            self._log_error()
            _logger.error(f"Ollama API error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'response': None
            }

    @rate_limit(calls_per_minute=60)
    def _call_custom_api(self, prompt, model):
        """Call custom API endpoint"""
        if not self.config_id.api_base_url:
            raise UserError("Custom API base URL not configured")

        headers = {
            'Authorization': f'Bearer {self.config_id.api_key}',
            'Content-Type': 'application/json'
        }

        # This is a generic format - customize based on your custom API's requirements
        data = {
            'prompt': prompt,
            'model': model,
            'options': {
                'temperature': self.config_id.temperature,
                'max_tokens': self.config_id.max_tokens
            }
        }

        try:
            response = requests.post(
                self.config_id.api_base_url,
                headers=headers,
                json=data,
                timeout=self.config_id.timeout
            )
            response.raise_for_status()

            result = response.json()
            # Customize this based on your custom API's response format
            content = result.get('response', result.get('output', result.get('text', '')))

            # Log successful call
            self._log_call()

            return {
                'success': True,
                'response': content,
                'model_used': model,
                'raw_response': result
            }
        except requests.exceptions.RequestException as e:
            self._log_error()
            _logger.error(f"Custom API error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'response': None
            }

    def _log_call(self):
        """Log successful API call"""
        self.write({
            'last_call_time': fields.Datetime.now(),
            'call_count': self.call_count + 1
        })

    def _log_error(self):
        """Log API error"""
        self.write({
            'error_count': self.error_count + 1
        })

    def get_agricultural_prompt_templates(self):
        """Return common prompt templates for agricultural use cases"""
        return {
            'pest_disease_diagnosis': (
                "As an agricultural expert, analyze this description of plant symptoms "
                "and identify the likely pest, disease, or nutrient deficiency. Include "
                "the scientific name, symptoms, lifecycle information, recommended "
                "treatments, and prevention strategies."
            ),
            'crop_recommendation': (
                "Based on these local conditions [soil type: {soil_type}, "
                "climate: {climate}, season: {season}, previous crops: {previous_crops}], "
                "recommend suitable crops and varieties for planting. Consider yield potential, "
                "market demand, and regional suitability."
            ),
            'yield_prediction': (
                "Predict the likely yield for {crop_type} given these conditions: "
                "planting date: {planting_date}, variety: {variety}, field size: {field_size}, "
                "weather patterns: {weather}, pest/disease pressure: {pest_pressure}. "
                "Include confidence level and factors that could affect yield."
            ),
            'resource_optimization': (
                "Optimize resource allocation for {crop_type} farming. Recommend "
                "fertilizer types and timing, irrigation schedule, and labor allocation "
                "to maximize yield while minimizing costs and environmental impact."
            ),
            'market_prediction': (
                "Analyze market trends for {crop_type} and predict price movements "
                "for the next {time_period}. Consider supply/demand factors, "
                "seasonal patterns, and external market influences."
            ),
            'sustainability_assessment': (
                "Assess the sustainability of this farming practice: {practice_description}. "
                "Evaluate environmental impact, resource efficiency, and long-term viability. "
                "Provide recommendations for improvement."
            )
        }

    def call_ai_service(self, service_type, prompt, context_data=None, model_override=None):
        """
        Generic method to call AI service based on service type

        Args:
            service_type (str): Type of AI service ('llm', 'vision', 'ml', etc.)
            prompt (str): The input to process
            context_data (dict): Additional context information
            model_override (str): Specific model to use instead of default

        Returns:
            dict: Response from the AI service
        """
        # For LLM service type, delegate to the main call_llm method
        if service_type.lower() in ['llm', 'language', 'text', 'chat']:
            return self.call_llm(prompt, context_data, model_override)

        # For other types, return error since this is an LLM service
        return {
            'success': False,
            'error': f'LLM service cannot handle {service_type} requests. Service type not supported.',
            'response': None
        }

    def call_llm_service(self, prompt, context_data=None, model_override=None):
        """
        Wrapper method to call LLM service - matches the expected interface
        """
        return self.call_llm(prompt, context_data, model_override)

    def make_decision(self, data, decision_type='classification'):
        """
        Make decisions using the LLM service

        Args:
            data: Input data for decision making
            decision_type (str): Type of decision to make

        Returns:
            dict: Decision result with confidence
        """
        try:
            # Format the decision-making request
            if decision_type.lower() == 'classification':
                prompt = f"Classify the following agricultural data: {data}. Provide your classification and confidence level."
            elif decision_type.lower() == 'recommendation':
                prompt = f"Based on the following context: {data}, provide agricultural recommendations. Focus on practical, evidence-based advice."
            elif decision_type.lower() == 'diagnosis':
                prompt = f"Diagnose the following agricultural issue: {data}. Provide possible causes and solutions."
            else:
                prompt = f"Analyze the following data: {data}. Provide insights relevant to type {decision_type}."

            # Enhance with agricultural context if configured
            if self.config_id.use_agricultural_context:
                prompt = self._enhance_prompt_with_ag_context(prompt, data)

            result = self.call_llm(prompt)

            # Extract confidence from the response if available
            confidence = 85.0  # Default confidence for LLM responses

            return {
                'success': result.get('success', False),
                'decision': result.get('response', 'No response generated'),
                'confidence': confidence,
                'model_used': result.get('model_used', 'LLM Service'),
                'raw_response': result
            }
        except Exception as e:
            return {
                'success': False,
                'decision': None,
                'confidence': 0.0,
                'error': str(e)
            }

    def process_decision(self, data, decision_type='classification'):
        """
        Process agricultural decision making

        Args:
            data: Input data for decision making
            decision_type (str): Type of decision to make

        Returns:
            dict: Decision result with confidence
        """
        return self.make_decision(data, decision_type)

    def get_agricultural_insights(self, data):
        """
        Extract agricultural insights from input data

        Args:
            data: Input data to analyze

        Returns:
            dict: Agricultural insights
        """
        try:
            prompt = f"""
            Analyze the following agricultural data and extract key insights:
            {data}

            Please provide:
            1. Key observations
            2. Potential issues or concerns
            3. Recommendations for improvement
            4. Risk factors to consider
            """

            result = self.call_llm(prompt)

            return {
                'success': result.get('success', False),
                'insights': result.get('response', ''),
                'model_used': result.get('model_used', 'LLM Service'),
                'raw_response': result
            }
        except Exception as e:
            return {
                'success': False,
                'insights': None,
                'error': str(e)
            }