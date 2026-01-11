from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestFarmSupplyCompliance(TransactionCase):

    def setUp(self):
        super(TestFarmSupplyCompliance, self).setUp()
        self.Product = self.env['product.product']
        self.PurchaseOrder = self.env['purchase.order']
        self.Partner = self.env['res.partner'].create({'name': 'Agri Supplier'})
        
        # 创建一个未核准的剧毒农药
        self.pesticide = self.Product.create({
            'name': 'Banned Pesticide X',
            'type': 'product',
            'is_agri_input': True,
            'input_type': 'pesticide',
            'is_safety_approved': False
        })

    def test_01_prohibited_input_warning(self):
        """ 测试采购未核准投入品时的预警逻辑 """
        po = self.PurchaseOrder.create({
            'partner_id': self.Partner.id,
            'order_line': [(0, 0, {
                'product_id': self.pesticide.id,
                'product_qty': 10.0,
                'price_unit': 100.0,
            })]
        })
        
        # 验证 PO 行是否被标记为“不安全”
        self.assertTrue(po.order_line[0].is_compliance_warning)
