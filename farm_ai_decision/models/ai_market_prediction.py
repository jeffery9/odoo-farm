# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
import json
from datetime import datetime, timedelta
import random

_logger = logging.getLogger(__name__)

class AIMarketPrediction(models.Model):
    """
    AI model for market price prediction
    Implements US-58-08: Agri-market intelligent prediction
    """
    _name = 'ai.market.prediction'
    _description = 'AI Market Prediction'
    _inherit = ['ai.decision.base']

    product_id = fields.Many2one('product.template', string='Product')
    current_price = fields.Float('Current Price')
    predicted_price_7d = fields.Float('Predicted Price (7 days)')
    predicted_price_30d = fields.Float('Predicted Price (30 days)')
    predicted_price_90d = fields.Float('Predicted Price (90 days)')
    price_trend = fields.Selection([
        ('up', 'Up'),
        ('down', 'Down'),
        ('stable', 'Stable'),
        ('volatile', 'Volatile'),
    ], string='Price Trend')
    market_factors = fields.Text('Market Factors Analysis')
    sales_strategy = fields.Html('Sales Strategy')
    optimal_sales_timing = fields.Html('Optimal Sales Timing')
    risk_level = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Risk Level', default='medium')

    def calculate_market_prediction(self):
        """Calculate market price predictions"""
        for record in self:
            if record.current_price:
                # Simulate price prediction algorithm
                base_change = random.uniform(-0.15, 0.20)  # -15% to +20%

                # Adjust based on historical patterns
                if record.product_id:
                    if 'tomato' in record.product_id.name.lower():
                        # Tomato prices often peak in winter
                        seasonal_factor = 1.0 + (0.15 if datetime.now().month in [12, 1, 2, 11] else -0.05)
                    elif 'wheat' in record.product_id.name.lower():
                        # Wheat prices may peak during harvest season
                        seasonal_factor = 1.0 + (0.10 if datetime.now().month in [6, 7, 8] else -0.05)
                    else:
                        seasonal_factor = 1.0

                # Calculate predictions
                record.predicted_price_7d = record.current_price * (1 + base_change * 0.2) * seasonal_factor
                record.predicted_price_30d = record.current_price * (1 + base_change * 0.6) * seasonal_factor
                record.predicted_price_90d = record.current_price * (1 + base_change) * seasonal_factor

                # Determine trend
                if base_change > 0.10:
                    record.price_trend = 'up'
                    record.priority = 'high'
                elif base_change < -0.10:
                    record.price_trend = 'down'
                    record.priority = 'high'
                elif abs(base_change) < 0.05:
                    record.price_trend = 'stable'
                else:
                    record.price_trend = 'volatile'

                # Generate market factors
                factors = [
                    "Seasonal demand fluctuations",
                    "Weather conditions affecting production",
                    "Commodity market trends",
                    "Supply chain disruptions",
                    "Export/import regulations"
                ]
                record.market_factors = json.dumps(factors)

                # Generate sales strategy
                if record.price_trend == 'up':
                    record.sales_strategy = """
                    <p><strong>Optimal Strategy:</strong> Consider holding inventory for better prices.</p>
                    <ul>
                        <li>Wait for price peak if storage is available</li>
                        <li>Consider futures contracts to lock in higher prices</li>
                        <li>Explore premium market segments</li>
                    </ul>
                    """
                    record.optimal_sales_timing = "Hold for 30-60 days when prices are expected to peak"
                elif record.price_trend == 'down':
                    record.sales_strategy = """
                    <p><strong>Optimal Strategy:</strong> Sell quickly to avoid losses.</p>
                    <ul>
                        <li>Harvest and sell immediately if ready</li>
                        <li>Consider processing to add value</li>
                        <li>Explore alternative markets</li>
                    </ul>
                    """
                    record.optimal_sales_timing = "Sell as soon as possible before further price decline"
                else:
                    record.sales_strategy = """
                    <p><strong>Optimal Strategy:</strong> Monitor closely and sell at local peaks.</p>
                    <ul>
                        <li>Watch for short-term price fluctuations</li>
                        <li>Consider partial sales to reduce risk</li>
                        <li>Prepare for seasonal changes</li>
                    </ul>
                    """
                    record.optimal_sales_timing = "Monitor weekly, sell during temporary price peaks"

                record.confidence_score = min(85, max(60, 70 + random.uniform(-10, 10)))
                record.status = 'recommended'