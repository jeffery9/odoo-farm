from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class VisualStatusIndicator(models.Model):
    """
    视觉状态标识 [US-16-03]
    """
    _name = 'visual.status.indicator'
    _description = 'Visual Status Indicator Configuration'

    name = fields.Char('Indicator Name', required=True, translate=True)
    status_type = fields.Selection([
        ('task', 'Task Status'),
        ('quality', 'Quality Status'),
        ('safety', 'Safety Status'),
        ('compliance', 'Compliance Status'),
        ('weather', 'Weather Alert'),
        ('equipment', 'Equipment Status'),
    ], string='Status Type', required=True)
    status_value = fields.Char('Status Value', required=True, help='Value to match (e.g. "pending", "in_progress", "done")')
    color_code = fields.Char('Color Code', default='#000000', help='CSS color code for the indicator')
    icon_class = fields.Char('Icon Class', help='CSS class for the icon (e.g. "fa fa-check")')
    badge_style = fields.Selection([
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('success', 'Success'),
        ('danger', 'Danger'),
        ('warning', 'Warning'),
        ('info', 'Info'),
    ], string='Badge Style', default='secondary')
    notification_sound = fields.Char('Notification Sound', help='Sound file for audio notifications')
    vibration_pattern = fields.Char('Vibration Pattern', help='Pattern for mobile vibration feedback')
    animation_effect = fields.Char('Animation Effect', help='CSS animation for status transitions')
    is_active = fields.Boolean('Is Active', default=True)
    description = fields.Text('Description', translate=True)