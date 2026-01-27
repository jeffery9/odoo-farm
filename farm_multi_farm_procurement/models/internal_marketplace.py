from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class InternalMarketplace(models.Model):
    """
    内部余缺调剂平台 [US-19-11]
    """
    _name = 'internal.marketplace'
    _description = 'Internal Marketplace'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Listing Title', required=True)
    cooperative_id = fields.Many2one('cooperative.entity', string='Cooperative', required=True)
    supplier_member_id = fields.Many2one('cooperative.member', string='Supplier Member', required=True)
    listing_type = fields.Selection([
        ('surplus', 'Surplus'),
        ('demand', 'Demand'),
    ], string='Listing Type', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float('Quantity', required=True)
    unit_of_measure = fields.Many2one('uom.uom', string='Unit of Measure')
    unit_price = fields.Float('Unit Price')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    start_date = fields.Date('Available From', default=fields.Date.context_today)
    end_date = fields.Date('Available Until')
    location = fields.Char('Location')
    description = fields.Text('Description')
    is_active = fields.Boolean('Is Active', default=True)
    state = fields.Selection([
        ('open', 'Open'),
        ('matched', 'Matched'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='open', required=True)

    demand_matches = fields.One2many('marketplace.demand.match', 'listing_id', string='Demand Matches')
    transaction_id = fields.Many2one('internal.marketplace.transaction', string='Transaction')

    def action_match_demand(self):
        """匹配供需"""
        # Find matching demands for surplus listings or matching surplus for demand listings
        pass

    def action_complete_transaction(self):
        """完成交易"""
        for listing in self:
            if listing.state == 'matched':
                # Create transaction and update state
                transaction = self.env['internal.marketplace.transaction'].create({
                    'supplier_member_id': listing.supplier_member_id.id,
                    'requester_member_id': listing.demand_matches[0].member_id.id if listing.demand_matches else False,
                    'product_id': listing.product_id.id,
                    'quantity': min(listing.quantity, listing.demand_matches[0].quantity) if listing.demand_matches else listing.quantity,
                    'unit_price': listing.unit_price,
                    'listing_id': listing.id,
                })
                listing.transaction_id = transaction.id
                listing.state = 'completed'