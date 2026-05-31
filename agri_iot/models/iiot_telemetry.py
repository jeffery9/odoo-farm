from odoo import models, fields, api

class IiotTelemetry(models.Model):
    _name = 'iiot.telemetry'
    _description = 'IIoT Telemetry Data'
    _order = 'timestamp desc'

    name = fields.Char("Sensor Name", required=True)
    sensor_type = fields.Selection([
        ('temperature', 'Temperature'),
        ('ph', 'pH Level'),
        ('dissolved_oxygen', 'Dissolved Oxygen'),
        ('humidity', 'Humidity'),
        ('soil_moisture', 'Soil Moisture'),
        ('flight_altitude', 'Flight Altitude'),
        ('chemical_level', 'Chemical Level'),
        ('battery_voltage', 'Drone Battery'),
        ('micro_sensor', 'Urban Micro-sensor')
    ], string="Sensor Type", required=True)

    value = fields.Float("Value", required=True)
    timestamp = fields.Datetime("Timestamp", default=fields.Datetime.now, required=True)

    # Base linkage
    device_id = fields.Many2one('iiot.device', string="IIoT Device")

    # GIS Snapshot
    gps_lat = fields.Float("Latitude", digits=(10, 7))
    gps_lng = fields.Float("Longitude", digits=(10, 7))

    @api.model_create_multi
    def create(self, vals_list):
        records = super(IiotTelemetry, self).create(vals_list)
        return records
