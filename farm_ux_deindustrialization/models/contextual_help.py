from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class ContextualHelp(models.Model):
    """
    上下文帮助 [US-16-05]
    """
    _name = 'contextual.help'
    _description = 'Smart Contextual Help for Agricultural Operations'

    name = fields.Char('Help Topic', required=True, translate=True)
    model_name = fields.Char('Model Name', required=True, help='Model this help applies to')
    field_name = fields.Char('Field Name', help='Specific field this help applies to')
    view_type = fields.Selection([
        ('form', 'Form View'),
        ('list', 'List View'),
        ('kanban', 'Kanban View'),
        ('calendar', 'Calendar View'),
        ('graph', 'Graph View'),
        ('pivot', 'Pivot View'),
    ], string='View Type', default='form')
    help_content = fields.Html('Help Content', translate=True, help='HTML content for the help text')
    help_video_url = fields.Char('Video Tutorial URL', help='URL to video tutorial')
    help_image = fields.Binary('Help Image', help='Image for visual instruction')
    image_name = fields.Char('Image Name')
    is_active = fields.Boolean('Is Active', default=True)
    priority = fields.Integer('Priority', default=10, help='Display priority (lower numbers displayed first)')
    target_roles = fields.Many2many('res.groups', string='Target Roles', help='Roles this help is intended for')
    industry_context = fields.Selection([
        ('general', 'General Agriculture'),
        ('planting', 'Planting'),
        ('livestock', 'Livestock'),
        ('aquaculture', 'Aquaculture'),
        ('winemaking', 'Winemaking'),
        ('bakery', 'Bakery'),
        ('dairy', 'Dairy'),
        ('processing', 'Processing'),
    ], string='Industry Context', default='general')
    difficulty_level = fields.Selection([
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ], string='Difficulty Level', default='beginner')
    # related_faq_ids = fields.Many2many('faq.entry', string='Related FAQ Entries')

    def get_contextual_help(self, model_name, field_name=None, view_type=None):
        """获取上下文相关的帮助"""
        domain = [('model_name', '=', model_name), ('is_active', '=', True)]
        if field_name:
            domain.append(('field_name', '=', field_name))
        if view_type:
            domain.append(('view_type', '=', view_type))
        
        return self.search(domain, order='priority asc')