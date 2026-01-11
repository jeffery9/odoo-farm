from odoo.tests.common import TransactionCase
from odoo import fields
from datetime import timedelta

class TestPreventionScheduling(TransactionCase):

    def setUp(self):
        super(TestPreventionScheduling, self).setUp()
        self.Template = self.env['farm.prevention.template']
        self.Task = self.env['project.task']
        self.Variety = self.env['product.product'].create({
            'name': 'Fattening Pig',
            'is_variety': True,
            'variety_type': 'livestock'
        })
        
        # 1. 创建防疫模板
        self.template = self.Template.create({
            'name': 'Standard Pig Prevention Plan',
            'line_ids': [
                (0, 0, {'name': 'Swine Fever Vaccine', 'delay_days': 7}),
                (0, 0, {'name': 'Foot and Mouth Disease Vaccine', 'delay_days': 30}),
            ]
        })

    def test_01_apply_template_to_task(self):
        """ 测试应用模板自动生成子任务 [US-33] """
        # 创建一个生产任务，开始日期为今天
        base_task = self.Task.create({
            'name': 'Pig Batch 2026-001',
            'planned_date_begin': fields.Date.today(),
            'prevention_template_id': self.template.id
        })
        
        # 触发模板应用逻辑
        base_task.action_apply_prevention_template()
        
        # 验证子任务数量
        self.assertEqual(len(base_task.child_ids), 2, "应生成2个子任务")
        
        # 验证第一个子任务日期 (T+7)
        task_7 = base_task.child_ids.filtered(lambda t: 'Swine Fever' in t.name)
        expected_date = fields.Date.today() + timedelta(days=7)
        self.assertEqual(task_7.date_deadline, expected_date)
