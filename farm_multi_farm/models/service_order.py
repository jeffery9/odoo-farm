from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class ServiceOrder(models.Model):
    """
    服务订单 [US-19-13]
    """
    _name = 'service.order'
    _description = 'Service Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Order Reference', required=True, default=lambda self: _('New'))
    service_id = fields.Many2one('agri.service', string='Service', required=True)
    requester_member_id = fields.Many2one('cooperative.member', string='Requester Member', required=True)
    order_date = fields.Date('Order Date', default=fields.Date.context_today, required=True)
    required_date = fields.Date('Required Date', required=True)
    service_quantity = fields.Float('Service Quantity', required=True)
    unit_rate = fields.Float('Unit Rate', related='service_id.unit_rate')
    total_amount = fields.Float('Total Amount', compute='_compute_total_amount', store=True)
    description = fields.Text('Service Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', required=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('service.order') or '/'
        return super().create(vals)

    @api.depends('service_quantity', 'unit_rate')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = record.service_quantity * record.unit_rate

    def action_confirm(self):
        """确认订单"""
        for order in self:
            order.state = 'confirmed'

    def action_start_service(self):
        """开始服务"""
        for order in self:
            order.state = 'in_progress'

    def action_complete_service(self):
        """完成服务"""
        for order in self:
            order.state = 'completed'
            # Create settlement
            settlement = self.env['internal.settlement'].create({
                'from_entity_id': order.requester_member_id.partner_id.company_id.id,
                'to_entity_id': order.service_id.provider_member_id.partner_id.company_id.id,
                'settlement_type': 'service_fee',
                'amount': order.total_amount,
                'description': f'Service fee for {order.service_id.name}',
                'settlement_date': order.order_date,
            })