# -*- coding: utf-8 -*-
# [US-203-02] 配方边缘：工艺参数到 MQTT Setpoint 的下发（独立于管理中心）
from odoo import models, fields, api, _

class PrecisionRecipeControl(models.Model):
    _name = 'precision.recipe.control'
    _description = 'Recipe-specific IoT Edge'

    name = fields.Char("Bridge Name", required=True)
    # 直接使用 agri_iot 的底层设备
    iiot_device_id = fields.Many2one('iiot.device', string="Communication Device", required=True)
    mqtt_topic = fields.Char("MQTT Setpoint Topic", required=True)
    
    recipe_parameter_id = fields.Many2one('precision.recipe.parameter', string="Recipe Parameter")
    last_sync_value = fields.Float("Last Value", readonly=True)

    def action_sync_setpoint(self, value=False):
        """ 边缘执行：直接调用通讯框架 (agri_iot) 并保存本边缘日志 """
        self.ensure_one()
        target_value = value if value is not False else self.recipe_parameter_id.target_value
        
        # 1. 保存配方边缘专用日志
        log = self.env['precision.iot.command.log'].create({
            'device_id': self.env['precision.iot.device'].search([('iiot_device_id', '=', self.iiot_device_id.id)], limit=1).id,
            'command': f'SET_RECIPE_PARAM_{self.mqtt_topic}',
            'payload': f'{{"value": {target_value}}}',
            'production_id': self.recipe_parameter_id.production_id.id,
            'phase_id': self.recipe_parameter_id.phase_id.id,
        })

        # 2. 直接调用通讯框架 agri_iot 执行下发
        if hasattr(self.iiot_device_id, 'action_mqtt_publish'):
            self.iiot_device_id.action_mqtt_publish(
                topic=self.mqtt_topic,
                payload=log.payload
            )
            log.write({'status': 'success'})
        
        self.write({'last_sync_value': target_value})
        return True