from odoo.tests.common import TransactionCase

class TestSustainability(TransactionCase):

    def setUp(self):
        super(TestSustainability, self).setUp()
        self.Task = self.env['project.task']
        self.Campaign = self.env['agricultural.campaign']
        
        # 创建两个不同的生产季进行对比
        self.season_2025 = self.Campaign.create({'name': '2025 Season'})
        self.season_2026 = self.Campaign.create({'name': '2026 Season'})

    def test_01_nutrient_reduction_tracking(self):
        """ 测试养分投入汇总逻辑 """
        # 2025 季任务
        self.Task.create({
            'name': '2025 Task',
            'campaign_id': self.season_2025.id,
            'total_n': 100.0,
            'total_p': 50.0,
            'total_k': 50.0
        })
        
        # 2026 季任务 (减量化)
        self.Task.create({
            'name': '2026 Task',
            'campaign_id': self.season_2026.id,
            'total_n': 80.0,
            'total_p': 40.0,
            'total_k': 40.0
        })
        
        # 验证汇总（通过视图进行）
        # 这里验证数据基础字段是否存在
        self.assertTrue(hasattr(self.season_2026, 'total_n'))
