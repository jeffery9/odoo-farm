import unittest
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class TestExportCompliance(TransactionCase):
    """
    测试出口合规功能 [US-17-06]
    """
    def setUp(self):
        super().setUp()
        
        # 创建测试数据
        self.country_standard = self.env['export.country.standard'].create({
            'name': 'Test Country',
            'code': 'TC',
            'compliance_requirements': 'Test compliance requirements'
        })
        
        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'type': 'consu',
            'tracking': 'lot',
        })

    def test_country_standard_creation(self):
        """测试国家标准创建 [US-17-06]"""
        self.assertEqual(self.country_standard.name, 'Test Country')
        self.assertEqual(self.country_standard.code, 'TC')

    def test_export_validation_logic(self):
        """测试出口验证逻辑 [US-17-06]"""
        # 测试合规检查函数
        is_compliant, violations = self.country_standard.check_export_compliance('TC')
        self.assertTrue(is_compliant)
        self.assertEqual(len(violations), 0)