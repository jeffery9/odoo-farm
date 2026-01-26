from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class JointProcurementLine(models.Model):
    """
    统购统销明细 [US-19-10]
    """
    _name = 'joint.procurement.line'
    _description = 'Joint Procurement Line'

    procurement_id = fields.Many2one('joint.procurement', string='Procurement', required=True, ondelete='cascade')
    member_id = fields.Many2one('cooperative.member', string='Member', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float('Quantity', required=True)
    unit_price = fields.Float('Unit Price', required=True)
    member_amount = fields.Float('Member Amount', compute='_compute_member_amount', store=True)
    markup_amount = fields.Float('Markup Amount', compute='_compute_markup_amount', store=True)
    settlement_id = fields.Many2one('internal.settlement', string='Settlement')

    @api.depends('quantity', 'unit_price')
    def _compute_member_amount(self):
        for line in self:
            line.member_amount = line.quantity * line.unit_price

    @api.depends('member_amount')
    def _compute_markup_amount(self):
        for line in self:
            if line.procurement_id:
                markup_rate = line.procurement_id.markup_rate / 100.0
                line.markup_amount = line.member_amount * markup_rate