from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestExportCompliance(TransactionCase):

    def setUp(self):
        super(TestExportCompliance, self).setUp()
        self.SaleOrder = self.env['sale.order']
        self.Product = self.env['product.product']
        self.Country = self.env.ref('base.jp') # 日本作为示例
        
        # 创建一个产品并设置禁用农药记录 (Mock logic)
        self.rice = self.Product.create({
            'name': 'Export Rice',
            'type': 'product'
        })

    def test_01_export_restriction(self):
        """ 测试出口合规性拦截逻辑 [US-17-06] """
        # 模拟一份不合规的销售订单
        so = self.SaleOrder.create({
            'partner_id': self.env['res.partner'].create({'name': 'Tokyo Trader'}).id,
            'export_country_id': self.Country.id,
            'order_line': [(0, 0, {
                'product_id': self.rice.id,
                'product_uom_qty': 1000,
            })]
        })
        
        # 强制设置合规状态为 False (模拟校验失败)
        so.is_export_compliant = False
        
        # 尝试确认订单，应触发拦截
        with self.assertRaises(UserError):
            so.action_confirm()
            
        # 设置合规，允许确认
        so.is_export_compliant = True
        so.action_confirm()
        self.assertEqual(so.state, 'sale')
        # 验证积分是否增加 (来自 farm_marketing 继承的逻辑)
        self.assertTrue(so.partner_id.loyalty_points > 0)
