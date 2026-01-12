import unittest
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class TestLiveStreamingModule(TransactionCase):
    """
    测试直播模块功能 [US-21-01 至 US-21-07]
    """
    def setUp(self):
        super().setUp()
        
        # 创建测试数据
        self.douyin_account = self.env['douyin.account'].create({
            'name': 'Test Douyin Account',
            'app_id': 'test_app_id',
            'app_secret': 'test_app_secret',
        })
        
        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'type': 'product',
            'list_price': 50.0,
        })

    def test_douyin_account_creation(self):
        """测试抖音账号创建 [US-21-01]"""
        self.assertEqual(self.douyin_account.name, 'Test Douyin Account')
        self.assertEqual(self.douyin_account.app_id, 'test_app_id')

    def test_product_sync_creation(self):
        """测试产品同步记录创建 [US-21-02]"""
        product_sync = self.env['product.sync'].create({
            'product_id': self.product.id,
            'douyin_account_id': self.douyin_account.id,
        })
        
        self.assertEqual(product_sync.product_id, self.product)
        self.assertEqual(product_sync.douyin_account_id, self.douyin_account)
        self.assertEqual(product_sync.sync_status, 'not_synced')

    def test_live_session_creation(self):
        """测试直播会话创建 [US-21-03]"""
        live_session = self.env['live.streaming.session'].create({
            'name': 'Test Live Session',
            'douyin_account_id': self.douyin_account.id,
            'description': 'Test live streaming session for product showcase'
        })
        
        self.assertEqual(live_session.name, 'Test Live Session')
        self.assertEqual(live_session.douyin_account_id, self.douyin_account)
        self.assertEqual(live_session.status, 'planned')

    def test_live_order_creation(self):
        """测试直播订单创建 [US-21-04]"""
        live_order = self.env['live.order'].create({
            'name': 'TEST_ORDER_001',
            'douyin_order_id': 'DOUYIN_TEST_001',
            'douyin_account_id': self.douyin_account.id,
            'product_id': self.product.id,
            'quantity': 2.0,
            'unit_price': 50.0,
            'total_amount': 100.0,
            'customer_name': 'Test Customer',
            'customer_phone': '13800138000',
            'status': 'pending'
        })
        
        self.assertEqual(live_order.name, 'TEST_ORDER_001')
        self.assertEqual(live_order.status, 'pending')
        self.assertEqual(live_order.total_amount, 100.0)