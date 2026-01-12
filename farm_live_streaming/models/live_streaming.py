from odoo import models, fields, api, _
from odoo.exceptions import UserError
import requests
import json


class DouyinAccount(models.Model):
    """
    抖音账号配置 [US-21-01]
    """
    _name = 'douyin.account'
    _description = 'Douyin Account Configuration'

    name = fields.Char('Account Name', required=True)
    app_id = fields.Char('App ID', help='抖音开放平台应用ID')
    app_secret = fields.Char('App Secret', help='抖音开放平台应用密钥')
    access_token = fields.Char('Access Token', help='OAuth授权后获取的访问令牌')
    refresh_token = fields.Char('Refresh Token', help='用于刷新访问令牌')
    is_active = fields.Boolean('Is Active', default=True)
    shop_id = fields.Char('Shop ID', help='抖音小店ID')
    live_room_ids = fields.Char('Live Room IDs', help='直播间ID列表')
    last_sync_time = fields.Datetime('Last Sync Time', help='最后同步时间')

    def action_authorize(self):
        """执行授权操作 [US-21-01]"""
        # 这里应该实现抖音OAuth授权流程
        # 由于实际API需要真实的应用信息，这里仅提供框架
        for account in self:
            # 构建授权URL
            auth_url = f"https://open.douyin.com/platform/oauth/connect/?client_key={account.app_id}&response_type=code&scope=aweme.share&redirect_uri=YOUR_REDIRECT_URI"
            # 实际实现中需要重定向到授权页面
            pass

    def get_access_token(self, auth_code):
        """通过授权码获取访问令牌"""
        for account in self:
            token_url = "https://open.douyin.com/oauth/access_token/"
            data = {
                'client_key': account.app_id,
                'client_secret': account.app_secret,
                'code': auth_code,
                'grant_type': 'authorization_code'
            }
            response = requests.post(token_url, data=data)
            if response.status_code == 200:
                result = response.json()
                account.access_token = result.get('access_token')
                account.refresh_token = result.get('refresh_token')
                return result
        return None


class LiveStreamingSession(models.Model):
    """
    直播会话 [US-21-03, US-21-06, US-21-07]
    """
    _name = 'live.streaming.session'
    _description = 'Live Streaming Session'

    name = fields.Char('Session Title', required=True)
    douyin_account_id = fields.Many2one('douyin.account', string='Douyin Account', required=True)
    start_time = fields.Datetime('Start Time')
    end_time = fields.Datetime('End Time')
    status = fields.Selection([
        ('planned', 'Planned'),
        ('live', 'Live'),
        ('ended', 'Ended'),
        ('archived', 'Archived')
    ], string='Status', default='planned')
    preview_url = fields.Char('Preview URL', help='直播预告链接')
    live_url = fields.Char('Live URL', help='直播链接')
    products = fields.Many2many('product.product', string='Products in Live')
    description = fields.Text('Description')
    view_count = fields.Integer('View Count', default=0, readonly=True)
    like_count = fields.Integer('Like Count', default=0, readonly=True)
    comment_count = fields.Integer('Comment Count', default=0, readonly=True)
    video_archive = fields.Binary('Video Archive', help='直播回放视频')
    archive_url = fields.Char('Archive URL', help='回放视频链接')
    
    def action_start_live(self):
        """开始直播 [US-21-03]"""
        for session in self:
            session.status = 'live'
            # 这里应该调用抖音API开始直播
            # 实际实现中需要与抖音直播API集成

    def action_end_live(self):
        """结束直播 [US-21-07]"""
        for session in self:
            session.status = 'ended'
            # 这里应该调用抖音API结束直播并获取回放
            # 实际实现中需要与抖音直播API集成

    def action_archive_live(self):
        """存档直播 [US-21-07]"""
        for session in self:
            session.status = 'archived'
            # 这里应该保存直播回放和统计数据


