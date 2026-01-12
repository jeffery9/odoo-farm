from odoo.tests.common import TransactionCase

class TestLivestockFeeding(TransactionCase):

    def setUp(self):
        super(TestLivestockFeeding, self).setUp()
        self.Intervention = self.env['mrp.production']
        self.Product = self.env['product.product']
        self.Task = self.env['project.task']
        
        # 1. 创建饲料产品
        self.corn = self.Product.create({'name': 'Corn Feed', 'type': 'product'})
        self.soybean = self.Product.create({'name': 'Soybean Meal', 'type': 'product'})
        
        # 2. 创建成品描述（逻辑对象：某次饲喂产出）
        self.feeding_output = self.Product.create({'name': 'Daily Ration', 'type': 'service'})
        
        # 3. 创建饲喂配方 (BOM)
        self.bom = self.env['mrp.bom'].create({
            'product_tmpl_id': self.feeding_output.product_tmpl_id.id,
            'product_qty': 1.0,
            'type': 'normal',
            'bom_line_ids': [
                (0, 0, {'product_id': self.corn.id, 'product_qty': 0.7}),
                (0, 0, {'product_id': self.soybean.id, 'product_qty': 0.3}),
            ]
        })
        
        # 4. 创建养殖任务
        self.task = self.Task.create({'name': 'Piggery Group 01'})

    def test_01_feeding_intervention_bom(self):
        """ 测试饲喂干预自动应用配方 [US-01-03] """
        feeding_op = self.Intervention.create({
            'product_id': self.feeding_output.id,
            'bom_id': self.bom.id,
            'product_qty': 100.0,
            'agri_task_id': self.task.id,
            'intervention_type': 'feeding'
        })
        
        # 验证原材料行是否按比例生成 (70kg corn, 30kg soybean)
        corn_move = feeding_op.move_raw_ids.filtered(lambda m: m.product_id == self.corn)
        self.assertEqual(corn_move.product_uom_qty, 70.0)
