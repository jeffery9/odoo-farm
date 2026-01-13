from odoo import models, fields, api, _
from datetime import timedelta

class FarmCSAPlan(models.Model):
    _name = 'farm.csa.plan'
    _description = 'CSA Subscription Plan'

    name = fields.Char("Plan Name", required=True)
    product_id = fields.Many2one('product.product', string="Default Product/Bag", required=True)
    frequency = fields.Selection([
        ('weekly', 'Weekly'),
        ('biweekly', 'Bi-weekly'),
        ('monthly', 'Monthly')
    ], string="Frequency", default='weekly', required=True)
    price = fields.Float("Price per Delivery")

class FarmCSASubscription(models.Model):
    _name = 'farm.csa.subscription'
    _description = 'Customer CSA Subscription'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Reference", required=True, copy=False, readonly=True, default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string="Customer", required=True)
    plan_id = fields.Many2one('farm.csa.plan', string="Plan", required=True)
    
    date_start = fields.Date("Start Date", default=fields.Date.today)
    next_delivery_date = fields.Date("Next Delivery Date", default=fields.Date.today)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('expired', 'Expired')
    ], string="Status", default='draft', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.csa.subscription') or _('CSA')
        return super().create(vals_list)

    def action_activate(self):
        self.write({'state': 'active'})

    def _generate_delivery_tasks(self):
        """ 定时任务调用：为当天到期的订阅生成配送单 """
        today = fields.Date.today()
        active_subs = self.search([
            ('state', '=', 'active'),
            ('next_delivery_date', '<=', today)
        ])
        
        for sub in active_subs:
            # 创建库存移动 (Picking)
            picking_type = self.env['stock.picking.type'].search([('code', '=', 'outgoing')], limit=1)
            picking = self.env['stock.picking'].create({
                'partner_id': sub.partner_id.id,
                'picking_type_id': picking_type.id,
                'origin': sub.name,
                'location_id': picking_type.default_location_src_id.id,
                'location_dest_id': sub.partner_id.property_stock_customer.id,
                'move_ids': [(0, 0, {
                    'name': sub.plan_id.product_id.name,
                    'product_id': sub.plan_id.product_id.id,
                    'product_uom_qty': 1.0,
                    'product_uom': sub.plan_id.product_id.uom_id.id,
                    'location_id': picking_type.default_location_src_id.id,
                    'location_dest_id': sub.partner_id.property_stock_customer.id,
                })]
            })
            
            # 计算下一次日期
            days = 7
            if sub.plan_id.frequency == 'biweekly': days = 14
            if sub.plan_id.frequency == 'monthly': days = 30
            
            sub.next_delivery_date = sub.next_delivery_date + timedelta(days=days)
            sub.message_post(body=_("Delivery task %s generated.") % picking.name)