class ProductSync(models.Model):
    """
    产品同步管理 [US-21-02]
    """
    _name = 'product.sync'
    _description = 'Product Sync with Douyin'

    product_id = fields.Many2one('product.product', string='Product', required=True)
    douyin_account_id = fields.Many2one('douyin.account', string='Douyin Account', required=True)
    douyin_product_id = fields.Char('Douyin Product ID', help='抖音平台商品ID')
    sync_status = fields.Selection([
        ('not_synced', 'Not Synced'),
        ('syncing', 'Syncing'),
        ('synced', 'Synced'),
        ('error', 'Error')
    ], string='Sync Status', default='not_synced')
    last_sync_time = fields.Datetime('Last Sync Time')
    sync_error = fields.Text('Sync Error')
    is_active = fields.Boolean('Is Active', default=True)

    def sync_single_product(self):
        """同步单个产品到抖音 [US-21-02]"""
        for sync in self:
            try:
                product = sync.product_id
                # 构建产品数据
                product_data = {
                    'name': product.name,
                    'description': product.description_sale or product.name,
                    'price': product.list_price,
                    'stock_num': int(product.qty_available),
                    'category_id': '',  # 需要映射到抖音分类
                    'images': [],  # 产品图片
                }
                
                # 调用抖音API创建/更新商品
                # 这里需要实际的API调用
                # response = self.call_douyin_api('product/create', product_data, sync.douyin_account_id)
                
                sync.sync_status = 'synced'
                sync.last_sync_time = fields.Datetime.now()
                sync.sync_error = False
            except Exception as e:
                sync.sync_status = 'error'
                sync.sync_error = str(e)

    def sync_all_products(self):
        """批量同步所有产品 [US-21-02]"""
        for sync in self:
            sync.sync_single_product()

    @api.model
    def auto_sync_stock(self):
        """自动同步库存变化 [US-21-02]"""
        # 查找所有已同步的产品
        synced_products = self.search([('sync_status', '=', 'synced'), ('is_active', '=', True)])
        for sync in synced_products:
            product = sync.product_id
            # 检查库存是否发生变化
            if product.qty_available != sync.product_id.virtual_available:
                # 同步库存到抖音
                stock_data = {
                    'product_id': sync.douyin_product_id,
                    'stock_num': int(product.qty_available)
                }
                # 调用抖音API更新库存
                # response = self.call_douyin_api('product/update_stock', stock_data, sync.douyin_account_id)


