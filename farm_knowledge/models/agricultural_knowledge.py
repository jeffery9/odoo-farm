from odoo import models, fields, api, _

class AgriculturalKnowledge(models.Model):
    """
    农业知识库 [US-16-06]
    """
    _name = 'agricultural.knowledge'
    _description = 'Agricultural Knowledge Base'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Title', required=True, translate=True)
    content = fields.Html(string='Content', translate=True)
    
    category = fields.Selection([
        ('crop_varieties', 'Crop Varieties'),
        ('cultivation', 'Cultivation Techniques'),
        ('pest_disease', 'Pest & Disease'),
        ('fertilization', 'Fertilization'),
        ('irrigation', 'Irrigation'),
        ('harvesting', 'Harvesting'),
        ('processing', 'Processing'),
        ('marketing', 'Marketing'),
        ('regulations', 'Regulations'),
        ('best_practices', 'Best Practices'),
    ], string='Category', default='cultivation')
    
    knowledge_type = fields.Selection([
        ('article', 'Knowledge Article'),
        ('case_study', 'Best Practice Case'),
        ('standard', 'Standard Operating Procedure'),
    ], string='Knowledge Type', default='article')

    tags = fields.Char(string='Tags', help='Comma-separated tags for search')
    active = fields.Boolean(default=True)
    author_id = fields.Many2one('res.users', string='Author', default=lambda self: self.env.user)
    
    difficulty_level = fields.Selection([
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
    ], string='Difficulty Level', default='beginner')
    
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
    
    seasonality = fields.Selection([
        ('spring', 'Spring'),
        ('summer', 'Summer'),
        ('autumn', 'Autumn'),
        ('winter', 'Winter'),
        ('year_round', 'Year Round'),
    ], string='Seasonality', default='year_round')
    
    video_url = fields.Char(string='Video URL')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    
    view_count = fields.Integer(string='View Count', default=0, readonly=True)
    helpful_count = fields.Integer(string='Helpful Count', default=0, readonly=True)

    pest_disease_id = fields.Many2one('farm.pest.disease', string="Related Pest/Disease")

    @api.model
    def smart_search(self, keywords):
        """US-16-06: 智能搜索"""
        if not keywords:
            return self.browse()
        domain = [
            '|', '|', '|',
            ('name', 'ilike', keywords),
            ('content', 'ilike', keywords),
            ('tags', 'ilike', keywords),
            ('category', 'ilike', keywords)
        ]
        return self.search(domain)

    def action_mark_helpful(self):
        self.ensure_one()
        self.helpful_count += 1
