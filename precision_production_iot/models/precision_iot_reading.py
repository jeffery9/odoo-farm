# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
import json


class PrecisionIotReading(models.Model):
    _name = 'precision.iot.reading'
    _description = 'Precision Production IoT Reading (Integrated with Industrial IoT)'
    _order = 'read_datetime desc'

    name = fields.Char('Reading Reference', compute='_compute_name', store=True)
    device_id = fields.Many2one('precision.iot.device', string='IoT Device', required=True, ondelete='cascade')
    sensor_id = fields.Many2one('precision.iot.sensor', string='Sensor', required=True, ondelete='cascade')
    parameter_name = fields.Char(related='sensor_id.parameter_name', string='Parameter', readonly=True)
    value = fields.Float('Value', required=True)
    uom = fields.Char('Unit of Measure', compute='_compute_uom', store=True)
    read_datetime = fields.Datetime('Reading Time', default=fields.Datetime.now, required=True)
    is_valid = fields.Boolean('Valid', default=True)
    validation_message = fields.Char('Validation Message')

    # Precision production related fields
    production_id = fields.Many2one('mrp.production', string='Production Order',
                                   help="Production order this reading is associated with")
    phase_id = fields.Many2one('precision.recipe.phase', string='Phase',
                              help="Phase of the recipe this reading is associated with")
    workorder_id = fields.Many2one('mrp.workorder', string='Work Order')

    # Quality metrics
    deviation_percent = fields.Float('Deviation (%)', compute='_compute_deviation', store=True)
    is_deviation_critical = fields.Boolean('Critical Deviation', compute='_compute_deviation', store=True)

    # Raw data for debugging
    raw_data = fields.Text('Raw Data', help="Raw data received from the sensor")

    @api.depends('sensor_id', 'read_datetime', 'value')
    def _compute_name(self):
        for record in self:
            if record.sensor_id and record.read_datetime:
                record.name = f"{record.sensor_id.name} - {record.read_datetime} - {record.value}"
            else:
                record.name = "New Reading"

    @api.depends('sensor_id')
    def _compute_uom(self):
        for record in self:
            record.uom = record.sensor_id.unit_of_measure if record.sensor_id else ''

    @api.depends('value', 'sensor_id')
    def _compute_deviation(self):
        for record in self:
            if record.sensor_id and record.sensor_id.parameter_name:
                # Find related target value if available (for precision.recipe.parameter)
                target_param = self.env['precision.recipe.parameter'].search([
                    ('production_id', '=', record.production_id.id),
                    ('phase_id', '=', record.phase_id.id),
                    ('name', '=ilike', record.sensor_id.parameter_name)
                ], limit=1)

                if target_param and target_param.target_value:
                    deviation = abs(record.value - target_param.target_value)
                    if target_param.target_value != 0:
                        deviation_percent = (deviation / abs(target_param.target_value)) * 100
                    else:
                        deviation_percent = float('inf') if deviation != 0 else 0

                    record.deviation_percent = deviation_percent
                    record.is_deviation_critical = deviation_percent > 25.0  # Critical if >25% deviation
                else:
                    record.deviation_percent = 0.0
                    record.is_deviation_critical = False
            else:
                record.deviation_percent = 0.0
                record.is_deviation_critical = False

    @api.constrains('value', 'sensor_id')
    def _check_value_range(self):
        for record in self:
            if record.sensor_id:
                is_valid, message = record.sensor_id.action_validate_reading(record.value)
                if not is_valid:
                    raise ValidationError(_("Value validation failed: %s") % message)

    def write(self, vals):
        # Update related sensor's current value if this is the latest reading
        result = super().write(vals)

        # Update the current value of the sensor if this reading is the latest
        if 'value' in vals or 'read_datetime' in vals:
            for reading in self:
                # Check if this is the latest reading for the sensor
                latest = self.env['precision.iot.reading'].search([
                    ('sensor_id', '=', reading.sensor_id.id)
                ], order='read_datetime desc', limit=1)

                if latest.id == reading.id:
                    reading.sensor_id.current_value = reading.value
                    reading.sensor_id.current_uom = reading.uom
                    reading.sensor_id.last_read_datetime = reading.read_datetime
                    reading.sensor_id.last_reading_id = reading.id

        return result

    @api.model
    def create(self, vals):
        # Set unit of measure from sensor if not provided
        if 'sensor_id' in vals and 'uom' not in vals:
            sensor = self.env['precision.iot.sensor'].browse(vals['sensor_id'])
            if sensor:
                vals['uom'] = sensor.unit_of_measure

        record = super().create(vals)

        # Update the current value of the sensor since this is now the latest reading
        record.sensor_id.current_value = record.value
        record.sensor_id.current_uom = record.uom
        record.sensor_id.last_read_datetime = record.read_datetime
        record.sensor_id.last_reading_id = record.id

        # Trigger automatic validation and potential intervention
        self._trigger_precision_intervention(record)

        return record

    @api.model
    def _trigger_precision_intervention(self, reading):
        """
        Trigger precision intervention based on IoT reading if deviation is significant
        """
        if reading.is_deviation_critical and reading.production_id:
            # Create an intervention record if deviation is critical
            self.env['precision.intervention'].create({
                'name': f"Critical Deviation: {reading.parameter_name} = {reading.value} {reading.uom}",
                'production_id': reading.production_id.id,
                'phase_id': reading.phase_id.id,
                'intervention_type': 'auto',
                'is_auto_generated': True,
                'description': f"IoT sensor reading {reading.name} shows critical deviation of {reading.deviation_percent:.2f}% from target value",
                'status': 'open'
            })

            # Update production status based on critical reading
            if reading.is_deviation_critical:
                reading.production_id.write({
                    'process_status': 'out_of_control',
                    'is_process_locked': True,
                    'lock_reason': f'Critical deviation detected from IoT sensor: {reading.parameter_name}'
                })

    @api.model
    def create_batch_readings(self, readings_data):
        """
        Create multiple readings at once for efficiency

        readings_data format: [
            {
                'device_id': id,
                'sensor_id': id,
                'value': float,
                'read_datetime': datetime,
                'production_id': id (optional),
                'phase_id': id (optional),
                'workorder_id': id (optional)
            },
            ...
        ]
        """
        created_readings = []
        for reading_data in readings_data:
            reading = self.create(reading_data)
            created_readings.append(reading)

        return created_readings

    def action_validate_reading(self):
        """Manual validation of the reading"""
        for record in self:
            if record.sensor_id:
                is_valid, message = record.sensor_id.action_validate_reading(record.value)
                record.is_valid = is_valid
                record.validation_message = message

    @api.model
    def create_from_iiot_telemetry(self, iiot_device_id, telemetry_data, production_id=None, phase_id=None):
        """
        Create IoT readings from Industrial IoT telemetry data
        This method is called when IIoT devices send telemetry data

        Args:
            iiot_device_id: The Industrial IoT device ID
            telemetry_data: Dictionary containing telemetry values
            production_id: Optional production order to associate with readings
            phase_id: Optional phase to associate with readings
        """
        # Find the corresponding precision IoT device
        precision_device = self.env['precision.iot.device'].search([('iiot_device_id', '=', iiot_device_id)], limit=1)

        if not precision_device:
            # If no precision IoT device is linked to this IIoT device, create a generic reading
            # or skip processing
            return []

        created_readings = []

        # Process each sensor value in the telemetry data
        for sensor_key, sensor_value in telemetry_data.items():
            # Find the sensor that matches this telemetry key
            sensor = self.env['precision.iot.sensor'].search([
                ('device_id', '=', precision_device.id),
                ('sensor_id', '=', sensor_key)
            ], limit=1)

            if sensor:
                # Create a reading for this sensor
                reading = self.create({
                    'device_id': precision_device.id,
                    'sensor_id': sensor.id,
                    'value': sensor_value,
                    'read_datetime': fields.Datetime.now(),
                    'production_id': production_id,
                    'phase_id': phase_id,
                    'raw_data': json.dumps(telemetry_data)
                })
                created_readings.append(reading)

        return created_readings