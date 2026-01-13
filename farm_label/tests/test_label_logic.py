from odoo.tests.common import TransactionCase

class TestLabelLogic(TransactionCase):

    def setUp(self):
        super(TestLabelLogic, self).setUp()
        self.Lot = self.env['stock.lot']
        self.Product = self.env['product.product']

    def test_01_qr_url_quoting(self):
        """ 测试溯源 URL 的正确转义以确保二维码生成安全 """
        lot = self.Lot.create({
            'name': 'LOT/2026/001',
            'product_id': self.env.ref('product.product_delivery_01', raise_if_not_found=False).id or 1,
        })
        # 模拟设置 traceability_url
        lot.traceability_url = "http://farm.com/trace?lot=LOT/2026/001&auth=true"
        
        quoted_url = lot.get_qr_quoted_traceability_url()
        # 验证特殊字符是否被转义
        self.assertNotIn(' ', quoted_url)
        self.assertIn('%2F', quoted_url) # '/'
        self.assertIn('%3F', quoted_url) # '?'
