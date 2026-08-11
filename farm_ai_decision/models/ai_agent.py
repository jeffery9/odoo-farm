# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
import json
from datetime import datetime, timedelta
import random
import uuid

_logger = logging.getLogger(__name__)

class AgriAiAgent(models.Model):
    """
    AI Agent model for intelligent decision support.
    Refactored to Agri domain with 100% logic retention.
    """
    _name = 'agri.ai.agent'
    _description = 'AI Agent for Intelligent Decision Support'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'agri.ai.base.mixin']
    _inherits = {
        'agri.ai.decision.base': 'base_id',
    }

    base_id = fields.Many2one('agri.ai.decision.base', required=True, ondelete="cascade",
                              help="Base AI decision support record")

    agent_type = fields.Selection([
        ('recommendation', 'Recommendation Agent'),
        ('analysis', 'Analysis Agent'),
        ('optimization', 'Optimization Agent'),
        ('prediction', 'Prediction Agent'),
        ('monitoring', 'Monitoring Agent'),
        ('classification', 'Classification Agent'),
        ('planning', 'Planning Agent'),
    ], string='Agent Type', required=True, default='recommendation')

    industry_id = fields.Char(string='Industry Type',
                                  help="Industry to which this AI agent applies")

    model_architecture = fields.Selection([
        ('random_forest', 'Random Forest'),
        ('neural_network', 'Neural Network'),
        ('svm', 'Support Vector Machine'),
        ('gradient_boosting', 'Gradient Boosting'),
        ('deep_learning', 'Deep Learning'),
        ('ensemble', 'Ensemble Method'),
        ('rule_based', 'Rule-based System'),
    ], string='Model Architecture', default='random_forest')

    training_data_source = fields.Char('Training Data Source',
                                       help="Source or dataset used for training")
    training_accuracy = fields.Float('Training Accuracy',
                                     help="Accuracy score from model training")
    last_trained = fields.Datetime('Last Trained',
                                   help="When the model was last retrained")
    training_samples = fields.Integer('Training Samples Count',
                                      help="Number of samples used in training")

    # Configuration parameters
    parameters = fields.Text('Model Parameters',
                             help="JSON configuration for the AI model")

    # Performance metrics
    precision_score = fields.Float('Precision Score',
                                   help="Precision score for classification tasks")
    recall_score = fields.Float('Recall Score',
                                help="Recall score for classification tasks")
    f1_score = fields.Float('F1 Score',
                            help="F1 score for classification tasks")
    mse_score = fields.Float('MSE Score',
                             help="Mean Squared Error for regression tasks")

    # Input/Output schema
    input_schema = fields.Text('Input Schema',
                               help="JSON schema defining expected input data")
    output_schema = fields.Text('Output Schema',
                                help="JSON schema defining expected output format")

    # Execution tracking
    execution_count = fields.Integer('Execution Count', default=0,
                                     help="Number of times agent has been executed")
    last_execution = fields.Datetime('Last Execution',
                                     help="When the agent was last executed")
    avg_response_time = fields.Float('Avg. Response Time (ms)',
                                     help="Average response time in milliseconds")

    # ISL-specific fields
    uses_isl_data = fields.Boolean('Uses ISL Data', default=False,
                                   help="Whether this agent accesses ISL models")
    isl_model_access = fields.Text('ISL Model Access',
                                   help="List of ISL models this agent can access")
    data_isolation_level = fields.Selection([
        ('none', 'No Isolation'),
        ('industry', 'Industry Level'),
        ('entity', 'Entity Level'),
        ('user', 'User Level'),
    ], string='Data Isolation Level', default='industry',
    help="Level of data isolation for the AI agent")

    def action_execute_agent(self, input_data=None):
        """Execute the AI agent with given input data"""
        for agent in self:
            # Update execution statistics
            agent.execution_count += 1
            agent.last_execution = fields.Datetime.now()

            # Process the input data through the AI model
            result = self._execute_model(agent, input_data or {})

            # Calculate response time
            if agent.last_execution:
                # This is a placeholder - actual response time would be calculated during execution
                agent.avg_response_time = random.uniform(50, 500)  # Simulate response time

            # Update base model with results
            agent.base_id.output_data = json.dumps(result)
            agent.base_id.status = 'recommended'

    def _execute_model(self, agent, input_data):
        """Execute the specific AI model based on agent type"""
        # Check if LLM integration is available
        llm_service = self.env['agri.ai.llm.service'].search([('config_id.is_active', '=', True),
                                                              ('config_id.is_default', '=', True)], limit=1)

        if llm_service:
            # Use LLM to generate more sophisticated responses
            return self._execute_with_llm(llm_service, agent, input_data)
        else:
            # Fallback to traditional methods if no LLM configured
            return self._execute_with_traditional_methods(agent, input_data)

    def _execute_with_llm(self, llm_service, agent, input_data):
        """Execute using LLM service for more sophisticated responses"""
        # Prepare context based on agent type
        context_data = {
            'agent_type': agent.agent_type,
            'model_architecture': agent.model_architecture,
            'industry': agent.industry_id.name if agent.industry_id else 'General Agriculture',
            'input_data': input_data,
        }

        # Create appropriate prompt based on agent type
        prompt_templates = llm_service.get_agricultural_prompt_templates()

        if agent.agent_type == 'recommendation':
            prompt = prompt_templates['crop_recommendation'].format(
                soil_type=input_data.get('soil_type', 'not specified'),
                climate=input_data.get('climate', 'not specified'),
                season=input_data.get('season', 'not specified'),
                previous_crops=input_data.get('previous_crops', 'not specified')
            )
        elif agent.agent_type == 'analysis':
            prompt = f"Analyze this agricultural data: {json.dumps(input_data)}. Identify trends, patterns, and insights."
        elif agent.agent_type == 'optimization':
            prompt = prompt_templates['resource_optimization'].format(
                crop_type=input_data.get('crop_type', 'various crops')
            )
        elif agent.agent_type == 'prediction':
            prompt = prompt_templates['yield_prediction'].format(
                crop_type=input_data.get('crop_type', 'unknown'),
                planting_date=input_data.get('planting_date', 'not specified'),
                variety=input_data.get('variety', 'not specified'),
                field_size=input_data.get('field_size', 'not specified'),
                weather=input_data.get('weather', 'not specified'),
                pest_pressure=input_data.get('pest_pressure', 'not specified')
            )
        elif agent.agent_type == 'monitoring':
            prompt = f"Monitor these agricultural metrics: {json.dumps(input_data)}. Identify any concerning patterns or anomalies."
        elif agent.agent_type == 'classification':
            prompt = f"Classify this agricultural observation: {json.dumps(input_data)}. Determine the category or type."
        elif agent.agent_type == 'planning':
            prompt = f"Create a plan based on these requirements: {json.dumps(input_data)}. Include timeline and resource allocation."
        else:
            prompt = f"Process this agricultural data: {json.dumps(input_data)}. Provide recommendations and analysis."

        # Call the LLM
        llm_result = llm_service.call_llm(prompt, context_data)

        if llm_result['success']:
            # Parse and structure the LLM response
            response_text = llm_result['response']
            return self._parse_llm_response(agent, response_text, input_data, llm_result)
        else:
            # Fallback to traditional methods if LLM fails
            _logger.warning(f"LLM call failed: {llm_result['error']}. Falling back to traditional methods.")
            return self._execute_with_traditional_methods(agent, input_data)

    def _parse_llm_response(self, agent, llm_response, input_data, llm_result):
        """Parse the LLM response into structured format"""
        import re

        # This is a simplified parser - in a real implementation, you might want to use
        # JSON responses from the LLM or more sophisticated parsing
        result = {
            'input_data': input_data,
            'model_type': agent.model_architecture,
            'timestamp': fields.Datetime.now().isoformat(),
            'session_id': str(uuid.uuid4()),
            'llm_response': llm_response,
            'model_used': llm_result.get('model_used', 'unknown'),
            'raw_llm_result': llm_result
        }

        # Extract recommendations if present
        if agent.agent_type == 'recommendation':
            # Look for recommendations in the response
            if 'recommendation' in llm_response.lower() or 'suggest' in llm_response.lower():
                result['recommendations'] = [llm_response]  # In a real implementation, parse out specific recommendations

        # Extract predictions if present
        elif agent.agent_type == 'prediction':
            # Look for values that might be predictions
            numbers = re.findall(r'\d+\.?\d*', llm_response)
            if numbers:
                # Assume the first number found is a predicted value
                try:
                    result['predictions'] = {'predicted_value': float(numbers[0])}
                except ValueError:
                    pass

        # Generate confidence based on response quality
        result['confidence'] = self._calculate_llm_confidence(agent, llm_response)

        # Generate reasoning explanation
        result['reasoning'] = self._generate_reasoning(agent, input_data, result)

        return result

    def _calculate_llm_confidence(self, agent, llm_response):
        """Calculate confidence score for LLM response"""
        # This is a simple heuristic - in practice, you might get confidence from the LLM itself
        # or use more sophisticated methods
        base_confidence = 0.85  # LLM responses generally have good quality

        # Adjust based on response length and structure
        if len(llm_response) < 50:
            base_confidence -= 0.2  # Short responses may be less detailed
        elif len(llm_response) > 500:
            base_confidence += 0.05  # Longer responses may be more comprehensive

        # Ensure confidence stays within bounds
        return max(0.5, min(0.95, base_confidence))

    def _execute_with_traditional_methods(self, agent, input_data):
        """Execute using traditional methods (existing implementation)"""
        result = {
            'input_data': input_data,
            'model_type': agent.model_architecture,
            'timestamp': fields.Datetime.now().isoformat(),
            'session_id': str(uuid.uuid4()),
        }

        # Different logic based on agent type
        if agent.agent_type == 'recommendation':
            result['recommendations'] = self._generate_recommendations(agent, input_data)
        elif agent.agent_type == 'analysis':
            result['analysis'] = self._perform_analysis(agent, input_data)
        elif agent.agent_type == 'optimization':
            result['optimization'] = self._perform_optimization(agent, input_data)
        elif agent.agent_type == 'prediction':
            result['predictions'] = self._make_predictions(agent, input_data)
        elif agent.agent_type == 'monitoring':
            result['monitoring'] = self._perform_monitoring(agent, input_data)
        elif agent.agent_type == 'classification':
            result['classification'] = self._perform_classification(agent, input_data)
        elif agent.agent_type == 'planning':
            result['planning'] = self._perform_planning(agent, input_data)

        # Calculate confidence score
        result['confidence'] = self._calculate_confidence(agent, input_data)

        # Generate reasoning explanation
        result['reasoning'] = self._generate_reasoning(agent, input_data, result)

        return result

    def _generate_recommendations(self, agent, input_data):
        """Generate recommendations based on input data"""
        recommendations = []

        # Example: Generate recommendations based on industry and input parameters
        if agent.industry_id:
            if 'crop' in agent.industry_id.name.lower():
                recommendations.append("Optimize irrigation schedule based on weather forecast")
                recommendations.append("Apply fertilizer based on soil nutrient analysis")
                recommendations.append("Monitor for pest outbreaks during critical growth periods")

        if 'yield' in input_data.get('metrics', []):
            if input_data.get('yield_deviation', 0) < -0.1:  # 10% below expected
                recommendations.append("Investigate causes of yield underperformance")

        if 'cost' in input_data.get('metrics', []):
            if input_data.get('cost_efficiency', 1.0) < 0.8:  # Below 80% efficiency
                recommendations.append("Optimize resource allocation to improve cost efficiency")

        return recommendations

    def _perform_analysis(self, agent, input_data):
        """Perform data analysis"""
        analysis = {
            'trends': [],
            'patterns': [],
            'anomalies': [],
            'correlations': []
        }

        # Example: Analyze time series data
        if 'time_series' in input_data:
            # Look for trends in the data
            analysis['trends'].append("Positive trend detected in yield data over last 30 days")
            analysis['patterns'].append("Seasonal pattern identified in resource consumption")
            analysis['anomalies'].append("Anomalous weather pattern detected for this time of year")

        # Example: Analyze categorical data
        if 'categories' in input_data:
            analysis['correlations'].append("Correlation found between fertilizer type and yield")

        return analysis

    def _perform_optimization(self, agent, input_data):
        """Perform optimization calculations"""
        optimization = {
            'optimal_values': {},
            'constraints': [],
            'objective_function': 'maximize_profit',
            'solution_confidence': 0.0
        }

        # Example: Resource allocation optimization
        if 'resources' in input_data:
            optimization['optimal_values'] = {
                'labor_hours': input_data.get('available_labor', 100) * 0.7,  # Use 70% of labor
                'fertilizer_kg': input_data.get('field_size', 1) * 50,  # 50kg per hectare
                'water_liters': input_data.get('field_size', 1) * 10000  # 10kl per hectare
            }

        if 'constraints' in input_data:
            optimization['constraints'] = input_data['constraints']

        optimization['solution_confidence'] = max(0.7, min(0.95, 0.8 + random.uniform(-0.1, 0.1)))

        return optimization

    def _make_predictions(self, agent, input_data):
        """Make predictions based on input data"""
        predictions = {
            'forecast': {},
            'confidence_intervals': {},
            'trend_direction': 'stable'
        }

        # Example: Predict future yield
        if 'historical_yield' in input_data:
            historical = input_data['historical_yield']
            if historical:
                avg_yield = sum(historical) / len(historical)
                trend = random.uniform(-0.05, 0.1)  # -5% to +10% trend
                predictions['forecast']['next_period_yield'] = avg_yield * (1 + trend)
                predictions['confidence_intervals']['yield'] = [
                    avg_yield * (1 + trend - 0.05),  # Lower bound
                    avg_yield * (1 + trend + 0.05)   # Upper bound
                ]

        # Example: Predict market prices
        if 'market_data' in input_data:
            predictions['forecast']['price_trend'] = random.choice(['increasing', 'decreasing', 'stable'])
            predictions['forecast']['estimated_price'] = random.uniform(1.0, 5.0)

        return predictions

    def _perform_monitoring(self, agent, input_data):
        """Perform monitoring and alerting"""
        monitoring = {
            'alerts': [],
            'status': 'normal',
            'metrics': {},
            'thresholds': {}
        }

        # Example: Monitor key metrics
        if 'temperature' in input_data:
            temp = input_data['temperature']
            if temp > 35:
                monitoring['alerts'].append("High temperature alert: Crop stress risk")
                monitoring['status'] = 'warning'
            elif temp < 5:
                monitoring['alerts'].append("Frost alert: Crop protection needed")
                monitoring['status'] = 'warning'

        if 'moisture' in input_data:
            moisture = input_data['moisture']
            if moisture < 20:
                monitoring['alerts'].append("Drought conditions detected: Irrigation required")
                monitoring['status'] = 'warning'

        monitoring['metrics'] = input_data
        monitoring['thresholds'] = {
            'temperature_high': 35,
            'temperature_low': 5,
            'moisture_low': 20
        }

        return monitoring

    def _perform_classification(self, agent, input_data):
        """Perform classification tasks"""
        classification = {
            'predicted_class': 'normal',
            'class_probabilities': {},
            'confidence_by_class': {}
        }

        # Example: Classify crop health status
        if 'health_indicators' in input_data:
            indicators = input_data['health_indicators']
            if indicators.get('leaf_color', 0.5) < 0.3:  # Pale leaves
                classification['predicted_class'] = 'nutrient_deficiency'
            elif indicators.get('pest_damage', 0) > 0.4:  # Significant damage
                classification['predicted_class'] = 'pest_infestation'
            elif indicators.get('disease_symptoms', 0) > 0.3:  # Disease symptoms
                classification['predicted_class'] = 'disease'
            else:
                classification['predicted_class'] = 'healthy'

        # Assign probabilities to each class
        classification['class_probabilities'] = {
            'healthy': random.uniform(0.6, 0.9),
            'nutrient_deficiency': random.uniform(0.05, 0.2),
            'pest_infestation': random.uniform(0.05, 0.15),
            'disease': random.uniform(0.05, 0.15)
        }

        return classification

    def _perform_planning(self, agent, input_data):
        """Perform planning and scheduling"""
        planning = {
            'schedule': [],
            'resource_allocation': {},
            'constraints_met': True,
            'optimization_score': 0.0
        }

        # Example: Generate work schedule
        if 'tasks' in input_data:
            for i, task in enumerate(input_data['tasks'][:5]):  # Limit to 5 tasks for example
                planning['schedule'].append({
                    'task': task.get('name', f'Task {i+1}'),
                    'start_date': fields.Date.context_today(self).strftime('%Y-%m-%d'),
                    'end_date': fields.Date.add(fields.Date.context_today(self),
                                                days=task.get('duration', 3)).strftime('%Y-%m-%d'),
                    'resources': task.get('required_resources', []),
                    'priority': task.get('priority', 'medium')
                })

        # Example: Resource allocation
        if 'resources' in input_data:
            planning['resource_allocation'] = {
                'labor': input_data['resources'].get('labor', 10),
                'equipment': input_data['resources'].get('equipment', 2),
                'materials': input_data['resources'].get('materials', {})
            }

        planning['optimization_score'] = max(0.7, min(0.95, 0.8 + random.uniform(-0.1, 0.1)))

        return planning

    def _calculate_confidence(self, agent, input_data):
        """Calculate confidence in the AI model's output"""
        # Base confidence from training
        base_confidence = agent.training_accuracy or 0.75

        # Data quality factor
        data_quality = len(input_data) / 10.0  # More data = higher confidence, up to 1.0
        data_quality = min(1.0, data_quality)

        # Feature completeness factor
        required_features = ['timestamp', 'location', 'crop_type']  # Example
        present_features = [f for f in required_features if f in input_data]
        completeness_factor = len(present_features) / len(required_features)

        # Combine factors
        final_confidence = (base_confidence * 0.5 +
                          data_quality * 0.3 +
                          completeness_factor * 0.2)

        return max(0.5, final_confidence)  # Minimum confidence of 50%

    def _generate_reasoning(self, agent, input_data, result):
        """Generate human-readable explanation of AI decision process"""
        reasoning_steps = [
            f"1. Input data received: {len(input_data)} features identified",
            f"2. Model type '{agent.model_architecture}' selected for '{agent.agent_type}' task",
            f"3. Industry context: {agent.industry_id.name if agent.industry_id else 'General'}",
            f"4. Analysis performed using {agent.training_samples or 0} training samples",
            f"5. Confidence score calculated: {result.get('confidence', 0):.2%}",
        ]

        if agent.agent_type == 'recommendation':
            reasoning_steps.append("6. Recommendations generated based on best practices and historical data")
        elif agent.agent_type == 'prediction':
            reasoning_steps.append("7. Predictions made using time series analysis and trend modeling")

        return "<br/>".join(reasoning_steps)

    def action_apply_recommendation(self):
        """Delegate recommendation application to the base record"""
        for agent in self:
            if agent.base_id:
                agent.base_id.action_apply_recommendation()
        return True

    def action_train_model(self):
        """Train the AI model with new data"""
        for agent in self:
            # Simulate model training process
            training_data = self._prepare_training_data(agent)

            # In a real implementation, this would call actual ML training
            # For now, we'll simulate the training process
            agent.training_samples = len(training_data)
            agent.training_accuracy = random.uniform(0.75, 0.95)
            agent.last_trained = fields.Datetime.now()

            # Update model parameters based on training
            new_params = {
                'learning_rate': random.uniform(0.001, 0.1),
                'epochs': random.randint(50, 200),
                'batch_size': random.randint(16, 64),
                'validation_split': 0.2
            }
            agent.parameters = json.dumps(new_params)

    def _prepare_training_data(self, agent):
        """Prepare training data for model retraining"""
        # In a real implementation, this would gather relevant training data
        # from historical decisions, feedback, and other sources
        # For now, we'll simulate data preparation
        return list(range(100 + random.randint(0, 50)))  # Simulated training samples
