from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class AgriService(models.Model):
    """
    社会化服务产能共享 [US-19-13]
    """
    _name = 'agri.service'
    _description = 'Agricultural Service'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Service Name', required=True)
    code = fields.Char('Service Code', required=True, copy=False)
    cooperative_id = fields.Many2one('cooperative.entity', string='Cooperative', required=True)
    provider_member_id = fields.Many2one('cooperative.member', string='Provider Member', required=True)
    service_category = fields.Selection([
        ('spraying', 'Spraying/Flying'),
        ('tillage', 'Tillage'),
        ('harvesting', 'Harvesting'),
        ('transport', 'Transport'),
        ('pruning', 'Pruning'),
        ('other', 'Other'),
    ], string='Service Category', required=True)
    capacity = fields.Float('Capacity', help='Service capacity per unit time')
    capacity_unit = fields.Char('Capacity Unit', default='hectares/day')
    unit_rate = fields.Float('Unit Rate', required=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    available_from = fields.Datetime('Available From', default=fields.Datetime.now)
    available_to = fields.Datetime('Available To')
    location = fields.Char('Service Location')
    description = fields.Text('Description')
    is_active = fields.Boolean('Is Active', default=True)

    @api.model
    def create(self, vals):
        if 'code' not in vals or not vals['code']:
            vals['code'] = self.env['ir.sequence'].next_by_code('agri.service') or '/'
        return super().create(vals)

    def action_set_available(self):
        """设置为可用"""
        self.available_from = fields.Datetime.now()
        self.is_active = True

    def action_set_unavailable(self):
        """设置为不可用"""
        self.is_active = False