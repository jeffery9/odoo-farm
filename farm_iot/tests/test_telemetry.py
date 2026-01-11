from odoo.tests.common import TransactionCase

class TestTelemetry(TransactionCase):

    def setUp(self):
        super(TestTelemetry, self).setUp()
        self.Telemetry = self.env['farm.telemetry']
        self.Task = self.env['project.task']
        self.task = self.Task.create({'name': 'Pond 01 Management'})

    def test_01_log_telemetry(self):
        """ 测试记录遥测数据 [US-11] """
        telemetry = self.Telemetry.create({
            'name': 'Oxygen Sensor 01',
            'sensor_type': 'dissolved_oxygen',
            'value': 6.5,
            'production_id': self.task.id
        })
        self.assertEqual(telemetry.production_id.id, self.task.id)
        self.assertEqual(telemetry.value, 6.5)
