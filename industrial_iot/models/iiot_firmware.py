# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re


class IiotFirmware(models.Model):
    _name = 'iiot.firmware'
    _description = 'Industrial IoT Firmware'
    _order = 'version DESC'

    name = fields.Char('Name', compute='_compute_name', store=True)
    version = fields.Char('Version', required=True, help='Firmware version number')
    profile_code = fields.Char('Device Type', required=True, help='Applicable device type code')
    url = fields.Char('Download URL', required=True, help='Firmware download URL')
    checksum = fields.Char('Checksum', help='Firmware file checksum')
    description = fields.Text('Description')
    is_active = fields.Boolean('Active', default=True, help='Is this an active version?')
    created_date = fields.Datetime('Created Date', default=fields.Datetime.now)

    _sql_constraints = [
        ('version_profile_uniq', 'UNIQUE(version, profile_code)', 'Firmware version must be unique for each device type!'),
    ]

    @api.depends('version', 'profile_code')
    def _compute_name(self):
        for firmware in self:
            firmware.name = f"{firmware.profile_code} v{firmware.version}"

    @api.constrains('version')
    def _check_version_format(self):
        for record in self:
            # Basic version format check (e.g., x.y.z)
            if not re.match(r'^[a-zA-Z0-9._-]+$', record.version):
                raise ValidationError(_("Version format is incorrect, can only contain letters, numbers, dots, underscores and hyphens"))

    @api.constrains('url')
    def _check_url_format(self):
        for record in self:
            if record.url and not record.url.startswith(('http://', 'https://', 'ftp://')):
                raise ValidationError(_("URL format is incorrect, please use http://, https:// or ftp:// prefix"))

    def action_deactivate(self):
        """Deactivate firmware version"""
        self.write({'is_active': False})
        return True

    def action_activate(self):
        """Activate firmware version"""
        self.write({'is_active': True})
        return True


class IiotUpdate(models.Model):
    _name = 'iiot.update'
    _description = 'Industrial IoT Firmware Update'
    _order = 'create_date DESC'

    name = fields.Char('Update Name', compute='_compute_name', store=True)
    device_id = fields.Many2one('iiot.device', 'Target Device', required=True)
    firmware_id = fields.Many2one('iiot.firmware', 'Firmware Version', required=True)
    update_id = fields.Char('Update ID', default=lambda self: self._generate_update_id(), readonly=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('downloading', 'Downloading'),
        ('installing', 'Installing'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='pending', required=True)
    start_time = fields.Datetime('Start Time')
    end_time = fields.Datetime('End Time')
    error_message = fields.Text('Error Message')
    progress = fields.Float('Progress', default=0.0, help='Update progress percentage (0.0-100.0)')
    description = fields.Text('Description')

    @api.depends('device_id', 'firmware_id')
    def _compute_name(self):
        for update in self:
            if update.device_id and update.firmware_id:
                update.name = f"{update.device_id.device_id} -> {update.firmware_id.version}"
            else:
                update.name = "Incomplete update task"

    @api.model
    def _generate_update_id(self):
        import uuid
        return str(uuid.uuid4())

    def action_send_ota(self):
        """Send OTA update command to device"""
        for update in self:
            if update.status != 'pending':
                continue

            # Send OTA notification to device
            try:
                # Get the OTA notification topic
                ota_topic = update.device_id.profile_id.ota_notify_topic_template.format(
                    device=update.device_id.device_id
                )

                # Prepare OTA command payload
                payload = {
                    'command': 'ota_update',
                    'update_id': update.update_id,
                    'firmware_url': update.firmware_id.url,
                    'checksum': update.firmware_id.checksum,
                    'version': update.firmware_id.version
                }

                # Send via device's send_command method
                update.device_id.send_command('ota_update', **{
                    'update_id': update.update_id,
                    'firmware_url': update.firmware_id.url,
                    'checksum': update.firmware_id.checksum,
                    'version': update.firmware_id.version
                })

                # Update status
                update.write({
                    'status': 'sent',
                    'start_time': fields.Datetime.now()
                })

            except Exception as e:
                update.write({
                    'status': 'failed',
                    'error_message': str(e)
                })

    def update_status_from_device(self, new_status, progress=None, error_message=None):
        """Update status from device"""
        vals = {'status': new_status}
        if progress is not None:
            vals['progress'] = progress
        if error_message is not None:
            vals['error_message'] = error_message
        if new_status in ['success', 'failed']:
            vals['end_time'] = fields.Datetime.now()

        self.write(vals)

    def action_cancel_update(self):
        """Cancel update task"""
        for update in self:
            if update.status in ['pending', 'sent']:
                update.write({
                    'status': 'cancelled',
                    'end_time': fields.Datetime.now()
                })