from odoo.tests.common import TransactionCase
from datetime import date, timedelta

class TestCertificationLogic(TransactionCase):

    def setUp(self):
        super(TestCertificationLogic, self).setUp()
        self.Location = self.env['stock.location']

    def test_01_organic_conversion_progress(self):
        """ 测试有机转换进度计算与自动升级 [US-12-02] """
        today = date.today()
        # 创建一个 2 年前（约 730 天）开始转换的地块，目标 1095 天（3年）
        start_date = today - timedelta(days=730)
        parcel = self.Location.create({
            'name': 'Organic Field 1',
            'certification_level': 'organic_transition',
            'conversion_start_date': start_date,
            'conversion_target_days': 1000 
        })
        
        parcel._compute_conversion_progress()
        # 730 / 1000 = 73%
        self.assertEqual(parcel.conversion_progress, 73.0)
        self.assertEqual(parcel.certification_level, 'organic_transition')

        # 模拟达到 100% 进度
        parcel.conversion_start_date = today - timedelta(days=1001)
        parcel._compute_conversion_progress()
        self.assertEqual(parcel.conversion_progress, 100.0)
        # 验证自动升级状态
        self.assertEqual(parcel.certification_level, 'organic')

    def test_02_conversion_reset_on_violation(self):
        """ 测试使用违禁投入品后转换进度重置 """
        today = date.today()
        parcel = self.Location.create({
            'name': 'Organic Field 2',
            'certification_level': 'organic_transition',
            'conversion_start_date': today - timedelta(days=500),
            'conversion_target_days': 1000
        })
        
        # 初始进度 50%
        parcel._compute_conversion_progress()
        self.assertEqual(parcel.conversion_progress, 50.0)
        
        # 记录今天使用了违禁品
        parcel.last_prohibited_substance_date = today
        parcel._compute_conversion_progress()
        
        # 进度应归零，因为今天重置了
        self.assertEqual(parcel.conversion_progress, 0.0)
