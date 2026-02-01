# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class PrecisionIotCommandLog(models.Model):
    _name = 'precision.iot.command.log'
    _description = 'Precision IoT Command Log'
    _order = 'create_date desc'

    name = fields.Char('Command Reference', compute='_compute_name', store=True)
    device_id = fields.Many2one('precision.iot.device', string='IoT Device', required=True)
    command_type = fields.Selection([
        ('set_point', 'Set Control Point'),
        ('start_phase', 'Start Phase'),
        ('stop_phase', 'Stop Phase'),
        ('calibrate', 'Calibrate Device'),
        ('emergency_stop', 'Emergency Stop'),
        ('custom', 'Custom Command'),
    ], string='Command Type', required=True)
    command_value = fields.Float('Command Value')
    command_description = fields.Char('Command Description')
    status = fields.Selection([
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
        ('timeout', 'Timeout'),
    ], string='Status', default='sent', required=True)
    error_message = fields.Text('Error Message')

    # Precision production related fields
    production_id = fields.Many2one('mrp.production', string='Production Order')
    phase_id = fields.Many2one('precision.recipe.phase', string='Phase')

    # Response tracking
    response_received = fields.Boolean('Response Received')
    response_data = fields.Text('Response Data')
    execution_time = fields.Datetime('Execution Time')

    @api.depends('device_id', 'command_type', 'create_date')
    def _compute_name(self):
        for record in self:
            if record.device_id and record.command_type:
                record.name = f"{record.device_id.name} - {record.command_type} - {record.create_date}"
            else:
                record.name = "New Command Log"

    def action_resend_command(self):
        """Resend a failed command"""
        for log in self:
            if log.status == 'failed':
                device = log.device_id
                if device and device.iiot_device_id:
                    success = device.send_control_command(
                        log.command_type,
                        value=log.command_value,
                        target_phase_id=log.phase_id
                    )

                    if success:
                        log.write({
                            'status': 'sent',
                            'error_message': False
                        })
                    else:
                        raise _('Failed to resend command to device.')