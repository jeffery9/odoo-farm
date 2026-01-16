from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class JointProcurementConfiguration(models.Model):
    """
    农场联合采购合作组织 [US-09-15]
    """
    _name = 'joint.procurement.configuration'
    _description = 'Joint Procurement for Farm Cooperatives'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Cooperative Name', required=True, default=lambda self: _('New'))
    member_ids = fields.Many2many('res.partner', string='Cooperative Members',
                                  domain=[('is_company', '=', True), ('supplier_rank', '=', 0)])
    procurement_product_category = fields.Many2one('product.category', string='Procurement Product Category')
    agreement_start_date = fields.Date('Agreement Start Date', required=True)
    agreement_end_date = fields.Date('Agreement End Date', required=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True)
    joint_procurement_orders = fields.One2many('joint.procurement.order', 'coop_config_id', string='Joint Procurement Orders')
    total_participating_farms = fields.Integer('Total Participating Farms', compute='_compute_total_participating_farms', store=True)
    is_active = fields.Boolean('Is Active', compute='_compute_is_active', store=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('joint.procurement.configuration') or '/'
        return super().create(vals)

    @api.depends('member_ids')
    def _compute_total_participating_farms(self):
        for record in self:
            record.total_participating_farms = len(record.member_ids)

    @api.depends('agreement_start_date', 'agreement_end_date', 'status')
    def _compute_is_active(self):
        for record in self:
            today = fields.Date.context_today(self)
            record.is_active = (
                record.status == 'active' and
                record.agreement_start_date <= today <= record.agreement_end_date
            )

    def action_activate_cooperative(self):
        """Activate the cooperative agreement"""
        self.write({'status': 'active'})

    def action_close_cooperative(self):
        """Close the cooperative agreement"""
        self.write({'status': 'closed'})


class JointProcurementOrder(models.Model):
    """
    联合采购订单 [US-09-15]
    """
    _name = 'joint.procurement.order'
    _description = 'Joint Procurement Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    coop_config_id = fields.Many2one('joint.procurement.configuration', string='Cooperative Configuration', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product to Procure', required=True)
    requested_quantity = fields.Float('Requested Quantity', required=True)
    unit_of_measure = fields.Many2one('uom.uom', string='Unit of Measure', related='product_id.uom_id')
    requested_by_farm = fields.Many2one('res.partner', string='Requested By Farm',
                                       domain=[('is_company', '=', True), ('supplier_rank', '=', 0)])
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('ordered', 'Ordered'),
        ('delivered', 'Delivered'),
        ('invoiced', 'Invoiced'),
    ], string='Status', default='draft', required=True)
    procurement_orders = fields.One2many('purchase.order', 'joint_procurement_order_id', string='Procurement Orders')
    total_cost = fields.Float('Total Cost')
    cost_per_farm = fields.Float('Cost Per Participating Farm', compute='_compute_cost_per_farm', store=True)

    @api.depends('total_cost', 'coop_config_id.total_participating_farms')
    def _compute_cost_per_farm(self):
        for record in self:
            if record.coop_config_id.total_participating_farms > 0:
                record.cost_per_farm = record.total_cost / record.coop_config_id.total_participating_farms
            else:
                record.cost_per_farm = 0.0


