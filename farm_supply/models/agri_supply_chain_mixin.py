from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        """ [ISL/DNA Bridge] Inject initial DNA upon supply receipt. """
        res = super(StockPicking, self).button_validate()
        
        # Only process inbound supply orders (Purchase/Supply)
        for picking in self.filtered(lambda p: p.picking_type_id.code == 'incoming' and p.state == 'done'):
            for move in picking.move_ids:
                if move.lot_ids:
                    for lot in move.lot_ids:
                        # Use DNA engine with inbound context
                        # Pass move as input context
                        lot.inherit_dna_from_source(move)
        return res
class AgriSupplyChainNodeMixin(models.AbstractModel):
    """
    Base mixin for agricultural supply chain nodes
    """
    _name = 'agri.supply.chain.node.mixin'
    _description = 'Agricultural Supply Chain Node Mixin'

    # Basic node information
    name = fields.Char('Node Name', required=True)
    node_code = fields.Char('Node Code', required=True, copy=False)
    node_type = fields.Selection([
        ('supplier', 'Supplier'),
        ('producer', 'Producer'),
        ('processor', 'Processor'),
        ('distributor', 'Distributor'),
        ('retailer', 'Retailer'),
    ], string='Node Type', required=True, default='producer', ondelete={'supplier': 'set default', 'producer': 'set default', 'processor': 'set default', 'distributor': 'set default', 'retailer': 'set default'})

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

    _node_code_unique = models.Constraint(
        'UNIQUE(node_code)',
        'Node code must be unique!'
    )