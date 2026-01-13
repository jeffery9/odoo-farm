from odoo import models, fields, api

class FarmLocation(models.Model):
    _inherit = 'stock.location'

    camera_device_id = fields.Many2one(
        'iiot.device', 
        string="Field Camera", 
        domain=[('is_camera', '=', True)],
        help="The camera assigned to monitor this specific plot or pond."
    )

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
        ('flight_altitude', 'Flight Altitude (高度)'),
        ('chemical_level', 'Chemical Level (药箱水位)'),
        ('battery_voltage', 'Drone Battery (电压)')
    ], string="Sensor Type", required=True)
    
    value = fields.Float("Value", required=True)
    timestamp = fields.Datetime("Timestamp", default=fields.Datetime.now, required=True)
    
    # 关联资产与任务
    production_id = fields.Many2one('project.task', string="Production Task")
    drone_id = fields.Many2one('maintenance.equipment', string="Drone", domain="[('is_drone', '=', True)]")
    device_id = fields.Many2one('iiot.device', string="IIoT Device")
    
    # 关联地块（可选）
    land_parcel_id = fields.Many2one('stock.location', string="Land Parcel/Pond")
    
    # GIS Snapshot [US-02-02]
    gps_lat = fields.Float("Latitude", digits=(10, 7))
    gps_lng = fields.Float("Longitude", digits=(10, 7))

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            # 查找并运行相关的自动化规则
            rules = self.env['farm.automation.rule'].search([
                ('active', '=', True),
                ('sensor_type', '=', record.sensor_type)
            ])
            for rule in rules:
                rule.check_and_trigger(record)
        return records
