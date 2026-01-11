from odoo import models, fields, api

class SaleOrder(models.Model):
    # ... (原有代码)
    _inherit = 'sale.order'
    # ...

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    lot_id = fields.Many2one(
        'stock.lot', 
        string="Production Lot",
        domain="[('product_id', '=', product_id), ('state', '=', 'healthy'), ('is_safe_to_harvest', '=', True)]"
    )

    booking_ids = fields.One2many('farm.booking', 'sale_order_id', string="Farm Bookings")
    booking_count = fields.Integer(compute='_compute_booking_count')

    @api.depends('booking_ids')
    def _compute_booking_count(self):
        for order in self:
            order.booking_count = len(order.booking_ids)

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            for line in order.order_line:
                # 如果产品标记为品种（生物资产类）
                if line.product_id.is_variety:
                    self.env['project.task'].create({
                        'name': _('Demand: %s for %s') % (line.product_id.name, order.name),
                        'project_id': self.env['project.project'].search([('activity_family', '=', 'planting')], limit=1).id,
                        'description': _('Auto-generated from Sale Order %s. Quantity: %s') % (order.name, line.product_uom_qty),
                        'sale_order_id': order.id, # 建立关联
                    })
        return res

    def action_view_bookings(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("farm_agritourism.action_farm_booking")
        action['domain'] = [('sale_order_id', '=', self.id)]
        action['context'] = {'default_sale_order_id': self.id, 'default_partner_id': self.partner_id.id}
        return action
