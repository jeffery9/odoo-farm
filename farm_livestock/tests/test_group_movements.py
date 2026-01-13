from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestGroupMovements(TransactionCase):

    def setUp(self):
        super(TestGroupMovements, self).setUp()
        self.Lot = self.env['stock.lot']
        self.Product = self.env['product.product']
        
        self.pig_product = self.Product.create({
            'name': 'Fattening Pig',
            'type': 'product',
            'tracking': 'lot'
        })
        
        self.group_a = self.Lot.create({
            'name': 'PIG-GRP-A',
            'product_id': self.pig_product.id,
            'is_animal': True,
        })

    def test_01_record_death(self):
        """ 测试记录动物死亡减员 [US-05-04] """
        # 初始数量假设通过库存已经有了，这里测试逻辑层面的记录
        self.group_a.action_record_death(qty=2, reason='disease', notes='Swine flu suspicion')
        
        # 验证消息记录
        message = self.group_a.message_ids[0]
        self.assertIn('2', message.body)
        self.assertIn('disease', message.body)

    def test_02_merge_groups(self):
        """ 测试群组合并 [US-05-04] """
        group_b = self.Lot.create({
            'name': 'PIG-GRP-B',
            'product_id': self.pig_product.id,
            'is_animal': True,
        })
        
        # 合并 B 到 A
        self.group_a.action_merge_from(group_b)
        
        # 验证 B 已注销
        self.assertEqual(group_b.biological_stage, 'harvested')
        self.assertIn('Merged', self.group_a.message_ids[0].body)
