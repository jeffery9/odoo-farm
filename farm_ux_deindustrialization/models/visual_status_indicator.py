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
    model_name = fields.Char('Model Name', required=True, help='The model this indicator applies to (e.g. mrp.production)')
    field_name = fields.Char('Field Name', required=True, help='The field to monitor for status changes')
    evaluation_logic = fields.Text('Evaluation Logic', help='Python lambda function to evaluate status (e.g. lambda record: record.state == "done" and "green" or "red")')
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
    icon = fields.Char('Icon', help='Font Awesome icon (e.g. fa-check, fa-warning)')
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
    display_on_mobile = fields.Boolean('Display on Mobile', default=True)
    description = fields.Text('Description', translate=True)

    def evaluate_status(self, record):
        """动态评估记录的状态"""
        if self.evaluation_logic and self.is_active:
            try:
                # 安全地执行评估逻辑
                # 这里实际在前端或业务逻辑中，会根据评估逻辑来计算状态
                import ast
                import operator
                # 实现安全的评估
                pass
            except Exception:
                return 'secondary'  # 默认状态
        return 'secondary'