from odoo import models, fields, api


class SupplyChainNodeMixin(models.AbstractModel):
    """
    Base mixin for supply chain nodes
    """
    _name = 'supply.chain.node.mixin'
    _description = 'Supply Chain Node Mixin'

    # Basic node information
    name = fields.Char('Node Name', required=True)
    node_code = fields.Char('Node Code', required=True, copy=False)
    node_type = fields.Selection([
        ('supplier', 'Supplier'),
        ('producer', 'Producer'),
        ('processor', 'Processor'),
        ('distributor', 'Distributor'),
        ('retailer', 'Retailer'),
    ], string='Node Type', required=True)

    partner_id = fields.Many2one('res.partner', string='Associated Partner')
    location_id = fields.Many2one('farm.location', string='Location')

    # KPIs
    inventory_value = fields.Monetary('Inventory Value')
    pending_inbound = fields.Float('Pending Inbound')
    pending_outbound = fields.Float('Pending Outbound')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)

    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('critical', 'Critical'),
    ], string='Status', default='active')

    _sql_constraints = [
        ('node_code_unique', 'UNIQUE(node_code)', 'Node code must be unique!'),
    ]