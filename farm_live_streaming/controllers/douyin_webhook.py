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
        state = kwargs.get('state')
        if code and state:
            account = request.env['douyin.account'].sudo().browse(int(state))
            if account._exchange_code_for_token(code):
                return "Authorization Successful! Access tokens saved."
        return "Authorization Failed."

    @http.route('/douyin/notification', type='json', auth='public', csrf=False)
    def douyin_order_notification(self):
        """
        US-21-04: 真实的抖音 Webhook 接收
        包含签名校验 logic
        """
        data = json.loads(request.httprequest.data)
        signature = request.httprequest.headers.get('X-Douyin-Signature')
        
        # 寻找对应的账号进行校验
        # 注意：这里可能需要根据 data 里的特定 ID 先定位 client_secret
        account = request.env['douyin.account'].sudo().search([], limit=1)
        
        if not self._verify_signature(request.httprequest.data, signature, account.client_secret):
            _logger.warning("Douyin Webhook: Invalid Signature detected!")
            return {'err_no': 4001, 'err_tips': 'invalid signature'}

        event_type = data.get('event')
        content = data.get('content', {})
        
        if event_type == 'trade.Paid':
            self._create_odoo_order(content)
            
        return {'err_no': 0, 'err_tips': 'success'}

    def _verify_signature(self, body, signature, client_secret):
        """ 抖音 Webhook 签名校验算法 """
        if not signature: return False
        import hmac
        import hashlib
        # 抖音签名规范通常是将 body 与 secret 进行 hmac
        # 实际代码需根据抖音开放平台具体版本的签名文档微调
        expected = hmac.new(client_secret.encode(), body, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)

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
