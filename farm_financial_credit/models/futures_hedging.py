# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
import json
from datetime import datetime, timedelta
import random

_logger = logging.getLogger(__name__)

class FarmFuturesHedging(models.Model):
    """
    Model for agricultural futures and hedging
    Implements US-059-07: Agri-Futures & Hedging Management
    """
    _name = 'farm.futures.hedging'
    _description = 'Farm Futures Hedging'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Hedging Reference', required=True, default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string='Farmer/Trader', required=True)
    hedging_type = fields.Selection([('futures', 'Futures Hedging')], string='Hedging Type', default='futures')

    amount = fields.Monetary('Hedging Amount', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', required=True)
    reference = fields.Char('Reference', help="External reference from broker")
    risk_score = fields.Float('Risk Score')
    interest_rate = fields.Float('Interest Rate (%)', digits=(16, 2), default=3.0)
    duration_months = fields.Integer('Duration (months)')
    application_date = fields.Date('Application Date', default=fields.Date.context_today)
    approval_date = fields.Date('Approval Date')
    maturity_date = fields.Date('Maturity Date', compute='_compute_maturity_date', store=True, precompute=True)
    service_fees = fields.Monetary('Service Fees', currency_field='currency_id')

    commodity_type = fields.Selection([
        ('corn', 'Corn'),
        ('wheat', 'Wheat'),
        ('soybean', 'Soybean'),
        ('cotton', 'Cotton'),
        ('sugar', 'Sugar'),
        ('coffee', 'Coffee'),
        ('live_cattle', 'Live Cattle'),
        ('lean_hogs', 'Lean Hogs'),
    ], string='Commodity Type')
    contract_month = fields.Selection([
        ('mar', 'March'),
        ('may', 'May'),
        ('jul', 'July'),
        ('sep', 'September'),
        ('dec', 'December'),
    ], string='Contract Month')
    contract_year = fields.Integer('Contract Year', default=lambda self: datetime.now().year)
    contract_size = fields.Float('Contract Size (units)', help="Size of each contract in commodity units")
    number_of_contracts = fields.Integer('Number of Contracts')
    entry_price = fields.Float('Entry Price ($/unit)', digits=(16, 4))
    current_price = fields.Float('Current Price ($/unit)', digits=(16, 4))
    exit_price = fields.Float('Exit Price ($/unit)', digits=(16, 4))
    position_type = fields.Selection([
        ('long', 'Long (Buy) - Hedge against price increase'),
        ('short', 'Short (Sell) - Hedge against price decrease'),
    ], string='Position Type', default='short')
    strategy_type = fields.Selection([
        ('floor', 'Floor Price Protection'),
        ('ceiling', 'Ceiling Price Protection'),
        ('collar', 'Collar Strategy'),
        ('speculation', 'Speculation'),
    ], string='Strategy Type', default='floor')
    margin_amount = fields.Monetary('Margin Amount', currency_field='currency_id')
    unrealized_pnl = fields.Monetary('Unrealized P&L', currency_field='currency_id', compute='_compute_unrealized_pnl', store=True, precompute=True)
    stop_loss_price = fields.Float('Stop Loss Price ($/unit)', digits=(16, 4))
    take_profit_price = fields.Float('Take Profit Price ($/unit)', digits=(16, 4))
    exchange_name = fields.Char('Exchange', default='CME Group')
    broker_id = fields.Many2one('res.partner', string='Broker', domain=[('is_broker', '=', True)])
    position_status = fields.Selection([
        ('open', 'Open'),
        ('partially_closed', 'Partially Closed'),
        ('closed', 'Closed'),
    ], string='Position Status', default='open')
    hedge_effectiveness = fields.Float('Hedge Effectiveness (%)', digits=(16, 2))

    @api.depends('current_price', 'entry_price', 'number_of_contracts', 'contract_size')
    def _compute_unrealized_pnl(self):
        for record in self:
            if record.current_price and record.entry_price and record.number_of_contracts and record.contract_size:
                if record.position_type == 'long':
                    price_change = record.current_price - record.entry_price
                else:  # short position
                    price_change = record.entry_price - record.current_price

                record.unrealized_pnl = price_change * record.number_of_contracts * record.contract_size
            else:
                record.unrealized_pnl = 0

    def update_current_price(self):
        """Update current market price"""
        for record in self:
            # In a real system, this would connect to market data feeds
            # For simulation, we'll add some random fluctuation
            base_change = random.uniform(-0.1, 0.1)  # +/- 10% fluctuation
            record.current_price = record.entry_price * (1 + base_change)

    def calculate_margin(self):
        """Calculate required margin for position"""
        for record in self:
            if record.entry_price and record.number_of_contracts and record.contract_size:
                total_value = record.entry_price * record.number_of_contracts * record.contract_size
                # Typical margin requirement is 5-10% of contract value
                margin_rate = 0.07  # 7% margin requirement
                record.margin_amount = total_value * margin_rate
                record.amount = record.margin_amount  # Use margin as the "amount" for this service

    @api.depends('application_date', 'duration_months')
    def _compute_maturity_date(self):
        for record in self:
            if record.application_date and record.duration_months:
                record.maturity_date = fields.Date.from_string(record.application_date) + timedelta(days=record.duration_months*30)
            else:
                record.maturity_date = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.futures.hedging') or _('FH')
        return super().create(vals_list)

    def action_open_position(self):
        """Open the futures hedging position"""
        self.write({'state': 'open'})

    def action_activate_position(self):
        """Activate the hedging position after opening"""
        self.write({'state': 'active'})

    def action_close_position(self):
        """Close the hedging position"""
        self.write({'state': 'closed'})