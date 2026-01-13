from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class LiveOrder(models.Model):
    """
    US-21-04: 直播来源订单追踪
    职责：
    1. 下载：存储抖音原始报文快照。
    2. 导入：解析快照并转化为 Odoo 销售订单。
    """
    _name = 'live.order'
    _description = 'Live Stream Sales Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Order Reference", required=True)
    dy_order_id = fields.Char("Douyin Order ID", required=True, index=True)
    account_id = fields.Many2one('douyin.account', string="Account", required=True)
    session_id = fields.Many2one('live.streaming.session', string="Live Session")
    
    # 原始报文快照
    raw_data = fields.Text("Raw Data JSON")
    
    # 业务关联
    odoo_so_id = fields.Many2one('sale.order', string="Odoo Sales Order", readonly=True)
    buyer_nick = fields.Char("Buyer Name")
    amount_total = fields.Float("Order Amount")
    
    state = fields.Selection([
        ('draft', 'Downloaded'),
        ('imported', 'Imported'),
        ('failed', 'Error'),
        ('shipped', 'Shipped')
    ], default='draft', tracking=True)

    def action_view_odoo_so(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'res_id': self.odoo_so_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    # --- 步骤 1: 下载逻辑 ---
    @api.model
    def action_download_from_douyin(self, account_id):
        """ 仅负责从 API 拉取数据并建立快照记录 """
        account = self.env['douyin.account'].browse(account_id)
        endpoint = "/item/order/list/"
        params = {'count': 50, 'status': 'PAID'}
        
        response = account._do_douyin_request(endpoint, params=params, method='GET')
        orders_data = response.get('data', {}).get('orders', [])
        
        new_ids = []
        for dy_order in orders_data:
            existing = self.search([('dy_order_id', '=', dy_order['order_id'])], limit=1)
            if existing:
                continue
            
            import json
            vals = {
                'name': dy_order['order_id'],
                'dy_order_id': dy_order['order_id'],
                'account_id': account.id,
                'buyer_nick': dy_order.get('buyer_name', 'Douyin User'),
                'amount_total': dy_order.get('amount', 0),
                'raw_data': json.dumps(dy_order),
                'state': 'draft'
            }
            new_record = self.create(vals)
            new_ids.append(new_record.id)
            
        return len(new_ids)

    # --- 步骤 2: 导入逻辑 ---
    def action_import_to_odoo(self):
        """ 将已下载的快照批量转化为 Odoo 销售订单 """
        for rec in self.filtered(lambda r: r.state == 'draft'):
            try:
                import json
                dy_order = json.loads(rec.raw_data or '{}')
                
                # 1. 匹配产品
                mapping = self.env['douyin.product'].search([('douyin_item_id', '=', dy_order.get('item_id'))], limit=1)
                if not mapping:
                    rec.message_post(body=_("Import Failed: Product mapping not found for Item %s") % dy_order.get('item_id'))
                    rec.state = 'failed'
                    continue
                
                # 2. 执行创建 SO
                rec._create_sale_order(dy_order, mapping.product_id)
                
            except Exception as e:
                rec.state = 'failed'
                rec.message_post(body=_("Import Exception: %s") % str(e))

    def _create_sale_order(self, dy_order, product):
        """ 执行底层的 SO 创建逻辑 """
        partner = self.env['res.partner'].sudo().search([('name', '=', self.buyer_nick)], limit=1)
        if not partner:
            partner = self.env['res.partner'].sudo().create({'name': self.buyer_nick})
            
        so = self.env['sale.order'].sudo().create({
            'partner_id': partner.id,
            'origin': f"Douyin Live Sync: {self.name}",
            'client_order_ref': self.dy_order_id,
            'order_line': [(0, 0, {
                'product_id': product.id,
                'product_uom_qty': dy_order.get('qty', 1),
                'price_unit': dy_order.get('amount', 0),
            })]
        })
        so.action_confirm()
        self.write({'odoo_so_id': so.id, 'state': 'imported'})
        return so

    def action_sync_shipping_to_douyin(self, carrier_name, tracking_ref):
        """ 将发货状态回传到抖音 """
        self.ensure_one()
        if not self.dy_order_id or self.state != 'imported':
            return False
        
        res = self.account_id.action_confirm_shipping(self.dy_order_id, "OTHER", tracking_ref)
        if res.get('data', {}).get('error_code') == 0:
            self.write({'state': 'shipped'})
            return True
        return False

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        for picking in self:
            if picking.state == 'done' and picking.picking_type_code == 'outgoing' and picking.sale_id:
                live_orders = self.env['live.order'].search([
                    ('odoo_so_id', '=', picking.sale_id.id),
                    ('state', '=', 'imported')
                ])
                for order in live_orders:
                    order.action_sync_shipping_to_douyin(
                        picking.carrier_id.name or "Farm Express",
                        picking.carrier_tracking_ref or picking.name
                    )
        return res