from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class AgriculturalKnowledge(models.Model):
    """
    农业知识库 [US-16-06]
    """
    _name = 'agricultural.knowledge'
    _description = 'Agricultural Knowledge Base'
    _order = 'category, name'

    name = fields.Char('Knowledge Title', required=True, translate=True)
    category = fields.Selection([
        ('crop_varieties', 'Crop Varieties'),
        ('cultivation_techniques', 'Cultivation Techniques'),
        ('pest_disease', 'Pest & Disease'),
        ('fertilization', 'Fertilization'),
        ('irrigation', 'Irrigation'),
        ('harvesting', 'Harvesting'),
        ('processing', 'Processing'),
        ('marketing', 'Marketing'),
        ('regulations', 'Regulations'),
        ('best_practices', 'Best Practices'),
    ], string='Category', required=True)
    content = fields.Html('Content', translate=True)
    image_ids = fields.Many2many('ir.attachment', string='Images', domain=[('mimetype', '=like', 'image/%')])
    video_url = fields.Char('Video URL', help='URL to educational video')
    related_products = fields.Many2many('product.product', string='Related Products')
    related_tasks = fields.Many2many('project.task', string='Related Tasks')
    is_active = fields.Boolean('Is Active', default=True)
    author = fields.Char('Author', help='Knowledge author')
    publish_date = fields.Date('Publish Date', default=fields.Date.context_today)
    tags = fields.Char('Tags', help='Comma-separated tags for search')
    difficulty_level = fields.Selection([
        ('basic', 'Basic'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
    ], string='Difficulty Level', default='basic')
    industry_specific = fields.Selection([
        ('general', 'General Agriculture'),
        ('planting', 'Planting'),
        ('livestock', 'Livestock'),
        ('aquaculture', 'Aquaculture'),
        ('winemaking', 'Winemaking'),
        ('bakery', 'Bakery'),
        ('dairy', 'Dairy'),
        ('processing', 'Processing'),
    ], string='Industry Specific', default='general')
    seasonality = fields.Char('Seasonality', help='Applicable seasons (e.g. spring, summer)')

    def search_knowledge(self, keywords):
        """搜索知识库"""
        domain = [
            ('is_active', '=', True),
            '|', '|', '|',
            ('name', 'ilike', keywords),
            ('content', 'ilike', keywords),
            ('tags', 'ilike', keywords),
            ('category', 'ilike', keywords)
        ]
        return self.search(domain)