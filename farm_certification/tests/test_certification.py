from odoo.tests.common import TransactionCase
from odoo import fields
from datetime import timedelta

class TestFarmCertification(TransactionCase):

    def setUp(self):
        super(TestFarmCertification, self).setUp()
        self.Location = self.env['stock.location']
        self.Lot = self.env['stock.lot']
        self.Product = self.env['product.product']
        
        # 1. 创建处于“有机转换期”的地块
        self.conversion_start = fields.Date.today() - timedelta(days=400) # 已转换1年多
        self.plot = self.Location.create({
            'name': 'Organic Plot A',
            'is_land_parcel': True,
            'certification_level': 'organic_transition',
            'conversion_start_date': self.conversion_start
        })

    def test_01_certification_inheritance(self):
        """ 测试收获批次自动继承地块的认证等级 """
        apple = self.Product.create({'name': 'Apple', 'type': 'product'})
        lot = self.Lot.create({
            'name': 'APPLE-LOT-001',
            'product_id': apple.id,
            'location_id': self.plot.id
        })
        
        # 更新逻辑，使其继承地块状态
        lot._onchange_location_id_certification()
        self.assertEqual(lot.certification_level, 'organic_transition')

    def test_02_conversion_status(self):
        """ 测试转换期进度计算 """
        # 假设有机转换期要求是 3 年 (1095天)
        self.plot.conversion_target_days = 1095
        self.assertEqual(self.plot.conversion_progress, 400/1095 * 100)
