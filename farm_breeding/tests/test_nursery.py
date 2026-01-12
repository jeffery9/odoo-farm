from odoo.tests.common import TransactionCase
from odoo import fields
from datetime import timedelta

class TestNurseryManagement(TransactionCase):

    def setUp(self):
        super(TestNurseryManagement, self).setUp()
        self.NurseryBatch = self.env['farm.nursery.batch']
        self.Product = self.env['product.product']
        
        self.seed = self.Product.create({
            'name': 'Tomato Seedlings',
            'type': 'product',
            'is_variety': True,
            'variety_type': 'crop'
        })

    def test_01_seedling_age_calculation(self):
        """ 测试苗龄自动计算 [US-03-02] """
        ten_days_ago = fields.Date.today() - timedelta(days=10)
        batch = self.NurseryBatch.create({
            'name': 'TOM-2026-001',
            'product_id': self.seed.id,
            'sowing_date': ten_days_ago
        })
        self.assertEqual(batch.seedling_age, 10, "苗龄应为10天")

    def test_02_convert_to_transplant_task(self):
        """ 测试一键生成移栽任务 [US-03-02] """
        batch = self.NurseryBatch.create({
            'name': 'TOM-2026-002',
            'product_id': self.seed.id,
            'sowing_date': fields.Date.today()
        })
        
        task = batch.action_create_transplant_task()
        self.assertEqual(task.name, 'Transplant Task: TOM-2026-002')
        self.assertIn(batch.name, task.description)
