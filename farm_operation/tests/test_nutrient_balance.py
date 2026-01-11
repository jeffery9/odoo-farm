from odoo.tests.common import TransactionCase

class TestNutrientBalance(TransactionCase):

    def setUp(self):
        super(TestNutrientBalance, self).setUp()
        self.Task = self.env['project.task']
        self.Intervention = self.env['mrp.production']
        self.Product = self.env['product.product']
        
        # 1. 创建地块 (100单位面积)
        self.location = self.env['stock.location'].create({
            'name': 'Test Plot',
            'is_land_parcel': True,
            'land_area': 100.0
        })
        
        # 2. 创建生产任务
        self.task = self.Task.create({
            'name': 'Wheat 2026 - Plot A',
            'land_parcel_id': self.location.id
        })
        
        # 3. 创建化肥产品 (N: 20%, P: 10%, K: 10%)
        self.fertilizer = self.Product.create({
            'name': 'Complex Fertilizer',
            'type': 'product',
            'n_content': 20.0,
            'p_content': 10.0,
            'k_content': 10.0
        })

    def test_01_nutrient_accumulation(self):
        """ 测试施肥后养分自动累加 [US-07] """
        # 创建一个施肥干预任务，投入 50kg 化肥
        intervention = self.Intervention.create({
            'product_id': self.Product.create({'name': 'Dummy'}).id,
            'product_qty': 1.0,
            'agri_task_id': self.task.id,
            'intervention_type': 'fertilizing',
            'move_raw_ids': [(0, 0, {
                'product_id': self.fertilizer.id,
                'product_uom_qty': 50.0,
                'product_uom': self.fertilizer.uom_id.id,
                'location_id': self.env.ref('stock.stock_location_stock').id,
                'location_dest_id': self.fertilizer.property_stock_inventory.id,
            })]
        })
        
        # 模拟 MO 完成逻辑（此处需调用触发计算的方法）
        self.task._update_nutrient_balance()
        
        # 预期结果: 
        # N = 50kg * 20% = 10kg
        # P = 50kg * 10% = 5kg
        # K = 50kg * 10% = 5kg
        self.assertEqual(self.task.total_n, 10.0)
        self.assertEqual(self.task.total_p, 5.0)
        self.assertEqual(self.task.total_k, 5.0)
