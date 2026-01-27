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