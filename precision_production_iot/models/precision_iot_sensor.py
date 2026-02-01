# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import json
from datetime import datetime, timedelta


class PrecisionIotSensor(models.Model):
    _name = 'precision.iot.sensor'
    _description = 'Precision Production IoT Sensor (Integrated with Industrial IoT)'
    _order = 'name'

    name = fields.Char('Sensor Name', required=True)
    sensor_id = fields.Char('Sensor ID', required=True, copy=False, help="Unique identifier for the sensor")
    device_id = fields.Many2one('precision.iot.device', string='IoT Device', required=True, ondelete='cascade')
    sensor_type = fields.Selection([
        ('temperature', 'Temperature'),
        ('humidity', 'Humidity'),
        ('pressure', 'Pressure'),
        ('ph', 'pH'),
        ('conductivity', 'Conductivity'),
        ('flow', 'Flow Rate'),
        ('weight', 'Weight'),
        ('level', 'Level'),
        ('voltage', 'Voltage'),
        ('current', 'Current'),
        ('frequency', 'Frequency'),
    ], string='Sensor Type', required=True)
    parameter_name = fields.Char('Parameter Name', help="The parameter this sensor measures, e.g. 'Temperature'")
    description = fields.Text('Description')
    is_active = fields.Boolean('Active', default=True)
    is_calibrated = fields.Boolean('Calibrated', default=False)
    calibration_date = fields.Date('Last Calibration Date')
    calibration_next = fields.Date('Next Calibration Due')

    # Measurement units and ranges
    unit_of_measure = fields.Char('Unit of Measure', help="e.g. °C, %RH, kPa, pH, mS/cm, L/min, kg")
    min_range = fields.Float('Minimum Range')
    max_range = fields.Float('Maximum Range')
    tolerance_percent = fields.Float('Tolerance (%)', default=2.0)

    # Current reading info
    current_value = fields.Float('Current Value', readonly=True)
    current_uom = fields.Char('Current UOM', readonly=True)
    last_read_datetime = fields.Datetime('Last Read', readonly=True)
    last_reading_id = fields.Many2one('precision.iot.reading', string='Last Reading', readonly=True)

    # Relations
    reading_ids = fields.One2many('precision.iot.reading', 'sensor_id', string='Readings')

    _sql_constraints = [
        ('sensor_id_uniq', 'unique(sensor_id)', 'Sensor ID must be unique!'),
        ('device_sensor_uniq', 'unique(device_id, sensor_id)', 'Sensor ID must be unique per device!'),
    ]

    @api.constrains('min_range', 'max_range')
    def _check_range(self):
        for record in self:
            if record.min_range and record.max_range and record.min_range >= record.max_range:
                raise ValidationError(_("Minimum range must be less than maximum range"))

    def action_refresh_reading(self):
        """Refresh the current reading from the associated device"""
        for sensor in self:
            # The actual reading will be updated when the IIoT device receives telemetry
            latest_reading = self.env['precision.iot.reading'].search([
                ('sensor_id', '=', sensor.id)
            ], order='read_datetime desc', limit=1)

            if latest_reading:
                sensor.current_value = latest_reading.value
                sensor.current_uom = latest_reading.uom
                sensor.last_read_datetime = latest_reading.read_datetime
                sensor.last_reading_id = latest_reading.id

    def action_calibrate(self):
        """Mark sensor as calibrated and set calibration dates"""
        today = fields.Date.context_today(self)
        next_calibration = fields.Date.add(
            fields.Date.from_string(today),
            months=6  # Default: calibrate every 6 months
        )
        return self.write({
            'is_calibrated': True,
            'calibration_date': today,
            'calibration_next': next_calibration,
        })

    def action_validate_reading(self, value):
        """Validate if the reading value is within acceptable range"""
        self.ensure_one()
        if self.min_range is not None and value < self.min_range:
            return False, f"Value {value} below minimum range {self.min_range}"
        if self.max_range is not None and value > self.max_range:
            return False, f"Value {value} above maximum range {self.max_range}"
        return True, "Valid"

    @api.onchange('sensor_type')
    def _onchange_sensor_type(self):
        """Set default UOM based on sensor type"""
        uom_mapping = {
            'temperature': '°C',
            'humidity': '%RH',
            'pressure': 'kPa',
            'ph': 'pH',
            'conductivity': 'mS/cm',
            'flow': 'L/min',
            'weight': 'kg',
            'level': '%',
            'voltage': 'V',
            'current': 'A',
            'frequency': 'Hz',
        }
        if self.sensor_type:
            self.unit_of_measure = uom_mapping.get(self.sensor_type, '')