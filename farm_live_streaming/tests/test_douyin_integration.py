from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from unittest.mock import patch
import json

class TestDouyinIntegration(TransactionCase):

    def setUp(self):
        super(TestDouyinIntegration, self).setUp()
        self.Account = self.env['douyin.account']
        self.ProductMapping = self.env['douyin.product']
        self.Product = self.env['product.product']
        self.Lot = self.env['stock.lot']
        
        # 1. Create a test account
        self.account = self.Account.create({
            'name': 'Test Douyin Shop',
            'client_key': 'mock_key',
            'client_secret': 'mock_secret',
            'state': 'draft'
        })
        
        # 2. Create a test product and lot with story
        self.product = self.Product.create({
            'name': 'Organic Tomato',
            'type': 'product',
            'list_price': 10.0
        })
        self.lot = self.Lot.create({
            'name': 'TOM-001',
            'product_id': self.product.id,
            'story_content': '<p>Grown with pure water.</p>'
        })

    @patch('requests.post')
    def test_01_token_exchange(self, mock_post):
        """ Test OAuth code to token exchange """
        # Mock successful response from Douyin
        mock_post.return_value.json.return_value = {
            'data': {
                'error_code': 0,
                'access_token': 'new_access_token',
                'refresh_token': 'new_refresh_token',
                'expires_in': 7200
            }
        }
        
        success = self.account._exchange_code_for_token('test_code')
        self.assertTrue(success)
        self.assertEqual(self.account.access_token, 'new_access_token')
        self.assertEqual(self.account.state, 'authorized')

    @patch('requests.post')
    def test_02_do_request_auto_refresh(self, mock_post):
        """ Test that request auto-refreshes on specific error codes """
        self.account.write({
            'access_token': 'old_token',
            'refresh_token': 'valid_refresh',
            'state': 'authorized'
        })
        
        # Mock first call failing with token expired (40002)
        # and second call (refresh) succeeding
        # and third call (retry) succeeding
        mock_post.side_effect = [
            # 1. Original request failure
            type('MockRes', (), {'json': lambda: {'data': {'error_code': 40002, 'description': 'Token Expired'}}}),
            # 2. Refresh token call success
            type('MockRes', (), {'json': lambda: {'data': {'error_code': 0, 'access_token': 'refreshed_token', 'expires_in': 7200}}}),
            # 3. Retried request success
            type('MockRes', (), {'json': lambda: {'data': {'error_code': 0, 'result': 'success'}}})
        ]
        
        res = self.account._do_douyin_request('/test/api')
        self.assertEqual(res.get('data', {}).get('result'), 'success')
        self.assertEqual(self.account.access_token, 'refreshed_token')

    @patch('requests.post')
    def test_03_product_sync(self, mock_post):
        """ Test product sync includes traceability story """
        self.account.write({'state': 'authorized', 'access_token': 'token'})
        
        mapping = self.ProductMapping.create({
            'account_id': self.account.id,
            'product_id': self.product.id
        })
        
        mock_post.return_value.json.return_value = {
            'data': {'error_code': 0, 'item_id': 'DY_ITEM_123'}
        }
        
        mapping.action_sync_to_douyin()
        
        self.assertEqual(mapping.douyin_item_id, 'DY_ITEM_123')
        self.assertEqual(mapping.sync_state, 'synced')
        
        # Check that the request contained the story
        args, kwargs = mock_post.call_args
        payload = kwargs.get('json', {})
        self.assertIn('Grown with pure water', payload.get('description'))

    def test_04_webhook_signature(self):
        """ Test HMAC-SHA256 signature verification """
        from odoo.addons.farm_live_streaming.controllers.douyin_webhook import DouyinWebhook
        webhook = DouyinWebhook()
        
        body = b'{"event": "test"}'
        secret = 'secret'
        
        import hmac
        import hashlib
        expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
        
        # Should pass with correct signature
        self.assertTrue(webhook._verify_signature(body, expected, secret))
        
        # Should fail with wrong signature
        self.assertFalse(webhook._verify_signature(body, 'wrong_sig', secret))
