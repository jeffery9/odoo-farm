from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class MultiSensoryInteraction(models.Model):
    """
    多感官交互 [US-16-07]
    """
    _name = 'multi.sensory.interaction'
    _description = 'Multi-Sensory Interaction Configuration'

    name = fields.Char('Feature Name', required=True, translate=True)
    interaction_type = fields.Selection([
        ('voice_input', 'Voice Input'),
        ('gesture_control', 'Gesture Control'),
        ('audio_feedback', 'Audio Feedback'),
        ('haptic_feedback', 'Haptic Feedback'),
        ('visual_enhancement', 'Visual Enhancement'),
        ('large_touch_target', 'Large Touch Targets'),
    ], string='Interaction Type', required=True)
    model_name = fields.Char('Model Name', help='Model this feature applies to')
    field_name = fields.Char('Field Name', help='Field this feature applies to')
    is_enabled = fields.Boolean('Is Enabled', default=True)
    voice_commands = fields.Text('Voice Commands', help='JSON configuration of voice commands')
    gesture_mappings = fields.Text('Gesture Mappings', help='JSON configuration of gesture mappings')
    audio_notification = fields.Boolean('Audio Notification', help='Enable audio feedback')
    haptic_feedback = fields.Boolean('Haptic Feedback', help='Enable vibration feedback')
    visual_enhancement = fields.Boolean('Visual Enhancement', help='Enable visual enhancements')
    large_font_support = fields.Boolean('Large Font Support', help='Support large font mode')
    high_contrast_mode = fields.Boolean('High Contrast Mode', help='Support high contrast mode')
    screen_reader_compatible = fields.Boolean('Screen Reader Compatible', help='Compatible with screen readers')
    keyboard_shortcuts = fields.Text('Keyboard Shortcuts', help='JSON configuration of keyboard shortcuts')
    description = fields.Text('Description', translate=True)