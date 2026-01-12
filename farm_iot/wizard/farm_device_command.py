from odoo import models, fields, api, _
from odoo.exceptions import UserError

class FarmDeviceCommand(models.TransientModel):
    _name = 'farm.device.command'
    _description = 'Send Command to Farm Device'

    device_id = fields.Many2one('iiot.device', string="Target Device", required=True)
    command_type = fields.Selection([
        ('switch', 'Switch On/Off (开关控制)'),
        ('set_threshold', 'Set Threshold (设置阈值)'),
        ('reboot', 'Reboot Device (重启设备)'),
        ('custom', 'Custom JSON (自定义指令)')
    ], string="Command Type", default='switch', required=True)
    
    action = fields.Selection([
        ('on', 'Turn ON (开启)'),
        ('off', 'Turn OFF (关闭)')
    ], string="Action")
    
    custom_params = fields.Text("Custom Parameters (JSON)")

    def action_send(self):
        self.ensure_one()
        params = {}
        if self.command_type == 'switch':
            params = {'state': self.action}
            action_name = 'power_control'
        elif self.command_type == 'reboot':
            action_name = 'reboot'
        else:
            action_name = 'custom'
            # 简单处理自定义参数
            import json
            params = json.loads(self.custom_params or '{}')

        # 调用底层 industrial_iot 的发送能力
        try:
            import time
            start_ts = time.time()
            self.device_id.send_command(action_name, **params)
            latency = int((time.time() - start_ts) * 1000)
            
            # 记录审计日志 [US-06-03]
            self.env['farm.command.log'].create({
                'device_id': self.device_id.id,
                'command': action_name,
                'params': str(params),
                'status': 'success',
                'execution_time_ms': latency
            })
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Command Sent'),
                    'message': _('Command %s has been published to %s') % (action_name, self.device_id.name),
                    'type': 'success',
                    'sticky': False,
                }
            }
        except Exception as e:
            raise UserError(_("Failed to send command: %s") % str(e))
