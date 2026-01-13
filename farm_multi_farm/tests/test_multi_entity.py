from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestMultiEntity(TransactionCase):

    def setUp(self):
        super(TestMultiEntity, self).setUp()
        self.Coop = self.env['cooperative.entity']
        self.Farm = self.env['farm.entity']
        self.Company = self.env['res.company']

    def test_01_entity_recursion_check(self):
        """ 测试防止实体关系循环引用 [US-19-01] """
        company_a = self.Company.create({'name': 'Company A'})
        company_b = self.Company.create({'name': 'Company B'})
        
        farm_a = self.Farm.create({
            'name': 'Farm A',
            'company_id': company_a.id,
            'entity_type': 'farm'
        })
        farm_b = self.Farm.create({
            'name': 'Farm B',
            'company_id': company_b.id,
            'entity_type': 'subsidiary',
            'parent_entity_id': farm_a.id
        })
        
        # 尝试让 A 成为 B 的子实体，触发循环
        with self.assertRaises(ValidationError):
            farm_a.parent_entity_id = farm_b.id

    def test_02_data_sharing_logic(self):
        """ 测试基于租户隔离级别的数据访问 [US-19-02] """
        # 创建一个部分共享的实体
        farm = self.Farm.create({
            'name': 'Partial Share Farm',
            'company_id': self.env.company.id,
            'data_isolation_level': 'partial'
        })
        
        # 验证基础的可访问公司获取逻辑
        accessible = farm._get_accessible_companies()
        self.assertIn(self.env.company.id, accessible.ids)
