from odoo.tests.common import TransactionCase

class TestIotAutomation(TransactionCase):

    def setUp(self):
        super(TestIotAutomation, self).setUp()
        self.Telemetry = self.env['farm.telemetry']
        self.Rule = self.env['farm.automation.rule']
        self.Device = self.env['iiot.device']
        
        # 创建一个模拟执行设备
        profile = self.env['iiot.device.profile'].create({
            'name': 'Pump Profile',
            'telemetry_topic_template': 't/{device}',
            'command_topic_template': 'c/{device}',
            'command_template': '{"a": "{{action}}"}'
        })
        self.pump = self.Device.create({
            'name': 'Water Pump 1',
            'serial_number': 'PUMP-001',
            'device_id': 'pump01',
            'profile_id': profile.id
        })

    def test_01_rule_trigger(self):
        """ 测试低溶氧自动开启增氧机规则 [US-06-02] """
        rule = self.Rule.create({
            'name': 'Oxygen Alert',
            'sensor_type': 'dissolved_oxygen',
            'operator': '<',
            'threshold': 4.0,
            'target_device_id': self.pump.id,
            'command_to_send': 'power_on'
        })
        
        # 模拟产生一条低溶氧遥测数据 (3.5 < 4.0)
        # 注意：实际代码会在 create 时触发 check_and_trigger
        # 我们在这里模拟 telemetry 记录
        telemetry = self.Telemetry.create({
            'name': 'Oxygen Sensor 1',
            'sensor_type': 'dissolved_oxygen',
            'value': 3.5
        })
        
        # 检查是否生成了成功发送的指令日志
        log = self.env['farm.command.log'].search([('device_id', '=', self.pump.id)])
        self.assertTrue(log)
        self.assertEqual(log[0].command, 'power_on')
