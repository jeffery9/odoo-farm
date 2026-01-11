from odoo import models, fields, api, _

class FarmAutomationRule(models.Model):
    _name = 'farm.automation.rule'
    _description = 'Farm IOT Automation Rule'

    name = fields.Char("Rule Name", required=True)
    active = fields.Boolean(default=True)
    
    sensor_type = fields.Selection([
        ('temperature', 'Temperature (温度)'),
        ('ph', 'pH Level (酸碱度)'),
        ('dissolved_oxygen', 'Dissolved Oxygen (溶氧量)'),
    ], string="Trigger Sensor", required=True)
    
    operator = fields.Selection([
        ('<', 'Less Than'),
        ('>', 'Greater Than')
    ], string="Operator", default='<', required=True)
    
    threshold = fields.Float("Threshold", required=True)
    
    target_device_id = fields.Many2one('iiot.device', string="Action Device", required=True)
    command_to_send = fields.Char("Command/Action", default='power_on', required=True)
    command_params = fields.Char("Params (JSON)", default='{"state": "on"}')

    def check_and_trigger(self, telemetry):
        """ 检查并触发规则 """
        self.ensure_one()
        if telemetry.sensor_type != self.sensor_type:
            return False
            
        triggered = False
        if self.operator == '<' and telemetry.value < self.threshold:
            triggered = True
        elif self.operator == '>' and telemetry.value > self.threshold:
            triggered = True
            
        if triggered:
            import json
            params = json.loads(self.command_params or '{}')
            self.target_device_id.send_command(self.command_to_send, **params)
            
            # 在任务/地块消息流中记录自动触发
            if telemetry.production_id:
                telemetry.production_id.message_post(
                    body=_("AUTOMATION: Rule '%s' triggered. Command '%s' sent to %s because %s was %s %s.") % (
                        self.name, self.command_to_send, self.target_device_id.name, 
                        self.sensor_type, self.operator, self.threshold
                    )
                )
