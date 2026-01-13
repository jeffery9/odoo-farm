from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestBreedingLogic(TransactionCase):

    def setUp(self):
        super(TestBreedingLogic, self).setUp()
        self.NurseryBatch = self.env['farm.nursery.batch']
        self.Lot = self.env['stock.lot']
        self.Trait = self.env['farm.trait.value']
        self.Product = self.env['product.product']
        
        # 1. Create seed variety
        self.seed = self.Product.create({
            'name': 'Hybrid Rice Seed',
            'is_variety': True,
            'type': 'product'
        })
        
        # 2. Locations
        self.nursery_loc = self.env['stock.location'].create({
            'name': 'Nursery Room 1',
            'usage': 'internal'
        })
        self.field_loc = self.env['stock.location'].create({
            'name': 'Production Plot A',
            'usage': 'internal',
            'is_land_parcel': True
        })

    def test_01_nursery_transplant_flow(self):
        """ 测试育苗批次移栽自动触发逻辑 [US-10-01] """
        batch = self.NurseryBatch.create({
            'name': 'B-2026-001',
            'product_id': self.seed.id,
            'quantity': 1000,
            'survival_rate': 95.0,
            'location_src_id': self.nursery_loc.id,
            'location_dest_id': self.field_loc.id
        })
        
        # 执行移栽
        batch.action_create_transplant_task()
        
        # 1. 验证状态
        self.assertEqual(batch.state, 'transplanted')
        
        # 2. 验证是否生成了调拨单 (Picking)
        picking = self.env['stock.picking'].search([('origin', '=', batch.name)])
        self.assertTrue(picking)
        self.assertEqual(picking.location_id.id, self.nursery_loc.id)
        self.assertEqual(picking.location_dest_id.id, self.field_loc.id)
        
        # 3. 验证是否生成了任务 (Task)
        task = self.env['project.task'].search([('name', 'like', batch.name)])
        self.assertTrue(task)
        self.assertEqual(task.land_parcel_id.id, self.field_loc.id)

    def test_02_trait_comparison_wizard(self):
        """ 测试性状对比向导的数据加载逻辑 [US-10-02] """
        # 创建两个带有性状的批次
        lot1 = self.Lot.create({'name': 'LOT-A', 'product_id': self.seed.id})
        lot2 = self.Lot.create({'name': 'LOT-B', 'product_id': self.seed.id})
        
        self.Trait.create({'lot_id': lot1.id, 'name': 'Yield', 'value': 'High', 'score': 9.0})
        self.Trait.create({'lot_id': lot2.id, 'name': 'Yield', 'value': 'Medium', 'score': 7.0})
        
        # 启动向导
        wizard = self.env['farm.trait.comparison.wizard'].create({
            'lot_ids': [(6, 0, [lot1.id, lot2.id])]
        })
        wizard._onchange_lot_ids() # 触发数据加载
        
        # 验证向导行数 (2个批次各1个属性 = 2行)
        self.assertEqual(len(wizard.line_ids), 2)
        scores = wizard.line_ids.mapped('score')
        self.assertIn(9.0, scores)
        self.assertIn(7.0, scores)
