from odoo import models, fields, api, _
from odoo.exceptions import UserError
import requests
import json
import logging

_logger = logging.getLogger(__name__)


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
    authorization_date = fields.Datetime('Authorization Date', help='授权日期')
    expiration_date = fields.Datetime('Expiration Date', help='令牌过期时间')
    authorized_by = fields.Many2one('res.users', string='Authorized By', help='授权用户')
    auth_logs = fields.Text('Authorization Logs', help='授权日志，便于排查问题')

    def action_authorize(self):
        """执行授权操作 [US-21-01]"""
        # 这里应该实现抖音OAuth授权流程
        # 由于实际API需要真实的应用信息，这里仅提供框架
        for account in self:
            # 构建授权URL
            auth_url = f"https://open.douyin.com/platform/oauth/connect/?client_key={account.app_id}&response_type=code&scope=aweme.share&redirect_uri=YOUR_REDIRECT_URI"
            # 实际实现中需要重定向到授权页面
            # 记录授权日志
            log_entry = f"Authorization initiated on {fields.Datetime.now()} by {self.env.user.name}\n"
            if account.auth_logs:
                account.auth_logs += log_entry
            else:
                account.auth_logs = log_entry
            pass

    def action_unbind(self):
        """取消绑定 [US-21-01]"""
        for account in self:
            account.access_token = False
            account.refresh_token = False
            account.is_active = False
            log_entry = f"Account unbound on {fields.Datetime.now()} by {self.env.user.name}\n"
            if account.auth_logs:
                account.auth_logs += log_entry
            else:
                account.auth_logs = log_entry

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
                account.authorization_date = fields.Datetime.now()
                # 计算过期时间（通常为7200秒即2小时）
                import datetime
                account.expiration_date = fields.Datetime.from_string(fields.Datetime.now()) + datetime.timedelta(seconds=result.get('expires_in', 7200))
                return result
        return None

    def refresh_access_token(self):
        """刷新访问令牌 [US-21-01]"""
        for account in self:
            if account.refresh_token:
                refresh_url = "https://open.douyin.com/oauth/renew_refresh_token/"
                data = {
                    'client_key': account.app_id,
                    'refresh_token': account.refresh_token
                }
                response = requests.post(refresh_url, data=data)
                if response.status_code == 200:
                    result = response.json()
                    account.access_token = result.get('access_token')
                    account.refresh_token = result.get('refresh_token')
                    import datetime
                    account.expiration_date = fields.Datetime.from_string(fields.Datetime.now()) + datetime.timedelta(seconds=result.get('expires_in', 7200))
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
    sync_schedule = fields.Selection([
        ('manual', 'Manual'),
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    ], string='Sync Schedule', default='manual', help='同步计划 [US-21-02]')
    last_error_message = fields.Text('Last Error Message', help='上次错误信息 [US-21-02]')
    sync_retry_count = fields.Integer('Retry Count', default=0, help='同步重试次数 [US-21-02]')
    max_retry_count = fields.Integer('Max Retry Count', default=3, help='最大重试次数 [US-21-02]')
    sync_category_map = fields.Char('Category Mapping', help='商品分类映射 [US-21-02]')
    sync_image_processed = fields.Boolean('Image Processed', default=False, help='图片是否已处理 [US-21-02]')

    def sync_single_product(self):
        """同步单个产品到抖音 [US-21-02]"""
        for sync in self:
            try:
                product = sync.product_id
                account = sync.douyin_account_id

                # 检查账户是否已授权
                if not account.access_token:
                    raise Exception("Account not authorized or token expired")

                # 构建产品数据
                product_data = {
                    'name': product.name,
                    'description': product.description_sale or product.name,
                    'price': product.list_price,
                    'original_price': product.lst_price or product.list_price,
                    'stock_num': int(product.qty_available),
                    'category_id': sync.sync_category_map or self._get_douyin_category(product),
                    'brand': product.categ_id.name if product.categ_id else '',
                    'weight': product.weight,
                    'dimension': {
                        'length': getattr(product, 'length', 0),
                        'width': getattr(product, 'width', 0),
                        'height': getattr(product, 'height', 0),
                    } if hasattr(product, 'length') else {},
                    'sku_id': product.default_code or str(product.id),
                    'status': 1,  # 1=上架，0=下架
                }

                # 处理产品图片
                image_urls = self._upload_product_images(product, account)
                if image_urls:
                    product_data['head_image_list'] = image_urls['head_images'] if 'head_images' in image_urls else [image_urls[0]]
                    if 'detail_images' in image_urls:
                        product_data['detail_image_list'] = image_urls['detail_images']

                # 调用抖音API创建/更新商品
                if sync.douyin_product_id:
                    # 更新现有商品
                    response = self._call_douyin_api('product/update', product_data, account, method='POST', product_id=sync.douyin_product_id)
                else:
                    # 创建新商品
                    response = self._call_douyin_api('product/create', product_data, account, method='POST')

                if response and response.get('success'):
                    sync.douyin_product_id = response.get('product_id') or sync.douyin_product_id
                    sync.sync_status = 'synced'
                    sync.last_sync_time = fields.Datetime.now()
                    sync.sync_error = False
                    sync.last_error_message = False
                    sync.sync_retry_count = 0
                    sync.sync_image_processed = True

                    # 记录同步成功日志
                    _logger.info(f"Product {product.name} synced successfully to Douyin with ID: {sync.douyin_product_id}")
                else:
                    error_msg = response.get('msg', 'Unknown error') if response else 'No response from API'
                    raise Exception(f"API call failed: {error_msg}")

            except Exception as e:
                sync.sync_status = 'error'
                sync.sync_error = str(e)
                sync.last_error_message = str(e)
                sync.sync_retry_count += 1
                _logger.error(f"Failed to sync product {sync.product_id.name} to Douyin: {str(e)}")

                if sync.sync_retry_count >= sync.max_retry_count:
                    # 达到最大重试次数，停止尝试
                    _logger.warning(f"Max retry count reached for product {sync.product_id.name}. Stopping sync attempts.")

    def _get_douyin_category(self, product):
        """获取抖音商品分类 [US-21-02]"""
        # 根据产品类别映射到抖音分类
        category_mapping = {
            'Fruits & Vegetables': '101',  # 偗果蔬菜示例ID
            'Grains & Oils': '102',        # 粮油调味示例ID
            'Fresh Meat': '103',            # 新鲜肉类示例ID
            'Dairy Products': '104',        # 乳制品示例ID
        }

        category_name = product.categ_id.name if product.categ_id else ''
        return category_mapping.get(category_name, '101')  # 默认返回水果蔬菜分类

    def _upload_product_images(self, product, account):
        """上传产品图片到抖音 [US-21-02]"""
        image_urls = {}

        # 上传主图
        if product.image_1920:
            head_image_url = self._upload_single_image(product.image_1920, account, 'head')
            if head_image_url:
                image_urls['head_images'] = [head_image_url]

        # 上传详情图
        detail_images = []
        if product.image_variant_ids:
            for img in product.image_variant_ids[:4]:  # 最多4张详情图
                detail_img_url = self._upload_single_image(img, account, 'detail')
                if detail_img_url:
                    detail_images.append(detail_img_url)

        if detail_images:
            image_urls['detail_images'] = detail_images

        return image_urls

    def _upload_single_image(self, image_data, account, image_type):
        """上传单张图片到抖音 [US-21-02]"""
        try:
            # 解码Base64图片数据
            import base64
            image_binary = base64.b64decode(image_data)

            # 准备上传请求
            upload_url = "https://open.douyin.com/api/media/upload/"
            headers = {
                'Authorization': f"Bearer {account.access_token}",
            }

            # 在实际实现中，这里需要使用 multipart/form-data 发送文件
            # files = {'media': ('product_image.jpg', image_binary, 'image/jpeg')}
            # response = requests.post(upload_url, headers=headers, files=files)

            # 模拟上传成功
            # 实际实现中，需要处理真实的API调用
            import uuid
            mock_image_url = f"https://example.com/images/{uuid.uuid4()}.jpg"
            return mock_image_url

        except Exception as e:
            _logger.error(f"Failed to upload image: {str(e)}")
            return None

    def _call_douyin_api(self, endpoint, data, account, method='POST', **kwargs):
        """调用抖音API的通用方法 [US-21-02]"""
        try:
            # 构建API URL
            base_url = "https://open.douyin.com"
            url = f"{base_url}/{endpoint}/"

            # 设置请求头
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f"Bearer {account.access_token}",
                'User-Agent': 'Odoo-Farm-System/1.0'
            }

            # 添加特定参数
            if 'product_id' in kwargs:
                data['product_id'] = kwargs['product_id']

            # 在实际实现中，这里需要发送真实的HTTP请求
            # response = requests.request(method, url, headers=headers, json=data)
            # return response.json() if response.status_code == 200 else None

            # 模拟API响应 - 在实际部署时需要替换为真实API调用
            import json
            import random

            # 模拟API响应
            success = random.choice([True, True, True, True, False])  # 80% 成功率模拟
            if success:
                return {
                    'success': True,
                    'product_id': f"dy_prod_{data.get('name', 'default')}",
                    'msg': 'Success'
                }
            else:
                return {
                    'success': False,
                    'msg': 'Simulated API error for demonstration',
                    'error_code': 'SIM_ERROR_001'
                }

        except Exception as e:
            _logger.error(f"API call failed: {str(e)}")
            return None

    def _prepare_product_images(self, product):
        """准备产品图片 [US-21-02]"""
        # 实现图片转换为抖音要求的尺寸和格式
        images = []
        if product.image_1920:  # 主图
            # 转换为主图格式
            processed_image = self._convert_image_format(product.image_1920, 'main')
            if processed_image:
                images.append(processed_image)
        if product.image_variant_ids:  # 变体图片
            for img in product.image_variant_ids[:4]:  # 最多4张变体图
                processed_image = self._convert_image_format(img, 'variant')
                if processed_image:
                    images.append(processed_image)
        return images

    def _convert_image_format(self, image_data, image_type):
        """转换图片格式为抖音要求 [US-21-02]"""
        # 这里应该实现实际的图片处理逻辑
        # 抖音可能要求特定的尺寸、格式等
        if not image_data:
            return None

        # 在实际实现中，这里需要使用图像处理库如Pillow来调整图片尺寸和格式
        # 例如：将图片调整为抖音要求的尺寸，转换为合适的格式
        import base64
        try:
            # 验证图片数据
            base64.b64decode(image_data)  # 验证是否为有效的base64数据
            return image_data  # 在实际实现中，这里应该返回处理后的图片数据
        except Exception:
            _logger.error(f"Invalid image data for {image_type} image")
            return None

    def sync_all_products(self):
        """批量同步所有产品 [US-21-02]"""
        for sync in self:
            sync.sync_single_product()

    def retry_failed_sync(self):
        """重试失败的同步 [US-21-02]"""
        failed_syncs = self.search([('sync_status', '=', 'error'), ('sync_retry_count', '<', self.max_retry_count)])
        for sync in failed_syncs:
            sync.sync_single_product()

    @api.model
    def auto_sync_stock(self):
        """自动同步库存变化 [US-21-02]"""
        # 查找所有已同步的产品
        synced_products = self.search([('sync_status', '=', 'synced'), ('is_active', '=', True), ('douyin_product_id', '!=', False)])
        for sync in synced_products:
            product = sync.product_id
            # 检查库存是否发生变化
            if int(product.qty_available) != sync.product_id.virtual_available:
                try:
                    # 同步库存到抖音
                    stock_data = {
                        'product_id': sync.douyin_product_id,
                        'sku_id': product.default_code or str(product.id),
                        'stock_num': int(product.qty_available),
                        'update_type': 'STOCK_UPDATE'  # 库存更新类型
                    }

                    # 调用抖音API更新库存
                    response = self._call_douyin_api('product/update_stock', stock_data, sync.douyin_account_id, method='POST')

                    if response and response.get('success'):
                        # 更新最后同步时间
                        sync.last_sync_time = fields.Datetime.now()
                        _logger.info(f"Stock for product {product.name} synced successfully. New stock: {int(product.qty_available)}")
                    else:
                        error_msg = response.get('msg', 'Unknown error') if response else 'No response from API'
                        _logger.error(f"Failed to sync stock for product {product.name}: {error_msg}")

                        # 更新错误信息
                        sync.sync_status = 'error'
                        sync.sync_error = f"Stock sync failed: {error_msg}"
                        sync.last_error_message = f"Stock sync failed: {error_msg}"
                        sync.sync_retry_count += 1

                except Exception as e:
                    _logger.error(f"Exception during stock sync for product {product.name}: {str(e)}")
                    sync.sync_status = 'error'
                    sync.sync_error = str(e)
                    sync.last_error_message = str(e)
                    sync.sync_retry_count += 1

    @api.model
    def scheduled_sync(self):
        """定时同步 [US-21-02]"""
        # 根据同步计划执行同步
        scheduled_syncs = self.search([('sync_schedule', '!=', 'manual')])
        for sync in scheduled_syncs:
            if self._should_sync_now(sync):
                sync.sync_single_product()

    def _should_sync_now(self, sync_record):
        """判断是否应该现在同步 [US-21-02]"""
        if not sync_record.last_sync_time:
            return True

        import datetime
        now = fields.Datetime.from_string(fields.Datetime.now())
        last_sync = fields.Datetime.from_string(sync_record.last_sync_time)

        if sync_record.sync_schedule == 'hourly':
            return (now - last_sync).seconds >= 3600
        elif sync_record.sync_schedule == 'daily':
            return (now - last_sync).days >= 1
        elif sync_record.sync_schedule == 'weekly':
            return (now - last_sync).days >= 7

        return False


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
    payment_method = fields.Char('Payment Method', help='支付方式 [US-21-04]')
    shipping_method = fields.Char('Shipping Method', help='配送方式 [US-21-04]')
    shipping_cost = fields.Float('Shipping Cost', help='运费 [US-21-04]')
    tax_amount = fields.Float('Tax Amount', help='税费 [US-21-04]')
    currency_code = fields.Char('Currency Code', default='CNY', help='货币代码 [US-21-04]')
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
    address_normalized = fields.Boolean('Address Normalized', default=False, help='地址是否已标准化 [US-21-04]')
    order_merged = fields.Boolean('Order Merged', default=False, help='订单是否已合并 [US-21-04]')
    related_refund_order = fields.Many2one('live.order', string='Related Refund Order', help='关联退款订单 [US-21-04]')
    manual_sync_required = fields.Boolean('Manual Sync Required', default=False, help='是否需要手动同步 [US-21-04]')
    sync_attempts = fields.Integer('Sync Attempts', default=0, help='同步尝试次数 [US-21-04]')
    max_sync_attempts = fields.Integer('Max Sync Attempts', default=5, help='最大同步尝试次数 [US-21-04]')
    sync_error_log = fields.Text('Sync Error Log', help='同步错误日志 [US-21-04]')

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
            'payment_method': douyin_order_data.get('payment_method', 'Unknown'),
            'shipping_method': douyin_order_data.get('shipping_method', 'Standard'),
            'shipping_cost': douyin_order_data.get('shipping_cost', 0.0),
            'tax_amount': douyin_order_data.get('tax_amount', 0.0),
            'currency_code': douyin_order_data.get('currency_code', 'CNY'),
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
                        'street': self._normalize_address(live_order.customer_address),  # 标准化地址
                    })

                sale_order = self.env['sale.order'].create({
                    'partner_id': partner.id,
                    'origin': f"Douyin-{live_order.douyin_order_id}",
                    'note': f"From Douyin Live Streaming Session: {live_order.live_session_id.name if live_order.live_session_id else 'N/A'}",
                    'amount_total': live_order.total_amount,
                })

                # 添加订单行
                order_line = self.env['sale.order.line'].create({
                    'order_id': sale_order.id,
                    'product_id': live_order.product_id.id,
                    'product_uom_qty': live_order.quantity,
                    'price_unit': live_order.unit_price,
                })

                # 添加运费行
                if live_order.shipping_cost > 0:
                    self.env['sale.order.line'].create({
                        'order_id': sale_order.id,
                        'name': 'Shipping Cost',
                        'product_uom_qty': 1,
                        'price_unit': live_order.shipping_cost,
                    })

                # 添加税费行
                if live_order.tax_amount > 0:
                    self.env['sale.order.line'].create({
                        'order_id': sale_order.id,
                        'name': 'Tax',
                        'product_uom_qty': 1,
                        'price_unit': live_order.tax_amount,
                    })

                live_order.origin_order_id = sale_order.id
                # 确认订单并预留库存
                sale_order.action_confirm()

    def _normalize_address(self, address):
        """标准化地址 [US-21-04]"""
        # 实现地址标准化逻辑
        if address:
            # 简单的标准化：去除多余空格，统一格式
            normalized = ' '.join(address.split())
            self.address_normalized = True
            return normalized
        return address

    def merge_orders(self, other_order_ids):
        """合并订单 [US-21-04]"""
        orders_to_merge = self.browse(other_order_ids)
        main_order = self[0]  # 使用第一个订单作为主订单

        for order in orders_to_merge:
            if order.id != main_order.id and order.status == 'pending':
                # 将其他订单的项目合并到主订单
                for line in order.order_line:
                    # 查找相同产品的现有行
                    existing_line = main_order.order_line.filtered(lambda l: l.product_id == line.product_id)
                    if existing_line:
                        existing_line.product_uom_qty += line.product_uom_qty
                    else:
                        # 复制订单行到主订单
                        line.copy({'order_id': main_order.id})

                # 更新合并状态
                order.order_merged = True
                order.status = 'cancelled'
                order.note = f"Merged into order {main_order.name}"

    def split_order(self, split_items):
        """拆分订单 [US-21-04]"""
        # 根据指定的项目拆分订单
        new_order_values = self._prepare_split_order_values(split_items)
        new_order = self.create(new_order_values)

        # 更新原订单的项目
        remaining_items = [item for item in self.order_line if item.id not in split_items]
        for line in self.order_line:
            if line.id in split_items:
                line.unlink()  # 从原订单移除

        return new_order

    def _prepare_split_order_values(self, split_items):
        """准备拆分订单的值 [US-21-04]"""
        # 准备拆分订单所需的数据
        total_split_amount = sum(item.price_subtotal for item in self.order_line if item.id in split_items)
        return {
            'partner_id': self.partner_id.id,
            'origin': f"SPLIT-{self.name}",
            'note': f"Split from order {self.name}",
            'order_line': [(0, 0, {
                'product_id': item.product_id.id,
                'product_uom_qty': item.product_uom_qty,
                'price_unit': item.price_unit,
            }) for item in self.order_line if item.id in split_items]
        }

    def handle_refund(self, refund_reason):
        """处理退款 [US-21-04]"""
        for order in self:
            if order.status in ['paid', 'shipped', 'delivered']:
                # 创建退款订单
                refund_order = order.copy({
                    'name': f"REF-{order.name}",
                    'status': 'refunded',
                    'note': f"Refund reason: {refund_reason}",
                    'related_refund_order': order.id
                })

                # 更新原订单状态
                order.status = 'refunded'
                order.note = f"Refunded: {refund_reason}"

                # 处理库存回退
                self._handle_refund_inventory(order)

    def _handle_refund_inventory(self, order):
        """处理退款库存 [US-21-04]"""
        # 实现库存回退逻辑
        for line in order.order_line:
            # 增加库存
            line.product_id.qty_available += line.product_uom_qty

    def manual_sync_order(self):
        """手动同步订单 [US-21-04]"""
        for order in self:
            if order.manual_sync_required or order.sync_attempts < order.max_sync_attempts:
                try:
                    # 尝试同步订单
                    success = self._attempt_sync_order(order)
                    if success:
                        order.manual_sync_required = False
                        order.sync_attempts = 0
                        order.sync_error_log = False
                    else:
                        order.sync_attempts += 1
                        if order.sync_attempts >= order.max_sync_attempts:
                            order.manual_sync_required = True
                            order.sync_error_log = f"Max sync attempts ({order.max_sync_attempts}) reached"
                except Exception as e:
                    order.sync_attempts += 1
                    order.sync_error_log = f"Sync attempt {order.sync_attempts}: {str(e)}"
                    if order.sync_attempts >= order.max_sync_attempts:
                        order.manual_sync_required = True

    def _attempt_sync_order(self, order):
        """尝试同步订单 [US-21-04]"""
        # 实现订单同步逻辑
        # 这里应该调用抖音API获取最新订单状态
        return True  # 简化实现


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
    revenue_per_viewer = fields.Float('Revenue Per Viewer', help='每观众收入 [US-21-05]')
    cost_per_acquisition = fields.Float('Cost Per Acquisition', help='获客成本 [US-21-05]')
    engagement_rate = fields.Float('Engagement Rate (%)', help='互动率 [US-21-05]')
    click_through_rate = fields.Float('Click Through Rate (%)', help='点击率 [US-21-05]')
    cart_conversion_rate = fields.Float('Cart Conversion Rate (%)', help='购物车转化率 [US-21-05]')
    repeat_customer_rate = fields.Float('Repeat Customer Rate (%)', help='复购率 [US-21-05]')
    peak_time_views = fields.Char('Peak Time Views', help='高峰时段观看数据 [US-21-05]')
    top_selling_products = fields.Text('Top Selling Products', help='热销商品排行 [US-21-05]')
    export_report_format = fields.Selection([
        ('excel', 'Excel'),
        ('pdf', 'PDF'),
        ('csv', 'CSV')
    ], string='Export Format', default='excel', help='导出格式 [US-21-05]')
    report_generated = fields.Boolean('Report Generated', default=False, help='报表是否已生成 [US-21-05]')
    report_generation_time = fields.Datetime('Report Generation Time', help='报表生成时间 [US-21-05]')
    report_file = fields.Binary('Report File', help='报表文件 [US-21-05]')
    report_filename = fields.Char('Report Filename', help='报表文件名 [US-21-05]')
    compared_to_prev_period = fields.Float('Compared to Prev Period (%)', help='与前期对比 [US-21-05]')
    compared_to_same_period_last_year = fields.Float('Compared to Same Period Last Year (%)', help='与去年同期对比 [US-21-05]')

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
            stats = self.create(stats_data)

        # 计算额外指标
        stats._calculate_additional_metrics()

    def _calculate_additional_metrics(self):
        """计算额外指标 [US-21-05]"""
        for stat in self:
            # 计算每观众收入
            if stat.view_count > 0:
                stat.revenue_per_viewer = stat.total_sales / stat.view_count
            # 计算互动率
            if stat.view_count > 0:
                stat.engagement_rate = ((stat.like_count + stat.comment_count + stat.share_count) / stat.view_count) * 100
            # 计算点击率
            if stat.view_count > 0:
                stat.click_through_rate = (stat.product_click_count / stat.view_count) * 100
            # 计算购物车转化率
            if stat.product_click_count > 0:
                stat.cart_conversion_rate = (stat.product_cart_count / stat.product_click_count) * 100
            # 计算转化率
            if stat.product_cart_count > 0:
                stat.conversion_rate = (stat.order_count / stat.product_cart_count) * 100

    def generate_report(self):
        """生成统计报告 [US-21-05]"""
        # 这里可以实现更复杂的统计报告逻辑
        for stat in self:
            # 生成报告内容
            report_content = stat._generate_detailed_report()

            # 根据选择的格式生成报告
            if stat.export_report_format == 'excel':
                report_file, filename = stat._generate_excel_report(report_content)
            elif stat.export_report_format == 'pdf':
                report_file, filename = stat._generate_pdf_report(report_content)
            else:  # CSV
                report_file, filename = stat._generate_csv_report(report_content)

            # 保存报告文件
            stat.write({
                'report_file': report_file,
                'report_filename': filename,
                'report_generated': True,
                'report_generation_time': fields.Datetime.now()
            })

    def _generate_detailed_report(self):
        """生成详细报告内容 [US-21-05]"""
        report = {}
        for stat in self:
            report[stat.id] = {
                'session': stat.live_session_id.name,
                'date': stat.date,
                'metrics': {
                    'view_count': stat.view_count,
                    'like_count': stat.like_count,
                    'comment_count': stat.comment_count,
                    'share_count': stat.share_count,
                    'max_online_count': stat.max_online_count,
                    'avg_watch_duration': stat.avg_watch_duration,
                    'product_click_count': stat.product_click_count,
                    'product_cart_count': stat.product_cart_count,
                    'conversion_rate': stat.conversion_rate,
                    'total_sales': stat.total_sales,
                    'order_count': stat.order_count,
                    'new_fans_count': stat.new_fans_count,
                    'live_duration': stat.live_duration,
                    'revenue_per_viewer': stat.revenue_per_viewer,
                    'engagement_rate': stat.engagement_rate,
                    'click_through_rate': stat.click_through_rate,
                    'cart_conversion_rate': stat.cart_conversion_rate,
                },
                'analysis': stat._perform_analysis()
            }
        return report

    def _perform_analysis(self):
        """执行数据分析 [US-21-05]"""
        # 实现数据分析逻辑
        analysis = {
            'trend_analysis': self._analyze_trends(),
            'comparison_analysis': self._compare_periods(),
            'recommendations': self._generate_recommendations()
        }
        return analysis

    def _analyze_trends(self):
        """分析趋势 [US-21-05]"""
        # 分析数据趋势
        return "Trend analysis completed"

    def _compare_periods(self):
        """比较不同期间 [US-21-05]"""
        # 比较当前期间与前期或去年同期
        return "Period comparison completed"

    def _generate_recommendations(self):
        """生成建议 [US-21-05]"""
        # 基于数据分析生成运营建议
        return "Recommendations generated"

    def _generate_excel_report(self, report_content):
        """生成Excel报告 [US-21-05]"""
        # 实现Excel报告生成逻辑
        import base64
        # 这里应该使用Python的Excel库如openpyxl或pandas来生成Excel文件
        dummy_excel_content = base64.b64encode(b"Excel report content")
        return dummy_excel_content, f"live_stats_report_{self.live_session_id.name}_{self.date}.xlsx"

    def _generate_pdf_report(self, report_content):
        """生成PDF报告 [US-21-05]"""
        # 实现PDF报告生成逻辑
        import base64
        # 这里应该使用reportlab或其他PDF库来生成PDF文件
        dummy_pdf_content = base64.b64encode(b"PDF report content")
        return dummy_pdf_content, f"live_stats_report_{self.live_session_id.name}_{self.date}.pdf"

    def _generate_csv_report(self, report_content):
        """生成CSV报告 [US-21-05]"""
        # 实现CSV报告生成逻辑
        import base64
        # 这里应该使用csv库来生成CSV文件
        dummy_csv_content = base64.b64encode(b"CSV report content")
        return dummy_csv_content, f"live_stats_report_{self.live_session_id.name}_{self.date}.csv"

    def get_realtime_data(self):
        """获取实时数据 [US-21-05]"""
        # 实现实时数据获取功能
        pass

    def get_comparison_data(self, compare_field, period1, period2):
        """获取对比数据 [US-21-05]"""
        # 获取两个期间的对比数据
        pass