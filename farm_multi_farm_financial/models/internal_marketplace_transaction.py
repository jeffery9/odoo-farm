from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class InternalMarketplaceTransaction(models.Model):
    """
    市场平台交易 [US-042-11]
    """
    _name = 'internal.marketplace.transaction'
    _description = 'Internal Marketplace Transaction'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Transaction Reference', required=True, default=lambda self: _('New'))
    supplier_member_id = fields.Many2one('cooperative.member', string='Supplier Member', required=True)
    requester_member_id = fields.Many2one('cooperative.member', string='Requester Member', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float('Quantity', required=True)
    unit_price = fields.Float('Unit Price', required=True)
    total_amount = fields.Float('Total Amount', compute='_compute_total_amount', store=True)
    transaction_date = fields.Date('Transaction Date', default=fields.Date.context_today)
    picking_id = fields.Many2one('stock.picking', string='Stock Picking')
    settlement_id = fields.Many2one('internal.settlement', string='Settlement')
    state = fields.Selection([
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed'),
    ], string='State', default='pending', required=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('internal.marketplace.transaction') or '/'
        return super().create(vals)

    @api.depends('quantity', 'unit_price')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = record.quantity * record.unit_price

    def action_confirm(self):
        """确认交易"""
        for transaction in self:
            transaction.state = 'confirmed'

    def action_create_picking(self):
        """创建调拨单"""
        for transaction in self:
            # This would create a stock picking between the entities
            pass

    def action_create_settlement(self):
        """创建结算"""
        for transaction in self:
            settlement = self.env['internal.settlement'].create({
                'from_entity_id': transaction.requester_member_id.partner_id.company_id.id,
                'to_entity_id': transaction.supplier_member_id.partner_id.company_id.id,
                'settlement_type': 'internal_transaction',
                'amount': transaction.total_amount,
                'description': f'Marketplace transaction for {transaction.product_id.name}',
                'settlement_date': transaction.transaction_date,
            })
            transaction.settlement_id = settlement.id