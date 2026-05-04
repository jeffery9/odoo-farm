# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import json
from datetime import datetime


class PrecisionIotDevice(models.Model):
    _name = 'precision.iot.device'
    _description = 'Precision Production IoT Device (Integrated with Industrial IoT)'
    _order = 'name'

    # Link to Industrial IoT device
    iiot_device_id = fields.Many2one('iiot.device', string='Industrial IoT Device',
                                     help="Link to the base Industrial IoT device")

    # Basic information
    name = fields.Char('Device Name', compute='_compute_name', store=True, precompute=True)
    device_type = fields.Selection([
        ('temperature', 'Temperature Sensor'),
        ('humidity', 'Humidity Sensor'),
        ('pressure', 'Pressure Sensor'),
        ('ph', 'pH Sensor'),
        ('conductivity', 'Conductivity Sensor'),
        ('flow', 'Flow Sensor'),
        ('weight', 'Weight Scale'),
        ('multifunction', 'Multi-Function Device'),
    ], string='Device Type', required=True)
    description = fields.Text('Description')
    is_active = fields.Boolean('Active', default=True)

    # Link to production
    # TODO: [DE-INDUSTRIAL] Rename 'Production Line/Work Center' to 'IoT Facility Location' for Agri/Semiconductor use cases
    production_line_id = fields.Many2one('mrp.workcenter', string='Production Line/Work Center')

    # Status fields from Industrial IoT integration
    last_seen = fields.Datetime('Last Communication', related='iiot_device_id.last_telemetry', readonly=True)
    is_connected = fields.Boolean('Connected', compute='_compute_is_connected')
    
    @api.depends('iiot_device_id.connection_status')
    def _compute_is_connected(self):
        for rec in self:
            rec.is_connected = (rec.iiot_device_id.connection_status == 'online')
    status = fields.Selection(related='iiot_device_id.connection_status', readonly=True)
    firmware_version = fields.Char('Firmware Version', related='iiot_device_id.firmware_version', readonly=True)

    # Relations
    sensor_ids = fields.One2many('precision.iot.sensor', 'device_id', string='Sensors')
    reading_ids = fields.One2many('precision.iot.reading', 'device_id', string='Readings')

    @api.depends('iiot_device_id', 'iiot_device_id.name')
    def _compute_name(self):
        for record in self:
            if record.iiot_device_id:
                record.name = record.iiot_device_id.name
            else:
                record.name = "Unlinked Device"

    def action_refresh_readings(self):
        """Manually refresh readings from the Industrial IoT device"""
        for device in self:
            if device.iiot_device_id:
                # Trigger refresh of the linked IIoT device
                # The actual reading will be handled by telemetry processing
                pass

    def process_iiot_telemetry(self, telemetry_data):
        """
        Process telemetry data from the linked Industrial IoT device
        This method is called when the IIoT device receives new telemetry
        """
        for device in self:
            if device.iiot_device_id:
                # Process each sensor's data from the telemetry
                for sensor in device.sensor_ids:
                    # Extract value for this sensor from telemetry data
                    # This would depend on the specific format of the telemetry data
                    # For now, we'll assume the telemetry data has sensor-specific keys
                    if sensor.sensor_id in telemetry_data:
                        value = telemetry_data[sensor.sensor_id]

                        # Create a reading record
                        self.env['precision.iot.reading'].create({
                            'device_id': device.id,
                            'sensor_id': sensor.id,
                            'value': value,
                            'read_datetime': fields.Datetime.now(),
                            'raw_data': json.dumps(telemetry_data),
                            'production_id': device.production_line_id.id,  # Or linked production order
                        })

    def send_command_to_device(self, action, **params):
        """
        Send command to the linked Industrial IoT device
        This allows remote control of the IoT device
        """
        for device in self:
            if device.iiot_device_id:
                # Use the Industrial IoT device's command sending method
                return device.iiot_device_id.send_command(action, **params)
        return False

    def send_control_command(self, command_type, value=None, target_phase_id=None):
        """
        Send specific control commands to the device based on production needs
        """
        for device in self:
            if device.iiot_device_id:
                if command_type == 'set_point':
                    # Send a new setpoint to the device
                    params = {
                        'target_value': value,
                        'phase_id': target_phase_id.id if target_phase_id else None
                    }
                    return device.iiot_device_id.send_command('set_control_point', **params)
                elif command_type == 'start_phase':
                    # Start a specific phase on the device
                    params = {'phase_id': target_phase_id.id if target_phase_id else None}
                    return device.iiot_device_id.send_command('start_phase', **params)
                elif command_type == 'stop_phase':
                    # Stop a specific phase on the device
                    return device.iiot_device_id.send_command('stop_phase')
                elif command_type == 'calibrate':
                    # Calibrate the device
                    params = {'sensor_value': value}
                    return device.iiot_device_id.send_command('calibrate', **params)
                elif command_type == 'emergency_stop':
                    # Emergency stop command
                    return device.iiot_device_id.send_command('emergency_stop')
                else:
                    # Generic command with parameters
                    params = {'value': value, 'target_phase_id': target_phase_id.id if target_phase_id else None}
                    return device.iiot_device_id.send_command(command_type, **params)
        return False