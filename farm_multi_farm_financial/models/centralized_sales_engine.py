from odoo import models, fields, api, _

class InternalSettlement(models.Model):
    _inherit = 'internal.settlement'

    def action_centralized_sales_revenue_split(self, sale_order):
        """
        [US-SCENARIO-17] Distributed Grow, Centralized Brand Sales
        When the cooperative sells a mega-lot (e.g., Premium Tomatoes), this engine
        looks back at the traceability tree to find the individual smallholders who
        contributed to this batch. It then automatically generates internal settlements
        to transfer the high-margin retail profit back to the farmers based on their
        contributed weight.
        """
        # For this scenario, we assume the sale.order contains order lines with specific lots.
        # In a real deep-trace scenario, we'd traverse the mrp.production origin tree.
        # For simplicity in STDD, we assume the lots sold carry an 'origin_farmer_id'
        # or we just split the revenue based on a predefined contribution list.
        
        # Let's look for contribution tracking. If not present, we mock it.
        total_revenue = sale_order.amount_untaxed
        
        # Identify contributors
        # We will inject 'contributor_ids' onto stock.lot in the test or mixin
        contributor_settlements = []
        
        for line in sale_order.order_line:
            if line.lot_id and hasattr(line.lot_id, 'contributor_ids') and line.lot_id.contributor_ids:
                # Calculate revenue per kg
                revenue_per_kg = line.price_subtotal / (line.product_uom_qty or 1)
                
                for contribution in line.lot_id.contributor_ids:
                    # Cooperative keeps 10% management fee, Farmer gets 90%
                    payout_amount = contribution.contributed_qty * revenue_per_kg * 0.90
                    
                    settlement = self.create({
                        'from_entity_id': sale_order.company_id.partner_id.id, # Coop pays
                        'to_entity_id': contribution.farmer_id.partner_id.id, # Farmer receives
                        'settlement_type': 'general',
                        'amount': payout_amount,
                        'description': f"Revenue Share (90%) for Centralized Sale of {line.product_id.name}"
                    })
                    settlement.action_confirm()
                    contributor_settlements.append(settlement)
                    
        sale_order.message_post(body=_("Centralized Sales Revenue Split Executed: Generated %s payouts to contributing farmers.") % len(contributor_settlements))
        return contributor_settlements

class StockLotContribution(models.Model):
    _name = 'stock.lot.contribution'
    _description = 'Lot Contribution by Smallholder'
    
    lot_id = fields.Many2one('stock.lot', required=True, ondelete='cascade')
    farmer_id = fields.Many2one('res.users', string="Contributing Farmer", required=True)
    contributed_qty = fields.Float("Contributed Quantity (kg)", required=True)

class StockLot(models.Model):
    _inherit = 'stock.lot'
    
    contributor_ids = fields.One2many('stock.lot.contribution', 'lot_id', string="Smallholder Contributors")

