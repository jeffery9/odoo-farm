from odoo import models, fields, api, _

class FAQEntry(models.Model):
    """
    常见问题条目 [US-16-05]
    """
    _name = 'faq.entry'
    _description = 'Frequently Asked Questions'
    _order = 'sequence, id'

    sequence = fields.Integer(default=10)
    question = fields.Char(string='Question', required=True, translate=True)
    answer = fields.Html(string='Answer', required=True, translate=True)
    
    category = fields.Selection([
        ('general', 'General'),
        ('planting', 'Planting'),
        ('livestock', 'Livestock'),
        ('equipment', 'Equipment'),
        ('quality', 'Quality'),
        ('safety', 'Safety'),
    ], string='Category', default='general')
    
    active = fields.Boolean(default=True)
    tags = fields.Char(string='Tags')
    target_model = fields.Char("Target Model", help="Technical name of the model")
    knowledge_id = fields.Many2one('agricultural.knowledge', string='Detailed Article')