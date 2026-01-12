from odoo.tests.common import TransactionCase

class TestFarmCostAccounting(TransactionCase):

    def setUp(self):
        super(TestFarmCostAccounting, self).setUp()
        self.Task = self.env['project.task']
        self.AnalyticAccount = self.env['account.analytic.account']
        self.Campaign = self.env['agricultural.campaign'].create({'name': '2026 Test Season'})

    def test_01_automatic_analytic_account_creation(self):
        """ 测试创建生产任务时自动生成辅助核算账户 [US-04-02] """
        task = self.Task.create({
            'name': 'Cost Test Task',
            'campaign_id': self.Campaign.id,
        })
        
        # 验证辅助核算账户是否已创建并关联
        self.assertTrue(task.analytic_account_id, "生产任务应自动关联辅助核算账户")
        self.assertEqual(task.analytic_account_id.name, task.name)
        self.assertEqual(task.analytic_account_id.plan_id.name, 'Agri-Projects', "应属于农业项目计划")

    def test_02_cost_aggregation_logic(self):
        """ 测试成本归集逻辑（模拟） [US-04-02] """
        task = self.Task.create({'name': 'Aggregation Test'})
        
        # 创建一个模拟的成本凭证行
        self.env['account.analytic.line'].create({
            'name': 'Fertilizer Cost',
            'account_id': task.analytic_account_id.id,
            'amount': -500.0, # 支出为负
        })
        
        # 验证任务总成本汇总
        task._compute_total_costs()
        self.assertEqual(task.total_production_costs, 500.0)
