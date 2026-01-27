from odoo import models, fields, api, _
import random
import json

class FarmSupplyChainNode(models.Model):
    _name = 'farm.supply.chain.node'
    _description = 'Supply Chain Node (Control Tower)'

    name = fields.Char("Node Name", required=True)
    node_type = fields.Selection([
        ('supplier', 'Input Supplier'),
        ('farm', 'Production Farm'),
        ('processing', 'Processing Plant'),
        ('warehouse', 'Logistics Center'),
        ('distributor', 'Distributor/Customer')
    ], string="Node Type", required=True)
    
    partner_id = fields.Many2one('res.partner', string="Associated Entity")
    location_id = fields.Many2one('farm.location', string="Physical Location")
    
    # Real-time KPIs
    current_inventory_value = fields.Monetary("Inventory Value", currency_field='currency_id')
    pending_inbound_qty = fields.Float("Pending Inbound")
    pending_outbound_qty = fields.Float("Pending Outbound")
    
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    
    status = fields.Selection([
        ('normal', 'Normal'),
        ('delayed', 'Delayed'),
        ('critical', 'Critical Outage')
    ], default='normal', compute='_compute_node_status')

    def _compute_node_status(self):
        for rec in self:
            # Simulated logic for control tower
            if rec.pending_outbound_qty > 100:
                rec.status = 'delayed'
            else:
                rec.status = 'normal'

class FarmSupplyDemandForecast(models.Model):
    _name = 'farm.supply.demand.forecast'
    _description = 'Supply Chain Demand Forecast'
    _inherit = ['ai.decision.base']

    product_id = fields.Many2one('product.template', string="Product", required=True)
    forecast_period = fields.Selection([
        ('7d', 'Next 7 Days'),
        ('30d', 'Next 30 Days'),
        ('season', 'Full Production Season')
    ], default='30d')
    
    predicted_demand_qty = fields.Float("Predicted Demand")
    current_stock_level = fields.Float("Current Stock")
    safety_stock_recommended = fields.Float("Recommended Safety Stock")
    
    optimization_action = fields.Selection([
        ('replenish', 'Replenish Now'),
        ('liquidate', 'Excess Stock - Sell Now'),
        ('transfer', 'Internal Transfer Recommended'),
        ('hold', 'Stock Level Optimal')
    ], string="Optimization Action", compute='_compute_optimization')

    @api.depends('predicted_demand_qty', 'current_stock_level', 'safety_stock_recommended')
    def _compute_optimization(self):
        """US-54-02: Inventory Optimization Algorithm"""
        for rec in self:
            gap = (rec.predicted_demand_qty + rec.safety_stock_recommended) - rec.current_stock_level
            if gap > 0:
                rec.optimization_action = 'replenish'
            elif gap < -50:
                rec.optimization_action = 'liquidate'
            else:
                rec.optimization_action = 'hold'

class FarmSupplyRiskMonitor(models.Model):
    _name = 'farm.supply.risk.monitor'
    _description = 'Supply Chain Risk Monitoring'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Risk Event", required=True)
    risk_category = fields.Selection([
        ('logistics', 'Transport Disruption'),
        ('quality', 'Batch Quality Recall'),
        ('supplier', 'Supplier Default'),
        ('weather', 'Climate Impact')
    ], string="Risk Type", required=True)
    
    impact_level = fields.Selection([
        ('1', 'Low'), ('2', 'Medium'), ('3', 'High'), ('4', 'Catastrophic')
    ], default='1')
    
    affected_node_ids = fields.Many2many('farm.supply.chain.node', string="Affected Nodes")
    mitigation_plan = fields.Text("Emergency Response Plan")
    
    state = fields.Selection([
        ('identified', 'Risk Identified'),
        ('active', 'Active Impact'),
        ('mitigated', 'Mitigated'),
        ('closed', 'Resolved')
    ], default='identified', tracking=True)

    def action_trigger_alert(self):
        """US-54-03: Real-time Risk Alerting"""
        self.ensure_one()
        for node in self.affected_node_ids:
            node.message_post(body=_("RISK ALERT: '%s' impact detected on this node.") % self.name)
