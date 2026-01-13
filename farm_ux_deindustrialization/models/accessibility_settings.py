from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class AccessibilitySettings(models.Model):
    """
    无障碍设置 [US-16-09]
    """
    _name = 'accessibility.settings'
    _description = 'Accessibility & Inclusive Design Settings'

    name = fields.Char('Setting Name', required=True, translate=True)
    user_id = fields.Many2one('res.users', string='User', required=True, default=lambda self: self.env.user)
    screen_reader_enabled = fields.Boolean('Screen Reader Enabled', help='Enable screen reader compatibility')
    keyboard_navigation = fields.Boolean('Keyboard Navigation', help='Enable keyboard-only navigation')
    font_scaling = fields.Float('Font Scaling Factor', default=1.0, help='Scale factor for all fonts (1.0 = normal)')
    high_contrast_mode = fields.Boolean('High Contrast Mode', help='Enable high contrast color scheme')
    large_touch_targets = fields.Boolean('Large Touch Targets', help='Enable larger touch targets for easier interaction')
    reduced_motion = fields.Boolean('Reduced Motion', help='Reduce animations and motion effects')
    color_blind_mode = fields.Boolean('Color Blind Mode', help='Adjust colors for color blindness')
    voice_navigation = fields.Boolean('Voice Navigation', help='Enable voice-based navigation')
    font_family_preference = fields.Char('Font Family Preference', help='Preferred font family for accessibility')
    alternative_input_method = fields.Selection([
        ('none', 'None'),
        ('voice', 'Voice Control'),
        ('switch', 'Switch Control'),
        ('eye_tracking', 'Eye Tracking'),
    ], string='Alternative Input Method', default='none')
    voice_control_enabled = fields.Boolean('Voice Control Enabled', help='Enable voice commands')
    custom_color_scheme = fields.Char('Custom Color Scheme', help='Custom CSS for color adjustments')
    is_active = fields.Boolean('Is Active', default=True)
    last_updated = fields.Datetime('Last Updated', default=fields.Datetime.now)

    @api.constrains('font_scaling')
    def _check_font_scaling_range(self):
        """检查字体缩放范围"""
        for setting in self:
            if setting.font_scaling < 0.5 or setting.font_scaling > 3.0:
                raise ValidationError(_("Font scaling factor must be between 0.5 and 3.0"))