class LiveOrder(models.Model):
    """
    直播订单 [US-21-04]
    """
    _name = 'live.order'
    _description = 'Order from Live Streaming'

    name = fields.Char('Order ID', required=True)
    douyin_order_id = fields.Char('Douyin Order ID', required=True)
    douyin_account_id = fields.Many2one('douyin.account', string='Douyin Account', required=True)
    origin_order_id = fields.Many2one('sale.order', string='Origin Sale Order')
    live_session_id = fields.Many2one('live.streaming.session', string='Live Session')
    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float('Quantity', required=True)
    unit_price = fields.Float('Unit Price', required=True)
    total_amount = fields.Float('Total Amount', required=True)
    customer_name = fields.Char('Customer Name')
    customer_phone = fields.Char('Customer Phone')
    customer_address = fields.Text('Customer Address')
    status = fields.Selection([
        ('pending', 'Pending Payment'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded')
    ], string='Status', default='pending')
    create_time = fields.Datetime('Create Time')
    pay_time = fields.Datetime('Pay Time')
    ship_time = fields.Datetime('Ship Time')
    receive_time = fields.Datetime('Receive Time')

    def sync_order_from_douyin(self, douyin_order_data):
        """从抖音同步订单 [US-21-04]"""
        order = self.create({
            'name': douyin_order_data.get('order_no'),
            'douyin_order_id': douyin_order_data.get('order_id'),
            'douyin_account_id': douyin_order_data.get('account_id'),
            'product_id': self.env['product.product'].search([('default_code', '=', douyin_order_data.get('product_code'))], limit=1).id,
            'quantity': douyin_order_data.get('quantity'),
            'unit_price': douyin_order_data.get('unit_price'),
            'total_amount': douyin_order_data.get('total_amount'),
            'customer_name': douyin_order_data.get('customer_name'),
            'customer_phone': douyin_order_data.get('customer_phone'),
            'customer_address': douyin_order_data.get('customer_address'),
            'status': self._map_douyin_status(douyin_order_data.get('status')),
            'create_time': douyin_order_data.get('create_time'),
        })
        return order

    def _map_douyin_status(self, douyin_status):
        """映射抖音订单状态到本地状态"""
        status_mapping = {
            'WAIT_BUYER_PAY': 'pending',
            'WAIT_SELLER_SEND_GOODS': 'paid',
            'WAIT_BUYER_CONFIRM_GOODS': 'shipped',
            'TRADE_SUCCESS': 'delivered',
            'TRADE_CLOSED': 'cancelled',
            'TRADE_CLOSED_BY_SYS': 'cancelled',
        }
        return status_mapping.get(douyin_status, 'pending')

    def create_sale_order(self):
        """创建内部销售订单 [US-21-04]"""
        for live_order in self:
            if not live_order.origin_order_id:
                # 创建对应的内部销售订单
                partner = self.env['res.partner'].search([('name', '=', live_order.customer_name)], limit=1)
                if not partner:
                    partner = self.env['res.partner'].create({
                        'name': live_order.customer_name,
                        'phone': live_order.customer_phone,
                        'street': live_order.customer_address,
                    })

                sale_order = self.env['sale.order'].create({
                    'partner_id': partner.id,
                    'origin': f"Douyin-{live_order.douyin_order_id}",
                    'note': f"From Douyin Live Streaming Session: {live_order.live_session_id.name if live_order.live_session_id else 'N/A'}",
                })

                # 添加订单行
                self.env['sale.order.line'].create({
                    'order_id': sale_order.id,
                    'product_id': live_order.product_id.id,
                    'product_uom_qty': live_order.quantity,
                    'price_unit': live_order.unit_price,
                })

                live_order.origin_order_id = sale_order.id
                # 确认订单并预留库存
                sale_order.action_confirm()


class LiveStatistics(models.Model):
    """
    直播统计数据 [US-21-05]
    """
    _name = 'live.statistics'
    _description = 'Live Streaming Statistics'

    live_session_id = fields.Many2one('live.streaming.session', string='Live Session', required=True)
    date = fields.Date('Date', required=True, default=fields.Date.context_today)
    view_count = fields.Integer('View Count', help='观看人数')
    like_count = fields.Integer('Like Count', help='点赞数')
    comment_count = fields.Integer('Comment Count', help='评论数')
    share_count = fields.Integer('Share Count', help='分享数')
    max_online_count = fields.Integer('Max Online Count', help='最高在线人数')
    avg_watch_duration = fields.Float('Avg Watch Duration (min)', help='平均观看时长（分钟）')
    product_click_count = fields.Integer('Product Click Count', help='商品点击次数')
    product_cart_count = fields.Integer('Product Cart Count', help='商品加购次数')
    conversion_rate = fields.Float('Conversion Rate (%)', help='转化率')
    total_sales = fields.Float('Total Sales', help='总销售额')
    order_count = fields.Integer('Order Count', help='订单数量')
    new_fans_count = fields.Integer('New Fans Count', help='新增粉丝数')
    live_duration = fields.Float('Live Duration (hours)', help='直播时长（小时）')

    @api.model
    def update_statistics(self, session_id, stats_data):
        """更新统计数据 [US-21-05]"""
        today = fields.Date.context_today(self)
        stats = self.search([
            ('live_session_id', '=', session_id),
            ('date', '=', today)
        ], limit=1)

        if stats:
            stats.write(stats_data)
        else:
            stats_data['live_session_id'] = session_id
            stats_data['date'] = today
            self.create(stats_data)

    def generate_report(self):
        """生成统计报告 [US-21-05]"""
        # 这里可以实现更复杂的统计报告逻辑
        pass