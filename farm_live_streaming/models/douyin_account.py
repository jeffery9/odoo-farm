from odoo import models, fields, api, _
from odoo.exceptions import UserError
import requests
import datetime
import logging

_logger = logging.getLogger(__name__)

class DouyinAccount(models.Model):
    """
    US-21-01: 抖音账号与授权中心
    职责：管理 API 凭据、处理 OAuth 流程、维护令牌生命周期
    """
    _name = 'douyin.account'
    _description = 'Douyin Enterprise Account'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Account Nickname", required=True)
    client_key = fields.Char("Client Key (App ID)", required=True)
    client_secret = fields.Char("Client Secret", required=True, password=True)
    shop_id = fields.Char("Shop ID (抖音小店ID)")
    
    # OAuth 令牌管理
    access_token = fields.Char("Access Token", readonly=True)
    refresh_token = fields.Char("Refresh Token", readonly=True)
    token_expiry = fields.Datetime("Token Expiry", readonly=True)
    
    state = fields.Selection([
        ('draft', 'Unauthorized'),
        ('authorized', 'Authorized'),
        ('expired', 'Expired')
    ], default='draft', tracking=True)

    # US-21-01: 监控增强
    health_status = fields.Selection([
        ('healthy', 'Healthy'),
        ('warning', 'Expiring Soon'),
        ('error', 'Auth Failed'),
    ], string="Health Status", compute='_compute_health_status', store=True)
    
    last_health_check = fields.Datetime("Last Check")
    responsible_user_id = fields.Many2one('res.users', string="Responsible", default=lambda self: self.env.user)

    @api.depends('token_expiry', 'state')
    def _compute_health_status(self):
        now = datetime.datetime.now()
        for rec in self:
            if rec.state != 'authorized' or not rec.token_expiry:
                rec.health_status = 'error'
                continue
            
            diff = (rec.token_expiry - now).total_seconds()
            if diff < 0:
                rec.health_status = 'error'
            elif diff < 86400: # 24小时内过期
                rec.health_status = 'warning'
            else:
                rec.health_status = 'healthy'

    def action_verify_connection(self):
        """ 自动验证 API 连通性 """
        self.ensure_one()
        # 调用简单的个人信息接口测试 Token 有效性
        res = self._do_douyin_request("/oauth/userinfo/", method='GET')
        self.last_health_check = fields.Datetime.now()
        
        if res.get('data', {}).get('error_code') == 0:
            self.message_post(body=_("Health Check: Connection Successful. Account: %s") % res['data'].get('nickname'))
            return True
        else:
            self.state = 'expired'
            self._create_expiry_activity()
            return False

    def _cron_monitor_accounts(self):
        """ 定时任务：扫描并预警所有账号状态 """
        accounts = self.search([('state', '=', 'authorized')])
        for account in accounts:
            account.action_verify_connection()
            if account.health_status == 'warning':
                account._create_expiry_activity(_("Douyin token for %s will expire within 24 hours. Please re-authorize.") % account.name)

    def _create_expiry_activity(self, note=False):
        """ 创建预警活动 """
        self.ensure_one()
        if not self.responsible_user_id: return
        
        existing = self.env['mail.activity'].search([
            ('res_model_id', '=', self.env.ref('farm_live_streaming.model_douyin_account').id),
            ('res_id', '=', self.id),
            ('activity_type_id', '=', self.env.ref('mail.mail_activity_data_todo').id),
            ('state', '!=', 'done')
        ])
        if not existing:
            self.activity_schedule(
                'mail.mail_activity_data_todo',
                note=note or _("Douyin authorization has expired. Integration is suspended."),
                user_id=self.responsible_user_id.id,
                summary=_("Action Required: Douyin Auth")
            )

    # --- 授权逻辑 (Auth Logic) ---

    def action_authorize(self):
        """ 生成抖音 OAuth 授权链接 """
        base_url = "https://open.douyin.com/platform/oauth/connect/"
        redirect_uri = self.env['ir.config_parameter'].sudo().get_param('web.base.url') + '/douyin/callback'
        scope = "user_info,item.list,dy.order.list,im"
        return {
            'type': 'ir.actions.act_url',
            'url': f"{base_url}?client_key={self.client_key}&response_type=code&scope={scope}&redirect_uri={redirect_uri}&state={self.id}",
            'target': 'new',
        }

    def _exchange_code_for_token(self, code):
        """ Code 换 Access Token """
        url = "https://open.douyin.com/oauth/access_token/"
        payload = {
            'client_key': self.client_key,
            'client_secret': self.client_secret,
            'code': code,
            'grant_type': 'authorization_code',
        }
        return self._process_token_response(requests.post(url, data=payload, timeout=10))

    def _refresh_access_token(self):
        """ 刷新 Access Token """
        url = "https://open.douyin.com/oauth/renew_refresh_token/"
        payload = {
            'client_key': self.client_key,
            'refresh_token': self.refresh_token,
        }
        return self._process_token_response(requests.post(url, data=payload, timeout=10))

    def _process_token_response(self, response):
        """ 统一处理 Token 响应数据 """
        try:
            res_data = response.json().get('data', {})
            if res_data.get('error_code') == 0:
                expiry = datetime.datetime.now() + datetime.timedelta(seconds=res_data.get('expires_in', 7200))
                self.write({
                    'access_token': res_data.get('access_token'),
                    'refresh_token': res_data.get('refresh_token'),
                    'token_expiry': expiry,
                    'state': 'authorized'
                })
                return True
        except Exception as e:
            _logger.error("Douyin Token Process Failed: %s", e)
        return False

    # --- 通讯逻辑 (Transport Logic) ---

    def _execute_request(self, endpoint, params=None, method='POST'):
        """ 
        【传输层】职责：纯粹的网络通讯
        不做 Token 检查，不做重试
        """
        base_url = "https://open.douyin.com"
        headers = {'access-token': self.access_token}
        if method == 'GET':
            return requests.get(base_url + endpoint, params=params, headers=headers, timeout=10).json()
        return requests.post(base_url + endpoint, json=params, headers=headers, timeout=10).json()

    def _do_douyin_request(self, endpoint, params=None, method='POST'):
        """ 
        【调度层】职责：编排请求流程
        实现：Token 预检 -> 执行 -> 失效重试
        """
        self.ensure_one()
        
        # 1. 预检 Token
        now = datetime.datetime.now()
        if self.token_expiry and (self.token_expiry - now).total_seconds() < 300:
            self._refresh_access_token()

        # 2. 执行请求
        res = self._execute_request(endpoint, params, method)
        
        # 3. 错误处理与被动刷新重试
        error_code = res.get('data', {}).get('error_code')
        if error_code in [40002, 2190008]: # 令牌失效错误码
            _logger.warning("Token expired during request, attempting refresh...")
            if self._refresh_access_token():
                res = self._execute_request(endpoint, params, method)
        
        return res

    # --- 业务原子接口 (Business Atomic APIs) ---

    def action_confirm_shipping(self, dy_order_id, logistics_code, tracking_no):
        """ 回传发货信息 """
        payload = {'order_id': dy_order_id, 'logistics_code': logistics_code, 'tracking_no': tracking_no}
        return self._do_douyin_request("/item/order/logistics/confirm/", params=payload)

    def action_get_live_stats(self, room_id):
        """ 获取直播间统计 """
        return self._do_douyin_request("/api/live/room/data/", params={'room_id': room_id}, method='GET')

    def action_get_live_replay(self, room_id):
        """ 获取直播回放 """
        return self._do_douyin_request("/api/live/room/replay/", params={'room_id': room_id}, method='GET')

    def action_sync_orders(self):
        """ 订单同步编排逻辑 """
        self.ensure_one()
        LiveOrder = self.env['live.order']
        count = LiveOrder.action_download_from_douyin(self.id)
        pending_orders = LiveOrder.search([('account_id', '=', self.id), ('state', '=', 'draft')])
        pending_orders.action_import_to_odoo()
        self.message_post(body=_("Order sync completed: %s downloaded, %s imported.") % (count, len(pending_orders)))
        return True