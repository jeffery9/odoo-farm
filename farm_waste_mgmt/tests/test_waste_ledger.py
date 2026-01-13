from odoo.tests.common import TransactionCase

class TestWasteLedger(TransactionCase):

    def setUp(self):
        super(TestWasteLedger, self).setUp()
        self.Waste = self.env['farm.processing.waste']
        self.Product = self.env['product.product']

    def test_01_waste_disposal_record(self):
        """ 测试加工废弃物登记逻辑 [US-14-12] """
        peel = self.Product.create({'name': 'Apple Peel', 'type': 'consu'})
        waste = self.Waste.create({
            'product_id': peel.id,
            'quantity': 50.0,
            'disposal_method': 'field', # 还田
            'notes': 'Organic fertilizer for Zone C'
        })
        
        self.assertEqual(waste.disposal_method, 'field')
        self.assertTrue(waste.name.startswith('WST/')) # 验证序列号生成
