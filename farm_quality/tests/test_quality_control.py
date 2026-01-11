from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestFarmQuality(TransactionCase):

    def setUp(self):
        super(TestFarmQuality, self).setUp()
        self.Point = self.env['farm.quality.point']
        self.Check = self.env['farm.quality.check']
        self.Lot = self.env['stock.lot']
        self.Product = self.env['product.product']
        
        self.apple = self.Product.create({'name': 'Organic Apple', 'type': 'product'})
        self.lot = self.Lot.create({'name': 'APP-2026-001', 'product_id': self.apple.id})

    def test_01_quality_point_and_check(self):
        """ 测试创建质量控制点并执行检查 [US-13, US-14] """
        # 1. 定义控制点：收获前农残检测
        point = self.Point.create({
            'name': 'Pesticide Residue Test',
            'product_id': self.apple.id,
            'test_type': 'pass_fail'
        })
        
        # 2. 生成检查记录
        check = self.Check.create({
            'point_id': point.id,
            'lot_id': self.lot.id,
            'test_type': 'pass_fail'
        })
        
        # 3. 提交结果：不通过
        check.action_fail()
        self.assertEqual(check.quality_state, 'fail')
        self.assertEqual(self.lot.quality_status, 'failed', "批次状态应自动更新为失败")

    def test_02_measurement_check(self):
        """ 测试数值测量型检查 [US-14] """
        point = self.Point.create({
            'name': 'Sugar Content (Brix)',
            'test_type': 'measure',
            'norm': 12.0,
            'tolerance_min': 10.0,
            'tolerance_max': 15.0
        })
        
        check = self.Check.create({
            'point_id': point.id,
            'lot_id': self.lot.id,
            'test_type': 'measure',
            'measure': 13.5
        })
        
        check.action_done()
        self.assertEqual(check.quality_state, 'pass', "13.5在10-15范围内，应通过")
