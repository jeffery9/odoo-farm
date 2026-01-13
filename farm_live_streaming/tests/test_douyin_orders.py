from odoo.tests.common import TransactionCase
from unittest.mock import patch
import json

class TestDouyinOrders(TransactionCase):

    def setUp(self):
        super(TestDouyinOrders, self).setUp()
        self.Account = self.env['douyin.account']
        self.Mapping = self.env['douyin.product']
        self.LiveOrder = self.env['live.order']
        self.Product = self.env['product.product'].create({'name': 'Organic Rice', 'type': 'product'})
        
        # 1. Create account and mapping
        self.account = self.Account.create({
            'name': 'Farm Shop', 
            'client_key': 'abc', 
            'client_secret': '123',
            'state': 'authorized',
            'access_token': 'mock_token'
        })
        self.Mapping.create({
            'account_id': self.account.id,
            'product_id': self.Product.id,
            'douyin_item_id': 'DY-RICE-001'
        })

    @patch('odoo.addons.farm_live_streaming.models.douyin_account.DouyinAccount._do_douyin_request')
    def test_01_two_stage_sync(self, mock_request):
        """ Test the Download -> Import two-stage flow [US-21-04] """
        # 1. Mock the API response for order list
        mock_request.return_value = {
            'data': {
                'error_code': 0,
                'orders': [{
                    'order_id': 'DY_SEQ_001',
                    'buyer_name': 'Farmer Lee',
                    'item_id': 'DY-RICE-001',
                    'qty': 5,
                    'amount': 250.0
                }]
            }
        }
        
        # 2. Step 1: Download
        count = self.LiveOrder.action_download_from_douyin(self.account.id)
        self.assertEqual(count, 1)
        
        order_record = self.LiveOrder.search([('dy_order_id', '=', 'DY_SEQ_001')])
        self.assertTrue(order_record)
        self.assertEqual(order_record.state, 'draft')
        
        # 3. Step 2: Import
        order_record.action_import_to_odoo()
        
        self.assertEqual(order_record.state, 'imported')
        self.assertTrue(order_record.odoo_so_id)
        self.assertEqual(order_record.odoo_so_id.state, 'sale')
        self.assertEqual(order_record.odoo_so_id.order_line[0].product_qty, 5.0)

    def test_02_import_failure_mapping(self):
        """ Test import fails gracefully when mapping is missing """
        # Manually create a record with invalid item_id
        order = self.LiveOrder.create({
            'name': 'ERR-001',
            'dy_order_id': 'ERR-001',
            'account_id': self.account.id,
            'raw_data': json.dumps({'item_id': 'UNKNOWN_ITEM', 'order_id': 'ERR-001'}),
            'state': 'draft'
        })
        
        order.action_import_to_odoo()
        self.assertEqual(order.state, 'failed')
        self.assertIn('mapping not found', order.message_ids[0].body)