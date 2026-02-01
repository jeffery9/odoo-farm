# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import json


class PrecisionIotReadingWizard(models.TransientModel):
    _name = 'precision.iot.reading.wizard'
    _description = 'Precision IoT Reading Input Wizard'

    # Main fields
    device_id = fields.Many2one('precision.iot.device', string='IoT Device', required=True)
    sensor_id = fields.Many2one('precision.iot.sensor', string='Sensor',
                               domain="[('device_id', '=', device_id), ('is_active', '=', True)]")
    value = fields.Float('Reading Value', required=True)
    uom = fields.Char('Unit of Measure', readonly=True)
    read_datetime = fields.Datetime('Reading Time', default=fields.Datetime.now)

    # Precision production context
    production_id = fields.Many2one('mrp.production', string='Production Order')
    phase_id = fields.Many2one('precision.recipe.phase', string='Phase',
                              domain="[('production_id', '=', production_id)]")
    workorder_id = fields.Many2one('mrp.workorder', string='Work Order')

    # Validation fields
    is_valid = fields.Boolean('Valid', readonly=True)
    validation_message = fields.Char('Validation Message', readonly=True)
    deviation_percent = fields.Float('Deviation (%)', readonly=True)

    # Multi-reading support
    reading_ids = fields.Many2many('precision.iot.reading', string='Related Readings')

    @api.onchange('sensor_id')
    def _onchange_sensor_id(self):
        if self.sensor_id:
            self.uom = self.sensor_id.unit_of_measure

    @api.onchange('sensor_id', 'value', 'production_id', 'phase_id')
    def _onchange_for_validation(self):
        """Update validation fields when key values change"""
        if self.sensor_id and self.value is not None:
            # Validate the reading value
            is_valid, message = self.sensor_id.action_validate_reading(self.value)
            self.is_valid = is_valid
            self.validation_message = message

            # Calculate deviation if related to production
            if self.production_id and self.phase_id and self.sensor_id.parameter_name:
                # Find related target value
                target_param = self.env['precision.recipe.parameter'].search([
                    ('production_id', '=', self.production_id.id),
                    ('phase_id', '=', self.phase_id.id),
                    ('name', '=ilike', self.sensor_id.parameter_name)
                ], limit=1)

                if target_param and target_param.target_value:
                    deviation = abs(self.value - target_param.target_value)
                    if target_param.target_value != 0:
                        self.deviation_percent = (deviation / abs(target_param.target_value)) * 100
                    else:
                        self.deviation_percent = float('inf') if deviation != 0 else 0

    def action_apply_reading(self):
        """Apply the single reading and create an IoT reading record"""
        self.ensure_one()

        # Validate required fields
        if not self.sensor_id:
            raise ValidationError(_("Please select a sensor."))

        # Create the IoT reading
        reading = self.env['precision.iot.reading'].create({
            'device_id': self.device_id.id,
            'sensor_id': self.sensor_id.id,
            'value': self.value,
            'read_datetime': self.read_datetime,
            'production_id': self.production_id.id if self.production_id else False,
            'phase_id': self.phase_id.id if self.phase_id else False,
            'workorder_id': self.workorder_id.id if self.workorder_id else False,
        })

        # Update current sensor values
        self.sensor_id.current_value = self.value
        self.sensor_id.last_read_datetime = self.read_datetime

        # Check if this reading should trigger any interventions
        if reading.is_deviation_critical and reading.production_id:
            # Show a message about potential intervention
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Critical Deviation Detected'),
                    'message': _('A critical deviation was detected from the IoT sensor. The production may be locked for safety.'),
                    'type': 'warning',
                    'sticky': True
                }
            }

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('IoT reading has been recorded successfully.'),
                'type': 'success'
            }
        }

    def action_apply_multiple_readings(self):
        """Apply multiple readings at once (simulated from IoT device)"""
        # This would typically be used when processing multiple readings from an IoT device
        # For now, we'll show a form to input multiple readings
        action = {
            'name': _('IoT Multiple Readings'),
            'type': 'ir.actions.act_window',
            'res_model': 'precision.iot.multiple.readings.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_device_id': self.device_id.id,
                'default_production_id': self.production_id.id,
                'default_phase_id': self.phase_id.id,
            }
        }
        return action

    def action_refresh_device_readings(self):
        """Refresh readings from the selected device"""
        self.ensure_one()
        if self.device_id:
            # Call the refresh method for the device
            self.device_id.action_refresh_readings()

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Device Refresh'),
                    'message': _('Device readings have been refreshed.'),
                    'type': 'success'
                }
            }

    def action_send_control_command(self):
        """Send a control command to the device"""
        self.ensure_one()
        if self.device_id:
            # This would typically open a new wizard for control commands
            # For now, we'll implement a simple command
            action = {
                'name': _('Send Control Command to Device'),
                'type': 'ir.actions.act_window',
                'res_model': 'precision.iot.control.command.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_device_id': self.device_id.id,
                    'default_production_id': self.production_id.id,
                    'default_phase_id': self.phase_id.id,
                }
            }
            return action


