from odoo import models, fields, api, _

class InternalMarketplace(models.Model):
    _inherit = 'internal.marketplace'

    joint_procurement_id = fields.Many2one('joint.procurement', string="Linked Bulk Procurement")

class JointProcurement(models.Model):
    _inherit = 'joint.procurement'

    def action_aggregate_demands(self):
        """
        [US-SCENARIO-16] Cooperative Bulk Procurement
        Aggregates all open demands for the same product into this bulk procurement.
        """
        self.ensure_one()
        demands = self.env['internal.marketplace'].search([
            ('cooperative_id', '=', self.cooperative_id.id),
            ('listing_type', '=', 'demand'),
            ('state', '=', 'active'),
            ('joint_procurement_id', '=', False)
        ])
        
        # Group by product
        aggregated = {}
        for demand in demands:
            if demand.product_id not in aggregated:
                aggregated[demand.product_id] = []
            aggregated[demand.product_id].append(demand)
            
        for product, group in aggregated.items():
            total_qty = sum(d.quantity for d in group)
            # Create a line for each member (or we can just sum it up on the procurement lines)
            for demand in group:
                self.env['joint.procurement.line'].create({
                    'procurement_id': self.id,
                    'member_id': demand.supplier_member_id.id, # 'supplier_member_id' acts as the requestor in 'demand' type
                    'product_id': product.id,
                    'quantity': demand.quantity,
                    'unit_price': self.total_amount / max(1, len(demands)), # Dummy price fallback
                })
                demand.joint_procurement_id = self.id
                demand.state = 'completed'
                
        self.message_post(body=_("Aggregated %s micro-demands from members.") % len(demands))
        return True

    def action_confirm_and_allocate(self):
        """
        Confirms the procurement, simulating delivery to the village hub, 
        and automatically allocates to each member's virtual micro-inventory.
        """
        self.state = 'completed'
        for line in self.procurement_lines:
            # Generate Internal Settlement
            self.env['internal.settlement'].create({
                'from_entity_id': line.member_id.partner_id.id,
                'to_entity_id': self.cooperative_id.partner_id.id,
                'settlement_type': 'general',
                'amount': line.member_amount + line.markup_amount,
                'description': f"Bulk Procurement Share: {line.product_id.name}"
            })
            # Generate Virtual Stock Move (Micro-Inventory)
            # Find or create a virtual location for the member
            virtual_loc = self.env['stock.location'].search([
                ('name', '=', f"Virtual: {line.member_id.partner_id.name}"),
                ('usage', '=', 'internal')
            ], limit=1)
            if not virtual_loc:
                virtual_loc = self.env['stock.location'].create({
                    'name': f"Virtual: {line.member_id.partner_id.name}",
                    'usage': 'internal'
                })
            # Log the allocation
            self.message_post(body=_("Allocated %s %s to Micro-Inventory: %s") % (line.quantity, line.product_id.name, virtual_loc.name))

