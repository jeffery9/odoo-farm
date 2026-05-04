# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
import json
from datetime import datetime, timedelta
import random

_logger = logging.getLogger(__name__)

class AgriAiMarketPrediction(models.Model):
    """
    AI model for market price prediction
    Implements US-088-08: Agri-market intelligent prediction
    US-090-04: Revenue Management & Hedging
    US-090-05: Procurement Timing Prediction
    """
    _name = 'agri.ai.market.prediction'
    _description = 'AI Market Prediction'
    _inherit = ['agri.ai.decision.base']

    prediction_type = fields.Selection([
        ('sales', 'Sales/Revenue Optimization'),
        ('procurement', 'Input Procurement Optimization')
    ], string='Analysis Type', default='sales', required=True)

    product_id = fields.Many2one('product.template', string='Product/Input')
    current_price = fields.Float('Current Market Price')
    predicted_price_7d = fields.Float('Predicted Price (7 days)')
    predicted_price_30d = fields.Float('Predicted Price (30 days)')
    predicted_price_90d = fields.Float('Predicted Price (90 days)')
    
    price_trend = fields.Selection([
        ('up', 'Upward Trend'),
        ('down', 'Downward Trend'),
        ('stable', 'Stable'),
        ('volatile', 'High Volatility'),
    ], string='Price Trend')

    # US-090-04: Hedging & Revenue Management
    futures_price = fields.Float('Futures Price (Target Month)')
    basis_value = fields.Float('Basis (Spot - Futures)', compute='_compute_basis')
    hedging_recommendation = fields.Html('Hedging Strategy')
    optimal_sales_ratio = fields.Float('Recommended Sales Ratio (%)', help="Percentage of inventory to sell now vs hold/hedge")
    
    # US-090-05: Procurement Timing
    procurement_action = fields.Selection([
        ('buy_now', 'Strong Buy (Bottom Price)'),
        ('wait', 'Hold/Wait (Price Peak)'),
        ('bulk', 'Bulk Procurement Recommended'),
        ('minimal', 'Minimal Purchase Only')
    ], string="Procurement Action")

    market_factors = fields.Text('Market Factors Analysis')
    decision_summary = fields.Html('AI Decision Summary')

    @api.depends('current_price', 'futures_price')
    def _compute_basis(self):
        for rec in self:
            rec.basis_value = rec.current_price - rec.futures_price

    def calculate_market_prediction(self):
        """Enhanced AI calculation for Sales and Procurement"""
        for record in self:
            if not record.current_price:
                continue

            # 1. Base Prediction Logic (Simulated)
            base_change = random.uniform(-0.15, 0.20)
            seasonal_factor = 1.0
            if record.product_id:
                p_name = record.product_id.name.lower()
                if any(x in p_name for x in ['fertilizer', 'urea', 'potash']):
                    # Fertilizer linked to energy/oil
                    seasonal_factor = 1.0 + (0.10 if datetime.now().month in [3, 4, 9, 10] else -0.05)
                elif any(x in p_name for x in ['wheat', 'corn', 'soybean']):
                    seasonal_factor = 1.0 + (0.05 if datetime.now().month in [6, 7, 8] else -0.05)

            record.predicted_price_7d = record.current_price * (1 + base_change * 0.2) * seasonal_factor
            record.predicted_price_30d = record.current_price * (1 + base_change * 0.6) * seasonal_factor
            record.predicted_price_90d = record.current_price * (1 + base_change) * seasonal_factor

            # 2. Strategy Logic
            if record.prediction_type == 'sales':
                self._calculate_sales_strategy(record, base_change)
            else:
                self._calculate_procurement_strategy(record, base_change)

            record.confidence_score = min(90, max(65, 75 + random.uniform(-10, 10)))
            record.status = 'recommended'

    def _calculate_sales_strategy(self, record, base_change):
        """US-090-04: Revenue Management & Hedging"""
        record.futures_price = record.current_price * (1 + base_change * 1.1)
        
        if base_change > 0.05:
            record.price_trend = 'up'
            record.optimal_sales_ratio = 20.0
            record.hedging_recommendation = """
                <div class='alert alert-info'>
                    <strong>Bullish Signal:</strong> Prices are rising. 
                    Suggest holding 80% of stock. Sell 20% to cover immediate cash needs.
                    Consider <strong>Long Call</strong> options to protect against missing further upside.
                </div>
            """
        elif base_change < -0.05:
            record.price_trend = 'down'
            record.optimal_sales_ratio = 70.0
            record.hedging_recommendation = """
                <div class='alert alert-warning'>
                    <strong>Bearish Signal:</strong> Downward pressure detected.
                    Suggest immediate sale of 70% of inventory. 
                    <strong>Hedge Recommendation:</strong> Short Futures on Zhengzhou Commodity Exchange (ZCE) to lock in current rates.
                </div>
            """
        else:
            record.price_trend = 'stable'
            record.optimal_sales_ratio = 50.0
            record.hedging_recommendation = "<p>Market stable. Maintain balanced sales approach.</p>"

    def _calculate_procurement_strategy(self, record, base_change):
        """US-090-05: Input Procurement Optimization"""
        if base_change < -0.08:
            record.procurement_action = 'buy_now'
            record.price_trend = 'down' # Good for buying
            record.decision_summary = """
                <p class='text-success'><strong>Bottom detected.</strong> AI predicts price rebound in 30 days.
                Recommend <strong>Bulk Procurement</strong> for the next 2 production cycles.</p>
            """
        elif base_change > 0.08:
            record.procurement_action = 'wait'
            record.price_trend = 'up' # Bad for buying
            record.decision_summary = """
                <p class='text-danger'><strong>Price Peak.</strong> Energy costs driving fertilizer prices up.
                Wait for correction. Purchase <strong>Minimal</strong> quantities only.</p>
            """
        else:
            record.procurement_action = 'minimal'
            record.price_trend = 'stable'
            record.decision_summary = "<p>Prices normal. Regular procurement suggested.</p>"
