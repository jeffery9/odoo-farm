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

    sub_type = fields.Selection([
        ('bag', 'Weekly Bag'),
        ('adoption', 'Asset Adoption (认养)')
    ], string="Subscription Type", default='bag')
    
    # US-066-01: Adoption Linkage
    adopted_lot_id = fields.Many2one('stock.lot', string="Adopted Asset", 
                                    help="The specific animal or tree adopted by the customer.")

    # US-042: CSA Cooperative Credit Linkage
    coop_member_id = fields.Many2one('cooperative.member', string="Cooperative Member", help="The cooperative member backing this subscription's credit.")
    use_coop_credit = fields.Boolean("Use Cooperative Credit", default=False)
    credit_held_amount = fields.Float("Credit Held Amount", default=0.0)
    yield_token_balance = fields.Float("Yield Token Balance", default=0.0)
    credit_ledger_line_id = fields.Many2one('agri.clearing.ledger', string="Escrow Ledger Line", readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.csa.subscription') or _('CSA')
        return super().create(vals_list)

    def action_activate(self):
        from odoo.exceptions import ValidationError
        
        for sub in self:
            if sub.use_coop_credit:
                if not sub.coop_member_id:
                    raise ValidationError(_(
                        "COOP_MEMBER_REQUIRED: Cooperative member is required when coop credit is enabled. "
                        "(合作社授权必填：当启用合作社额度担保支付时，合作社成员字段必填。)"
                    ))
                
                # Check credit limit
                available_credit = sub.coop_member_id.credit_limit - sub.coop_member_id.credit_used
                if available_credit < sub.credit_held_amount:
                    raise ValidationError(_(
                        "COOP_CREDIT_INSUFFICIENT: Cooperative member credit is insufficient to back this subscription. "
                        "(合作社授信额度不足，无法激活此订阅担保。)"
                    ))
                
                # Create draft clearing ledger record
                ledger = self.env['agri.clearing.ledger'].create({
                    'partner_id': sub.partner_id.id,
                    'credit_change': -sub.credit_held_amount,
                    'description': f"CSA Pre-sale Credit Lock: {sub.name}",
                    'state': 'draft',
                    'source_ref': f"farm.csa.subscription,{sub.id}"
                })
                sub.credit_ledger_line_id = ledger.id

        self.write({'state': 'active'})
        for sub in self:
            if sub.sub_type == 'adoption' and sub.adopted_lot_id:
                sub.adopted_lot_id.message_post(body=_("ADOPTION: This asset has been adopted by %s.") % sub.partner_id.name)
                
                # 1. Provision Stream URL (Digital Twin Linkage)
                stream_url = f"https://stream.farm/csa/{sub.id}/{sub.adopted_lot_id.name}"
                sub.adopted_lot_id.write({
                    'csa_stream_url': stream_url,
                    'csa_adopter_id': sub.partner_id.id
                })
                
                # 2. Trigger Initial Care/Feeding Intervention
                # Find a generic service/feed product
                feed_product = self.env['product.product'].search([('name', '=', 'Standard Feed')], limit=1)
                if not feed_product:
                    feed_product = self.env['product.product'].create({'name': 'Standard Feed', 'type': 'consu'})
                    
                vals = {
                    'product_id': sub.adopted_lot_id.product_id.id,
                    'product_qty': 1.0,
                    'intervention_type': 'feeding',
                    'origin': f"CSA Adoption: {sub.name}",
                }
                if 'lot_producing_id' in self.env['mrp.production']._fields:
                    vals['lot_producing_id'] = sub.adopted_lot_id.id
                else:
                    vals['lot_producing_ids'] = [(4, sub.adopted_lot_id.id)]
                intervention = self.env['mrp.production'].create(vals)
                sub.message_post(body=_("Provisioned Video Stream: %s and scheduled initial Care Intervention: %s") % (stream_url, intervention.name))

    def _generate_delivery_tasks(self):
        """ 定时任务调用：为当天到期的订阅生成配送单 """
        today = fields.Date.today()
        active_subs = self.search([
            ('state', '=', 'active'),
            ('next_delivery_date', '<=', today)
        ])
        
        for sub in active_subs:
            # Token depletion check
            if sub.yield_token_balance <= 0.0:
                sub.message_post(body=_(
                    "CSA_TOKEN_EXHAUSTED: Pre-sale yield token balance is exhausted. Delivery suspended. "
                    "(提货代币已耗尽，本期自动发货暂停，请及时充值。)"
                ))
                # Skip creation of picking but postpone next delivery date to prevent spinning/looping
                days = 7
                if sub.plan_id.frequency == 'biweekly': days = 14
                if sub.plan_id.frequency == 'monthly': days = 30
                sub.next_delivery_date = sub.next_delivery_date + timedelta(days=days)
                continue

            # 创建库存移动 (Picking)
            picking_type = self.env['stock.picking.type'].search([('code', '=', 'outgoing')], limit=1)
            picking = self.env['stock.picking'].create({
                'partner_id': sub.partner_id.id,
                'picking_type_id': picking_type.id,
                'origin': sub.name,
                'location_id': picking_type.default_location_src_id.id,
                'location_dest_id': sub.partner_id.property_stock_customer.id,
                'move_ids': [(0, 0, {
                    'description_picking': sub.plan_id.product_id.name,
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

class FarmSharedTool(models.Model):
    """ US-066-02: Shared Tool Management for Urban/Community Farming """
    _name = 'farm.shared.tool'
    _description = 'Shared Agricultural Tool'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Tool Name", required=True)
    equipment_id = fields.Many2one('maintenance.equipment', string="Related Equipment")
    tool_type = fields.Selection([
        ('hand', 'Hand Tool'),
        ('power', 'Power Tool'),
        ('sensor', 'Portable Sensor')
    ], string="Type")
    
    status = fields.Selection([
        ('available', 'Available'),
        ('borrowed', 'In Use'),
        ('maintenance', 'Under Maintenance')
    ], default='available', tracking=True)
    
    current_user_id = fields.Many2one('res.partner', string="Current User")

    def action_borrow(self, partner_id):
        self.ensure_one()
        self.write({
            'status': 'borrowed',
            'current_user_id': partner_id
        })
        self.message_post(body=_("Tool borrowed by customer %s.") % self.current_user_id.name)

    def action_return(self):
        self.ensure_one()
        self.write({
            'status': 'available',
            'current_user_id': False
        })
        self.message_post(body=_("Tool returned and available for next user."))
