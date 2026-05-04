from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _name = 'sale.order' # Ensure name is present for safer inheritance check

    def action_confirm(self):
        """ US-009-01: Agricultural Lead-time verification """
        for order in self:
            if not hasattr(order, 'order_line'):
                continue
            for line in order.order_line:
                if hasattr(line.product_id, 'growth_duration') and line.product_id.growth_duration > 0 and order.commitment_date:
                    days_to_delivery = (order.commitment_date.date() - date.today()).days
                    if days_to_delivery < line.product_id.growth_duration:
                        raise UserError(_(
                            "Insufficient lead-time for product '%s'. "
                            "Required: %s days, Available: %d days."
                        ) % (line.product_id.name, line.product_id.growth_duration, days_to_delivery))
        return super(SaleOrder, self).action_confirm()
