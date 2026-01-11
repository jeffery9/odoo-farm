from odoo import models, fields, api

class FarmTelemetry(models.Model):
    _name = 'farm.telemetry'
    _description = 'Agricultural Telemetry Data'
    _order = 'timestamp desc'

    name = fields.Char("Sensor Name", required=True)
    sensor_type = fields.Selection([
        ('temperature', 'Temperature (温度)'),
        ('ph', 'pH Level (酸碱度)'),
        ('dissolved_oxygen', 'Dissolved Oxygen (溶氧量)'),
        ('humidity', 'Humidity (湿度)'),
        ('soil_moisture', 'Soil Moisture (土壤水分)'),
    ], string="Sensor Type", required=True)
    
    value = fields.Float("Value", required=True)
    timestamp = fields.Datetime("Timestamp", default=fields.Datetime.now, required=True)
    
    # 关联生产任务 [US-11]
    production_id = fields.Many2one('project.task', string="Production Task")
    
    # 关联 IIoT 设备
    device_id = fields.Many2one('iiot.device', string="IIoT Device")
    
    # 关联地块（可选）
    land_parcel_id = fields.Many2one('stock.location', string="Land Parcel/Pond")
