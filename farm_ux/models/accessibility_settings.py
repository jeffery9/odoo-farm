from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class AccessibilitySettings(models.Model):
    """
    无障碍设置 [US-039-09]
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
    
    # Inclusive Design for diverse workforce [US-095-01]
    inclusive_mode = fields.Boolean('Inclusive/Elder Mode', 
                                   help='Simplified UI with large fonts (1.5x) and high contrast for aging or low-digital-literacy workforce.')
    voice_entry_enabled = fields.Boolean('Voice-First Entry', 
                                        help='Prioritize voice input for recording farm activities.')
    
    voice_navigation = fields.Boolean('Voice Navigation', help='Enable voice-based navigation')

    font_family_preference = fields.Selection([('sans-serif', 'Sans-Serif'), ('serif', 'Serif'), ('dyslexic', 'Dyslexia Friendly')], default='sans-serif', string='Font Family')
    alternative_input_method = fields.Selection([('none', 'None'), ('eye_tracking', 'Eye Tracking'), ('switch', 'Switch Access')], default='none', string='Alternative Input')
    voice_control_enabled = fields.Boolean('Voice Control Enabled')
    is_active = fields.Boolean('Is Active', default=True)
    last_updated = fields.Datetime('Last Updated')

    custom_color_scheme = fields.Char('Custom Color Scheme')


    
    # UI Simplification
    hide_advanced_menus = fields.Boolean('Hide Advanced Menus', default=True, help="Hide configuration and complex menus.")
    simplified_kanban = fields.Boolean('Simplified Kanban Cards', default=True, help="Show only essential status and action buttons.")

    @api.constrains('font_scaling')
    def _check_font_scaling_range(self):
        """检查字体缩放范围"""
        for setting in self:
            if setting.font_scaling < 0.5 or setting.font_scaling > 3.0:
                raise ValidationError(_("Font scaling factor must be between 0.5 and 3.0"))

    @api.onchange('inclusive_mode')
    def _onchange_inclusive_mode(self):
        """US-095-01: Auto-preset accessibility for Elder Mode"""
        if self.inclusive_mode:
            self.font_scaling = 1.5
            self.large_touch_targets = True
            self.high_contrast_mode = True
            self.hide_advanced_menus = True
            self.simplified_kanban = True
            self.voice_entry_enabled = True

    