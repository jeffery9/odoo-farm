from odoo import models, fields, api

class FarmPartner(models.Model):
    _inherit = 'res.partner'

    loyalty_points = fields.Float("Farm Loyalty Points", default=0.0)

class FarmSaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(FarmSaleOrder, self).action_confirm()
        for order in self:
            # 简单规则：1元 = 1分
            points = order.amount_total
            order.partner_id.loyalty_points += points
            order.message_post(body=_("LOYALTY: %s points added to customer.") % points)
        return res

class FarmSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def action_view_traceability(self):
        """ 跳转到该行关联批次的外部溯源页面 """
        self.ensure_one()
        # 寻找已分配的批次 (从库存移动中找)
        move = self.move_ids.filtered(lambda m: m.state == 'done')
        lot = move.lot_ids[:1]
        if lot:
            return {
                'type': 'ir.actions.act_url',
                'url': lot.traceability_url,
                'target': 'new',
            }
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('No Lot Assigned'),
                'message': _('Traceability is available after delivery confirmation.'),
                'type': 'warning',
            }
        }

class FarmLotMarketing(models.Model):
    _inherit = 'stock.lot'

    traceability_url = fields.Char("Traceability URL", compute='_compute_traceability_url')
    
    # Marketing Content [US-25]
    story_title = fields.Char("Growth Story Title")
    story_content = fields.Html("Growth Story Content")
    marketing_image_ids = fields.Many2many('ir.attachment', string="Marketing Photos")
    
    # 溯源面板显示的指标快照
    avg_temp = fields.Float("Average Growth Temperature (℃)")
    water_purity = fields.Char("Water Purity Grade")

    def _compute_traceability_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for lot in self:
            lot.traceability_url = f"{base_url}/farm/trace/{lot.name}"
