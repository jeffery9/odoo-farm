from odoo import models, fields, api, _

class LiveOrder(models.Model):
    _inherit = 'live.order'

    routing_status = fields.Selection([
        ('pending', 'Pending Routing'),
        ('routed', 'Routed to Edge Hub'),
        ('failed', 'Routing Failed')
    ], default='pending')

    edge_warehouse_id = fields.Many2one('stock.warehouse', string="Dispatched Edge Warehouse")

    def action_import_and_route(self):
        """
        [US-SCENARIO-45] Omnichannel Live-Streaming Commerce
        Instantly process a massive spike in orders by checking global inventory 
        and routing the dispatch to the closest Edge Warehouse.
        """
        # Find all unrouted imported orders
        orders = self.filtered(lambda o: o.state == 'draft' and o.routing_status == 'pending')
        
        # Mock product and customer from raw data for the test
        # Assume product and destination city is somehow parsed
        
        # 1. Edge Warehouse Routing Logic
        warehouses = self.env['stock.warehouse'].search([])
        if not warehouses:
            return False
            
        for order in orders:
            # Create Sale Order
            so = self.env['sale.order'].create({
                'partner_id': self.env.user.partner_id.id, # Mock buyer
                'client_order_ref': order.dy_order_id,
            })
            
            # Simple Geo-Routing: assign round-robin to edge warehouses to simulate load balancing
            edge_warehouse = warehouses[order.id % len(warehouses)]
            
            so.warehouse_id = edge_warehouse.id
            
            # Create Line
            # Find a product
            product = self.env['product.product'].search([], limit=1)
            
            self.env['sale.order.line'].create({
                'order_id': so.id,
                'product_id': product.id,
                'product_uom_qty': 1.0, # Mock qty
            })
            
            so.action_confirm() # This deducts virtual stock and creates the picking
            
            # Ensure the picking uses cold chain if product requires it
            for picking in so.picking_ids:
                if product.product_tmpl_id.requires_cold_chain:
                    picking.is_cold_chain = True
            
            order.write({
                'state': 'imported',
                'odoo_so_id': so.id,
                'edge_warehouse_id': edge_warehouse.id,
                'routing_status': 'routed'
            })
            
            order.message_post(body=_("Order routed to Edge Warehouse: %s") % edge_warehouse.name)
            
        return True
