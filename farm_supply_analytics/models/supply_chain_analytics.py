from odoo import models, fields, api, _
import random
import json


class FarmSupplyChainNode(models.Model):
    _name = 'farm.supply.chain.node'
    _description = 'Supply Chain Node (Control Tower)'
    _inherit = ['supply.chain.node.mixin']

    # Add specific fields for supply chain analytics
    node_type = fields.Selection(selection_add=[
        ('supplier', 'Input Supplier'),
        ('farm', 'Production Farm'),
        ('processing', 'Processing Plant'),
        ('warehouse', 'Logistics Center'),
        ('distributor', 'Distributor/Customer')
    ])

    # Real-time KPIs from the original smart supply chain
    current_inventory_value = fields.Monetary("Inventory Value", related='inventory_value', readonly=False)
    pending_inbound_qty = fields.Float("Pending Inbound", related='pending_inbound', readonly=False)
    pending_outbound_qty = fields.Float("Pending Outbound", related='pending_outbound', readonly=False)

    status = fields.Selection(selection_add=[
        ('normal', 'Normal'),
        ('delayed', 'Delayed'),
        ('critical', 'Critical Outage')
    ], compute='_compute_node_status', store=True)

    def _compute_node_status(self):
        for rec in self:
            # Simulated logic for control tower
            if rec.pending_outbound_qty > 100:
                rec.status = 'delayed'
            else:
                rec.status = 'normal'


class SupplyChainDashboard(models.Model):
    """
    Supply Chain Dashboard for Control Tower [US-54-01]
    """
    _name = 'supply.chain.dashboard'
    _description = 'Supply Chain Dashboard'

    name = fields.Char('Dashboard Name', required=True)
    description = fields.Text('Description')

    # Overall KPIs
    total_nodes = fields.Integer('Total Nodes', compute='_compute_kpis')
    active_nodes = fields.Integer('Active Nodes', compute='_compute_kpis')
    critical_nodes = fields.Integer('Critical Nodes', compute='_compute_kpis')

    total_inventory_value = fields.Monetary('Total Inventory Value', compute='_compute_kpis')
    total_pending_orders = fields.Integer('Total Pending Orders', compute='_compute_kpis')

    # Visualization data
    node_status_data = fields.Text('Node Status Data', compute='_compute_visualization_data')
    inventory_trend_data = fields.Text('Inventory Trend Data', compute='_compute_visualization_data')

    @api.depends('name')
    def _compute_kpis(self):
        for dashboard in self:
            all_nodes = self.env['farm.supply.chain.node'].search([])
            dashboard.total_nodes = len(all_nodes)
            dashboard.active_nodes = len(all_nodes.filtered(lambda n: n.status == 'active'))
            dashboard.critical_nodes = len(all_nodes.filtered(lambda n: n.status == 'critical'))

            dashboard.total_inventory_value = sum(node.current_inventory_value for node in all_nodes)
            # Calculate pending orders based on purchase/sales orders
            po_count = self.env['purchase.order'].search_count([('state', 'in', ['draft', 'sent', 'to approve'])])
            so_count = self.env['sale.order'].search_count([('state', 'in', ['draft', 'sent'])])
            dashboard.total_pending_orders = po_count + so_count

    @api.depends('name')
    def _compute_visualization_data(self):
        for dashboard in self:
            # Node status distribution for visualization
            all_nodes = self.env['farm.supply.chain.node'].search([])
            status_counts = {}
            for node in all_nodes:
                status = node.status or 'unknown'
                status_counts[status] = status_counts.get(status, 0) + 1

            dashboard.node_status_data = json.dumps(status_counts)

            # Basic inventory trend (would be more sophisticated in real implementation)
            dashboard.inventory_trend_data = json.dumps({
                'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                'data': [random.randint(10000, 50000) for _ in range(6)]
            })