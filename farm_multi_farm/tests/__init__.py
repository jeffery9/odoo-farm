import unittest
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class TestMultiFarmCollaboration(TransactionCase):
    """
    测试多实体协同与合作社管理功能 [US-19-01 至 US-19-05]
    """
    def setUp(self):
        super().setUp()
        
        # 创建测试数据
        self.cooperative = self.env['farm.entity'].create({
            'name': 'Test Cooperative',
            'entity_type': 'cooperative',
        })
        
        self.farm1 = self.env['farm.entity'].create({
            'name': 'Test Farm 1',
            'entity_type': 'farm',
            'parent_entity_id': self.cooperative.id,
        })
        
        self.farm2 = self.env['farm.entity'].create({
            'name': 'Test Farm 2',
            'entity_type': 'farm',
            'parent_entity_id': self.cooperative.id,
        })
        
        self.company = self.env.ref('base.main_company')
        
        self.vehicle = self.env['farm.vehicle'].create({
            'name': 'Test Tractor',
            'vehicle_type': 'tractor',
            'company_id': self.company.id,
            'can_be_shared': True,
        })

    def test_entity_creation(self):
        """测试实体创建 [US-19-01]"""
        self.assertEqual(self.cooperative.name, 'Test Cooperative')
        self.assertEqual(self.cooperative.entity_type, 'cooperative')
        self.assertIn(self.farm1, self.cooperative.child_entity_ids)
        self.assertIn(self.farm2, self.cooperative.child_entity_ids)

    def test_entity_link_creation(self):
        """测试实体链接创建 [US-19-01]"""
        entity_link = self.env['farm.entity.link'].create({
            'source_entity_id': self.cooperative.id,
            'target_entity_id': self.farm1.id,
            'link_type': 'membership',
        })
        
        self.assertEqual(entity_link.link_type, 'membership')
        self.assertEqual(entity_link.source_entity_id, self.cooperative)
        self.assertEqual(entity_link.target_entity_id, self.farm1)

    def test_data_sharing_rule_creation(self):
        """测试数据共享规则创建 [US-19-02]"""
        sharing_rule = self.env['farm.data.sharing.rule'].create({
            'name': 'Test Sharing Rule',
            'source_entity_id': self.farm1.id,
            'target_entity_id': self.cooperative.id,
            'data_type': 'production',
            'access_level': 'read',
        })
        
        self.assertEqual(sharing_rule.name, 'Test Sharing Rule')
        self.assertEqual(sharing_rule.data_type, 'production')
        self.assertEqual(sharing_rule.access_level, 'read')

    def test_shared_vehicle_creation(self):
        """测试共享车辆创建 [US-19-03]"""
        self.vehicle.shared_entity_ids = [self.farm1.id, self.farm2.id]
        
        self.assertTrue(self.vehicle.can_be_shared)
        self.assertIn(self.farm1, self.vehicle.shared_entity_ids)
        self.assertIn(self.farm2, self.vehicle.shared_entity_ids)

    def test_internal_settlement_creation(self):
        """测试内部结算创建 [US-19-03, US-19-04]"""
        settlement = self.env['farm.internal.settlement'].create({
            'from_entity_id': self.farm1.id,
            'to_entity_id': self.farm2.id,
            'from_company_id': self.company.id,
            'to_company_id': self.company.id,
            'settlement_type': 'vehicle_rental',
            'amount': 500.0,
        })
        
        self.assertEqual(settlement.settlement_type, 'vehicle_rental')
        self.assertEqual(settlement.amount, 500.0)
        self.assertEqual(settlement.state, 'draft')

    def test_standard_procedure_creation(self):
        """测试标准规程创建 [US-19-05]"""
        procedure = self.env['farm.standard.procedure'].create({
            'name': 'Test Planting Standard',
            'code': 'TPS-001',
            'category': 'planting',
            'description': 'Standard procedure for planting operations',
            'is_mandatory': True,
        })
        
        self.assertEqual(procedure.name, 'Test Planting Standard')
        self.assertEqual(procedure.code, 'TPS-001')
        self.assertEqual(procedure.category, 'planting')
        self.assertTrue(procedure.is_mandatory)

    def test_compliance_check_creation(self):
        """测试合规检查创建 [US-19-05]"""
        procedure = self.env['farm.standard.procedure'].create({
            'name': 'Test Compliance Standard',
            'code': 'TCS-001',
            'category': 'fertilization',
        })
        
        compliance_check = self.env['farm.compliance.check'].create({
            'name': 'Test Compliance Check',
            'entity_id': self.farm1.id,
            'procedure_id': procedure.id,
            'compliance_status': 'pending',
        })
        
        self.assertEqual(compliance_check.name, 'Test Compliance Check')
        self.assertEqual(compliance_check.compliance_status, 'pending')
        self.assertEqual(compliance_check.entity_id, self.farm1)
        self.assertEqual(compliance_check.procedure_id, procedure)