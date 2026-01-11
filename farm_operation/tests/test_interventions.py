from odoo.tests.common import TransactionCase

class TestAgriInterventions(TransactionCase):

    def setUp(self):
        super(TestAgriInterventions, self).setUp()
        self.Intervention = self.env['mrp.production']
        self.Task = self.env['project.task']
        self.Product = self.env['product.product']
        
        # 创建基础数据
        self.task = self.Task.create({'name': 'Wheat Sowing - Plot A'})
        self.product = self.Product.create({
            'name': 'Wheat Seed',
            'type': 'product',
        })
        self.bom = self.env['mrp.bom'].create({
            'product_tmpl_id': self.product.product_tmpl_id.id,
            'product_uom_id': self.product.uom_id.id,
            'product_qty': 1.0,
            'type': 'normal',
        })

    def test_01_link_intervention_to_task(self):
        """ 测试干预记录（MO）关联生产任务 [US-06] """
        intervention = self.Intervention.create({
            'product_id': self.product.id,
            'bom_id': self.bom.id,
            'product_qty': 10.0,
            'agri_task_id': self.task.id
        })
        self.assertEqual(intervention.agri_task_id.id, self.task.id, "干预记录应正确关联任务")