class PrecisionIotControlCommandWizard(models.TransientModel):
    _name = 'precision.iot.control.command.wizard'
    _description = 'Precision IoT Control Command Wizard'

    device_id = fields.Many2one('precision.iot.device', string='IoT Device', required=True)
    production_id = fields.Many2one('mrp.production', string='Production Order')
    phase_id = fields.Many2one('precision.recipe.phase', string='Phase',
                              domain="[('production_id', '=', production_id)]")
    command_type = fields.Selection([
        ('set_point', 'Set Control Point'),
        ('start_phase', 'Start Phase'),
        ('stop_phase', 'Stop Phase'),
        ('calibrate', 'Calibrate Device'),
        ('emergency_stop', 'Emergency Stop'),
        ('custom', 'Custom Command'),
    ], string='Command Type', required=True)
    custom_command = fields.Char('Custom Command')
    command_value = fields.Float('Command Value')
    command_description = fields.Char('Command Description')

    @api.onchange('command_type')
    def _onchange_command_type(self):
        """Update UI based on command type"""
        if self.command_type == 'set_point':
            self.command_description = 'Set a new control point value for the device'
        elif self.command_type == 'start_phase':
            self.command_description = 'Start a specific phase on the device'
        elif self.command_type == 'stop_phase':
            self.command_description = 'Stop the current phase on the device'
        elif self.command_type == 'calibrate':
            self.command_description = 'Calibrate the device sensors'
        elif self.command_type == 'emergency_stop':
            self.command_description = 'Send emergency stop command to device'
        else:
            self.command_description = 'Send a custom command to the device'

    def action_send_command(self):
        """Send the selected command to the device"""
        self.ensure_one()

        if not self.device_id or not self.device_id.iiot_device_id:
            raise ValidationError(_("Selected device is not linked to an Industrial IoT device."))

        success = self.device_id.send_control_command(
            self.command_type,
            value=self.command_value,
            target_phase_id=self.phase_id
        )

        if success:
            # Log the command for audit trail
            self.env['precision.iot.command.log'].create({
                'device_id': self.device_id.id,
                'command_type': self.command_type,
                'command_value': self.command_value,
                'production_id': self.production_id.id if self.production_id else None,
                'phase_id': self.phase_id.id if self.phase_id else None,
                'status': 'sent',
                'command_description': self.command_description or f'{self.command_type} command',
            })

            message = _('Control command sent successfully to device: %s') % self.device_id.name
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Success'),
                    'message': message,
                    'type': 'success'
                }
            }
        else:
            raise ValidationError(_("Failed to send command to device."))




class PrecisionIotMultipleReadingsWizard(models.TransientModel):
    _name = 'precision.iot.multiple.readings.wizard'
    _description = 'Precision IoT Multiple Readings Wizard'

    device_id = fields.Many2one('precision.iot.device', string='IoT Device', required=True)
    production_id = fields.Many2one('mrp.production', string='Production Order')
    phase_id = fields.Many2one('precision.recipe.phase', string='Phase',
                              domain="[('production_id', '=', production_id)]")
    read_datetime = fields.Datetime('Reading Time', default=fields.Datetime.now)

    # Dynamic fields for sensor readings
    reading_line_ids = fields.One2many('precision.iot.reading.line.wizard', 'wizard_id', string='Sensor Readings')

    @api.onchange('device_id')
    def _onchange_device_id(self):
        """Load all active sensors from the selected device"""
        if self.device_id:
            # Clear existing lines
            self.reading_line_ids = [(5, 0, 0)]

            # Add a line for each active sensor on the device
            for sensor in self.device_id.sensor_ids.filtered(lambda s: s.is_active):
                self.reading_line_ids += [(0, 0, {
                    'sensor_id': sensor.id,
                    'uom': sensor.unit_of_measure,
                    'value': sensor.current_value or 0.0
                })]

    def action_apply_multiple_readings(self):
        """Apply all readings to create IoT reading records"""
        if not self.reading_line_ids:
            raise ValidationError(_("No readings to apply."))

        readings_data = []
        for line in self.reading_line_ids:
            if line.value is None or line.value == '':
                continue  # Skip empty readings

            readings_data.append({
                'device_id': self.device_id.id,
                'sensor_id': line.sensor_id.id,
                'value': line.value,
                'read_datetime': self.read_datetime or fields.Datetime.now(),
                'production_id': self.production_id.id if self.production_id else False,
                'phase_id': self.phase_id.id if self.phase_id else False,
            })

        if readings_data:
            # Create all readings at once
            readings = self.env['precision.iot.reading'].create_batch_readings(readings_data)

            # Check for any critical deviations
            critical_readings = readings.filtered(lambda r: r.is_deviation_critical)
            if critical_readings:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('Critical Deviations Detected'),
                        'message': f'{len(critical_readings)} critical deviation(s) detected from IoT sensors. Production may be locked for safety.',
                        'type': 'warning',
                        'sticky': True
                    }
                }

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': f'{len([r for r in readings_data if r])} IoT reading(s) have been recorded successfully.',
                'type': 'success'
            }
        }


class PrecisionIotReadingLineWizard(models.TransientModel):
    _name = 'precision.iot.reading.line.wizard'
    _description = 'Precision IoT Reading Line Wizard'

    wizard_id = fields.Many2one('precision.iot.multiple.readings.wizard', string='Wizard', ondelete='cascade')
    sensor_id = fields.Many2one('precision.iot.sensor', string='Sensor', required=True)
    value = fields.Float('Reading Value', required=True)
    uom = fields.Char('Unit of Measure')
    is_valid = fields.Boolean('Valid', compute='_compute_validation')
    validation_message = fields.Char('Validation Message', compute='_compute_validation')

    @api.depends('sensor_id', 'value')
    def _compute_validation(self):
        for record in self:
            if record.sensor_id and record.value is not None:
                is_valid, message = record.sensor_id.action_validate_reading(record.value)
                record.is_valid = is_valid
                record.validation_message = message
            else:
                record.is_valid = True
                record.validation_message = ""