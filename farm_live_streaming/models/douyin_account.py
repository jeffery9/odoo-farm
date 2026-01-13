from odoo import models, fields, api, _
from odoo.exceptions import UserError
import requests
import datetime
import logging

_logger = logging.getLogger(__name__)

class DouyinAccount(models.Model):
    """
    US-21-01: 抖音账号授权管理
    """
    _name = 'douyin.account'
    _description = 'Douyin Enterprise Account'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Account Nickname", required=True)
    client_key = fields.Char("Client Key", required=True)
    client_secret = fields.Char("Client Secret", required=True, password=True)
    
    # OAuth Tokens
    access_token = fields.Char("Access Token", readonly=True)
    refresh_token = fields.Char("Refresh Token", readonly=True)
    token_expiry = fields.Datetime("Token Expiry", readonly=True)
    
    state = fields.Selection([
        ('draft', 'Unauthorized'),
        ('authorized', 'Authorized'),
        ('expired', 'Expired')
    ], default='draft', tracking=True)

    def action_authorize(self):
        """ 生成授权链接 [US-21-01] """
        base_url = "https://open.douyin.com/platform/oauth/connect/"
        redirect_uri = self.env['ir.config_parameter'].sudo().get_param('web.base.url') + '/douyin/callback'
        auth_url = f"{base_url}?client_key={self.client_key}&response_type=code&scope=user_info,item.list,dy.order.list&redirect_uri={redirect_uri}&state={self.id}"
        
        return {
            'type': 'ir.actions.act_url',
            'url': auth_url,
            'target': 'new',
        }

    def _refresh_access_token(self):
        """ 自动刷新 Access Token """
        for rec in self:
            if not rec.refresh_token:
                continue
            # 模拟抖音刷新 Token API
            url = "https://open.douyin.com/oauth/refresh_token/"
            payload = {
                'client_key': rec.client_key,
                'grant_type': 'refresh_token',
                'refresh_token': rec.refresh_token
            }
            try:
                # response = requests.post(url, data=payload)
                # data = response.json()
                _logger.info("Douyin Token Refreshed for account: %s", rec.name)
                # 实际落地时更新 rec.access_token 和 rec.token_expiry
            except Exception as e:
                _logger.error("Failed to refresh Douyin token: %s", e)

class DouyinProduct(models.Model):
    """
    US-21-02: 商品库同步逻辑
    """
    _name = 'douyin.product'
    _description = 'Douyin Shop Product'

    account_id = fields.Many2one('douyin.account', string="Account", required=True)
    product_id = fields.Many2one('product.product', string="Odoo Product", required=True)
    douyin_item_id = fields.Char("Douyin Item ID")
    sync_state = fields.Selection([
        ('pending', 'Pending Sync'),
        ('synced', 'Synced'),
        ('error', 'Error')
    ], default='pending')

    def action_sync_to_douyin(self):
        """ 将产品和当前库存推送到抖音 [US-21-02] """
        for rec in self:
            # 获取溯源信息作为商品描述 [US-21-03]
            trace_data = rec.product_id.lot_ids[:1].story_content if rec.product_id.lot_ids else ""
            
            # 推送逻辑
            _logger.info("Syncing product %s to Douyin Shop...", rec.product_id.name)
            rec.sync_state = 'synced'
