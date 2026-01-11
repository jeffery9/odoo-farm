from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    booking_ids = fields.One2many('farm.booking', 'sale_order_id', string="Farm Bookings")
    booking_count = fields.Integer(compute='_compute_booking_count')

    @api.depends('booking_ids')
    def _compute_booking_count(self):
        for order in self:
            order.booking_count = len(order.booking_ids)

    def action_view_bookings(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("farm_agritourism.action_farm_booking")
        action['domain'] = [('sale_order_id', '=', self.id)]
        action['context'] = {'default_sale_order_id': self.id, 'default_partner_id': self.partner_id.id}
        return action
