from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class JointProcurement(models.Model):
    """
    统购统销内部清算 [US-19-10]
    """
    _name = 'joint.procurement'
    _description = 'Joint Procurement'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Procurement Reference', required=True, default=lambda self: _('New'))
    cooperative_id = fields.Many2one('cooperative.entity', string='Cooperative', required=True)
    procurement_date = fields.Date('Procurement Date', default=fields.Date.context_today, required=True)
    supplier_id = fields.Many2one('res.partner', string='Supplier', required=True)
    total_amount = fields.Float('Total Amount', required=True)
    markup_rate = fields.Float('Markup Rate (%)', default=0.0, help='Markup rate applied to members')
    procurement_type = fields.Selection([
        ('fertilizer', 'Fertilizer'),
        ('pesticide', 'Pesticide'),
        ('feed', 'Feed'),
        ('seeds', 'Seeds'),
        ('equipment', 'Equipment'),
        ('other', 'Other'),
    ], string='Procurement Type', required=True)
    description = fields.Text('Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', required=True)

    procurement_lines = fields.One2many('joint.procurement.line', 'procurement_id', string='Procurement Lines')
    settlement_lines = fields.One2many('internal.settlement', 'joint_procurement_id', string='Settlement Lines')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('joint.procurement') or '/'
        return super().create(vals)

    def action_confirm(self):
        """确认采购"""
        for procurement in self:
            procurement.state = 'confirmed'

    def action_complete(self):
        """完成采购并生成结算"""
        for procurement in self:
            procurement.state = 'completed'
            # Generate settlements for each member's share
            for line in procurement.procurement_lines:
                settlement = self.env['internal.settlement'].create({
                    'from_entity_id': line.member_id.partner_id.company_id.id,
                    'to_entity_id': procurement.cooperative_id.company_id.id,
                    'settlement_type': 'joint_procurement',
                    'joint_procurement_id': procurement.id,
                    'activity_production_id': False,
                    'amount': line.member_amount,
                    'description': f'Share of joint procurement {procurement.name} for {line.product_id.name}',
                    'settlement_date': procurement.procurement_date,
                })
                line.settlement_id = settlement.id
class InternalSettlementExtension(models.Model):
    _inherit = 'internal.settlement'
    
    joint_procurement_id = fields.Many2one('joint.procurement', string='Joint Procurement')
