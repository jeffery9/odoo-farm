from odoo.tests.common import TransactionCase
from odoo import fields

class TestFarmLabor(TransactionCase):

    def setUp(self):
        super(TestFarmLabor, self).setUp()
        self.Employee = self.env['hr.employee']
        self.Task = self.env['project.task']
        self.Worklog = self.env['farm.worklog']
        
        self.worker = self.Employee.create({'name': 'Agri Worker A'})
        self.task = self.Task.create({'name': 'Apple Harvesting Task'})

    def test_01_piece_rate_worklog(self):
        """ 测试计件工时记录 [US-43] """
        worklog = self.Worklog.create({
            'employee_id': self.worker.id,
            'task_id': self.task.id,
            'date': fields.Date.today(),
            'quantity': 50.0,
            'uom_id': self.env.ref('uom.product_uom_kgm').id,
            'work_type': 'harvesting'
        })
        
        self.assertEqual(worklog.employee_id.name, 'Agri Worker A')
        self.assertEqual(worklog.quantity, 50.0)
        
        # 验证任务层面的作业量汇总
        self.task._compute_total_worklog_qty()
        self.assertEqual(self.task.total_harvested_qty, 50.0)
