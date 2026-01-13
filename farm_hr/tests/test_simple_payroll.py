from odoo.tests.common import TransactionCase
from odoo import fields

class TestSimplePayroll(TransactionCase):

    def setUp(self):
        super(TestSimplePayroll, self).setUp()
        self.Employee = self.env['hr.employee'].create({'name': 'Piece Rate Worker'})
        self.Task = self.env['project.task'].create({'name': 'Task A'})
        
        # 1. 定义规则：采摘 = 2.0
        self.env['farm.wage.rule'].create({
            'work_type': 'harvesting',
            'price_per_unit': 2.0
        })
        
        # 2. 录入工时：采摘 100 单位
        self.env['farm.worklog'].create({
            'employee_id': self.Employee.id,
            'task_id': self.Task.id,
            'date': fields.Date.today(),
            'work_type': 'harvesting',
            'quantity': 100.0
        })

    def test_01_calculate_payment(self):
        """ 测试结算单自动计算逻辑 """
        payment = self.env['farm.labor.payment'].create({
            'employee_id': self.Employee.id,
            'date_from': fields.Date.today(),
            'date_to': fields.Date.today(),
        })
        
        payment.action_compute_sheet()
        
        # 100 * 2.0 = 200.0
        self.assertEqual(payment.total_amount, 200.0)
        self.assertEqual(len(payment.line_ids), 1)
