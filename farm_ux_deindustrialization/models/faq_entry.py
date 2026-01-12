from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class FAQEntry(models.Model):
    """
    常见问题条目 [US-16-05]
    """
    _name = 'faq.entry'
    _description = 'Frequently Asked Questions Entry'

    question = fields.Char('Question', required=True, translate=True)
    answer = fields.Html('Answer', required=True, translate=True)
    category = fields.Selection([
        ('general', 'General'),
        ('planting', 'Planting'),
        ('livestock', 'Livestock'),
        ('equipment', 'Equipment'),
        ('quality', 'Quality'),
        ('safety', 'Safety'),
        ('marketing', 'Marketing'),
        ('financial', 'Financial'),
        ('technical', 'Technical'),
    ], string='Category', default='general')
    is_active = fields.Boolean('Is Active', default=True)
    view_count = fields.Integer('View Count', default=0)
    helpful_count = fields.Integer('Helpful Count', default=0)
    not_helpful_count = fields.Integer('Not Helpful Count', default=0)
    related_help_ids = fields.Many2many('contextual.help', string='Related Help Topics')
    tags = fields.Char('Tags', help='Comma-separated tags for search')

    def increment_view_count(self):
        """增加查看计数"""
        for entry in self:
            entry.view_count += 1

    def mark_helpful(self):
        """标记为有用"""
        for entry in self:
            entry.helpful_count += 1

    def mark_not_helpful(self):
        """标记为无用"""
        for entry in self:
            entry.not_helpful_count += 1