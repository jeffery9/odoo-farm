from odoo.tests.common import TransactionCase
from datetime import date, timedelta

class TestCSASubscription(TransactionCase):

    def setUp(self):
        super(TestCSASubscription, self).setUp()
        self.Subscription = self.env['farm.csa.subscription']
        self.Partner = self.env['res.partner'].create({'name': 'CSA Member'})
        self.Product = self.env['product.product'].create({'name': 'Veggie Box', 'type': 'service'})

    def test_01_delivery_generation(self):
        """ 测试订阅周期性配送单生成逻辑 [US-08-02] """
        sub = self.Subscription.create({
            'name': 'SUB-001',
            'partner_id': self.Partner.id,
            'product_id': self.Product.id,
            'frequency': 'weekly',
            'start_date': date.today(),
            'state': 'active'
        })
        
        # 模拟生成下一次配送
        sub.action_generate_delivery()
        
        # 检查是否生成了调拨单
        picking = self.env['stock.picking'].search([('origin', '=', sub.name)])
        self.assertTrue(picking)
        self.assertEqual(picking.partner_id.id, self.Partner.id)
        
        # 验证下次配送日期是否自动推后 7 天
        expected_next = date.today() + timedelta(days=7)
        self.assertEqual(sub.next_delivery_date, expected_next)
