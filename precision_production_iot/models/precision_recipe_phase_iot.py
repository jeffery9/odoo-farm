# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PrecisionRecipePhaseIot(models.Model):
    _name = 'precision.recipe.phase'
    _inherit = 'precision.recipe.phase'

    # IoT Device Integration Fields
    iot_device_ids = fields.Many2many(
        'precision.iot.device',
        string='IoT Devices',
        help='IoT devices associated with this phase'
    )

    # Computed fields for IoT status
    iot_connected = fields.Boolean('IoT Connected', compute='_compute_iot_status', store=True)
    iot_disconnected = fields.Boolean('IoT Disconnected', compute='_compute_iot_status', store=True)
    iot_warning = fields.Boolean('IoT Warning', compute='_compute_iot_status', store=True)
    iot_error = fields.Boolean('IoT Error', compute='_compute_iot_status', store=True)
    iot_device_status = fields.Char('IoT Device Status', compute='_compute_iot_status', store=True)
    iot_readings_count = fields.Integer('IoT Readings Count', compute='_compute_iot_readings_count')

    @api.depends('iot_device_ids', 'iot_device_ids.is_connected', 'iot_device_ids.status')
    def _compute_iot_status(self):
        for phase in self:
            if phase.iot_device_ids:
                connected_devices = phase.iot_device_ids.filtered(lambda d: d.is_connected)
                error_devices = phase.iot_device_ids.filtered(lambda d: d.status == 'error')
                warning_devices = phase.iot_device_ids.filtered(lambda d: d.status == 'warning')

                phase.iot_connected = bool(connected_devices)
                phase.iot_disconnected = not bool(connected_devices) and bool(phase.iot_device_ids)
                phase.iot_warning = bool(warning_devices)
                phase.iot_error = bool(error_devices)

                if error_devices:
                    phase.iot_device_status = 'error'
                elif warning_devices:
                    phase.iot_device_status = 'warning'
                elif connected_devices:
                    phase.iot_device_status = 'online'
                elif phase.iot_device_ids:
                    phase.iot_device_status = 'offline'
                else:
                    phase.iot_device_status = False


            else:
                phase.iot_connected = False
                phase.iot_disconnected = False
                phase.iot_warning = False
                phase.iot_error = False
                phase.iot_device_status = False
                

    def _compute_iot_latest_readings(self):
        """Compute the latest readings from associated IoT devices for this phase"""
        for phase in self:
            latest_readings = []
            if phase.iot_device_ids:
                for device in phase.iot_device_ids:
                    for sensor in device.sensor_ids:
                        latest_reading = self.env['precision.iot.reading'].search([
                            ('sensor_id', '=', sensor.id),
                            ('phase_id', '=', phase.id)
                        ], order='read_datetime desc', limit=1)

                        if latest_reading:
                            latest_readings.append({
                                'sensor_name': sensor.name,
                                'value': f"{latest_reading.value} {latest_reading.uom}",
                                'deviation_percent': latest_reading.deviation_percent,
                                'deviation_critical': latest_reading.is_deviation_critical,
                                'deviation_warning': latest_reading.deviation_percent > 10 and latest_reading.deviation_percent <= 25,
                                'read_datetime': latest_reading.read_datetime
                            })
            phase.iot_latest_readings = latest_readings
    def _compute_iot_readings_count(self):
        for phase in self:
            if phase.iot_device_ids:
                related_readings = self.env['precision.iot.reading'].search([
                    ('device_id', 'in', phase.iot_device_ids.ids),
                    ('phase_id', '=', phase.id)
                ])
                phase.iot_readings_count = len(related_readings)
            else:
                phase.iot_readings_count = 0
