from odoo import models, fields, api, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    agri_task_ids = fields.One2many('project.task', 'sale_order_id', string="Farm Tasks")
    booking_ids = fields.One2many('farm.booking', 'sale_order_id', string="Farm Bookings")
    booking_count = fields.Integer(compute='_compute_booking_count')

    @api.depends('booking_ids')
    def _compute_booking_count(self):
        for order in self:
            order.booking_count = len(order.booking_ids)

    def action_confirm(self):
        # US-09-01: 提前期校验
        today = fields.Date.today()
        for order in self:
            for line in order.order_line:
                if line.product_id.growth_duration > 0:
                    # 检查承诺交货期是否足够
                    delivery_date = order.commitment_date or order.expected_date
                    if delivery_date:
                        days_to_delivery = (fields.Date.to_date(delivery_date) - today).days
                        if days_to_delivery < line.product_id.growth_duration:
                            # 弹出警告消息 (Odoo 19 支持在确认时抛出可忽略的警告或强制 UserError)
                            # 这里我们记录到消息流中，并弹出 UserError 以确保生产计划可行性
                            from odoo.exceptions import UserError
                            raise UserError(_("LEAD-TIME WARNING: Crop '%s' requires %s days to grow, but delivery is requested in %s days!") % (
                                line.product_id.name, line.product_id.growth_duration, days_to_delivery
                            ))

        res = super(SaleOrder, self).action_confirm()
        for order in self:
            for line in order.order_line:
                # 1. 需求驱动生产任务 [US-03-01]
                if line.product_id.is_variety:
                    self.env['project.task'].create({
                        'name': _('Demand: %s for %s') % (line.product_id.name, order.name),
                        'project_id': self.env['project.project'].search([('activity_family', '=', 'planting')], limit=1).id,
                        'description': _('Auto-generated from Sale Order %s. Quantity: %s') % (order.name, line.product_uom_qty),
                        'sale_order_id': order.id,
                    })
                
                # 2. 体验项目自动预约 [US-02-04]
                if line.product_id.is_experience_package:
                    self.env['farm.booking'].create({
                        'name': _('Booking for %s') % order.name,
                        'partner_id': order.partner_id.id,
                        'booking_date': fields.Date.today(),
                        'sale_order_id': order.id,
                        'booking_type': 'visit',
                    })
        return res

    def action_view_bookings(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("farm_agritourism.action_farm_booking")
        action['domain'] = [('sale_order_id', '=', self.id)]
        action['context'] = {'default_sale_order_id': self.id, 'default_partner_id': self.partner_id.id}
        return action

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_experience_package = fields.Boolean("Is Experience Package", default=False, help="Products like 'Family Day Package' which include bookings.")

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    lot_id = fields.Many2one(
        'stock.lot', 
        string="Production Lot",
        domain="[('product_id', '=', product_id)]"
    )