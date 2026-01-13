from odoo.tests.common import TransactionCase

class TestCostAllocation(TransactionCase):

    def setUp(self):
        super(TestCostAllocation, self).setUp()
        self.CostAlloc = self.env['farm.processing.cost']
        self.Production = self.env['mrp.production']
        self.AnalyticAccount = self.env['account.analytic.account'].create({'name': 'Processing Line 1'})
        
        # 创建一个加工单
        product = self.env['product.product'].create({'name': 'Juice', 'type': 'product'})
        self.mo = self.Production.create({
            'product_id': product.id,
            'product_qty': 100.0,
            'water_meter_start': 10.0,
            'water_meter_end': 20.0, # 10 units consumed
            'electricity_meter_start': 100.0,
            'electricity_meter_end': 150.0, # 50 units consumed
        })
        # 关联分析账户到产品或 BOM
        product.bom_ids = [(0, 0, {
            'product_tmpl_id': product.product_tmpl_id.id,
            'product_qty': 1,
            'analytic_account_id': self.AnalyticAccount.id
        })]

    def test_01_cost_calculation(self):
        """ 测试水电成本自动计算逻辑 [US-14-13] """
        alloc = self.CostAlloc.create({
            'production_id': self.mo.id,
            'water_rate': 2.0,
            'electricity_rate': 0.5,
            'other_indirect_costs': 100.0
        })
        
        # Water: 10 * 2.0 = 20
        # Elec: 50 * 0.5 = 25
        # Total: 20 + 25 + 100 = 145
        self.assertEqual(alloc.total_processing_cost, 145.0)

    def test_02_analytic_transfer(self):
        """ 测试成本分摊到分析账户 """
        alloc = self.CostAlloc.create({
            'production_id': self.mo.id,
            'other_indirect_costs': 500.0
        })
        alloc.action_allocate_costs()
        
        # 检查是否生成了负向的分析行
        line = self.env['account.analytic.line'].search([('account_id', '=', self.AnalyticAccount.id)])
        self.assertTrue(line)
        self.assertEqual(line[0].amount, -500.0)
