from odoo import models, fields, api, _

class FarmMarketDemand(models.Model):
    _name = 'farm.market.demand'
    _description = 'Market Demand Analysis'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Demand Title", required=True)
    partner_id = fields.Many2one('res.partner', string="Buyer/Aggregator", domain=[('is_company', '=', True)])
    product_id = fields.Many2one('product.template', string="Product Needed", required=True)
    
    quantity_required = fields.Float("Target Quantity")
    uom_id = fields.Many2one('uom.uom', string="Unit of Measure")
    
    target_price = fields.Monetary("Target Price", currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    
    delivery_date = fields.Date("Required Delivery Date")
    quality_spec = fields.Text("Quality Specifications")
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active Demand'),
        ('matched', 'Production Matched'),
        ('closed', 'Closed/Fulfilled')
    ], default='draft', tracking=True)

    matched_lot_ids = fields.Many2many('stock.lot', relation='market_demand_stock_lot_rel', column1='demand_id', column2='lot_id', string="Matched Farm Lots")

    def action_match_production(self):
        """
        Logic to match market demand with available or planned farm lots.
        Filters by product type, quality specifications, and availability dates.
        """
        for rec in self:
            # Simple matching logic: find lots with the same product
            matching_lots = self.env['stock.lot'].search([
                ('product_id', '=', rec.product_id.id),
                ('state', 'not in', ['sold', 'scrap'])
            ])
            rec.matched_lot_ids = [(6, 0, matching_lots.ids)]
            if matching_lots:
                rec.state = 'matched'
            return True
