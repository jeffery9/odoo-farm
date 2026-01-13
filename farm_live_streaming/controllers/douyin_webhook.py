from odoo import http, _
from odoo.http import request
import json
import logging

_logger = logging.getLogger(__name__)

class DouyinWebhook(http.Controller):

    @http.route('/douyin/callback', type='http', auth='public', csrf=False)
    def douyin_oauth_callback(self, **kwargs):
        """ 处理授权后的 Code 回传 [US-21-01] """
        code = kwargs.get('code')
        state = kwargs.get('state') # 我们之前传的 account_id
        if code and state:
            account = request.env['douyin.account'].sudo().browse(int(state))
            # 实际生产中这里应通过 code 换取 access_token
            account.write({
                'access_token': 'mock_token_' + code,
                'state': 'authorized'
            })
            return "Authorization Successful! You can close this window."
        return "Authorization Failed."

    @http.route('/douyin/notification', type='json', auth='public', csrf=False)
    def douyin_order_notification(self):
        """
        US-21-04: 处理抖音订单实时回传 (Webhooks)
        """
        data = json.loads(request.httprequest.data)
        _logger.info("Douyin Webhook received: %s", data)
        
        event_type = data.get('event') # e.g. trade.Paid
        content = data.get('content', {})
        
        if event_type == 'trade.Paid':
            self._create_odoo_order(content)
            
        return {'err_no': 0, 'err_tips': 'success'}

    def _create_odoo_order(self, dy_order):
        """ 将抖音订单转化为 Odoo 订单 [US-21-04] """
        SaleOrder = request.env['sale.order'].sudo()
        # 1. 查找或创建客户
        partner = request.env['res.partner'].sudo().search([('name', '=', dy_order.get('buyer_name'))], limit=1)
        if not partner:
            partner = request.env['res.partner'].sudo().create({'name': dy_order.get('buyer_name')})
            
        # 2. 创建订单
        new_order = SaleOrder.create({
            'partner_id': partner.id,
            'client_order_ref': dy_order.get('order_id'), # 存储抖音订单号
            'order_line': [(0, 0, {
                'product_id': self._find_product(dy_order.get('item_id')),
                'product_uom_qty': dy_order.get('qty', 1),
                'price_unit': dy_order.get('amount', 0),
            })]
        })
        new_order.action_confirm()
        _logger.info("Douyin order %s converted to Odoo SO: %s", dy_order.get('order_id'), new_order.name)

    def _find_product(self, dy_item_id):
        # 根据抖音 Item ID 匹配 Odoo 产品
        mapping = request.env['douyin.product'].sudo().search([('douyin_item_id', '=', dy_item_id)], limit=1)
        return mapping.product_id.id if mapping else False
