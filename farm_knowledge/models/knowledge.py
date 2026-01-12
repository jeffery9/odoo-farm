from odoo import models, fields, api, _

class FarmPestDisease(models.Model):
    _name = 'farm.pest.disease'
    _description = 'Pest & Disease Database'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Name", required=True) # e.g. "Wheat Rust"
    scientific_name = fields.Char("Scientific Name")
    category = fields.Selection([
        ('pest', 'Pest (虫害)'),
        ('disease', 'Disease (病害)'),
        ('weed', 'Weed (杂草)')
    ], required=True)
    
    symptoms = fields.Html("Symptoms Description")
    photo = fields.Binary("Reference Photo")
    
    # 推荐解决方案
    recommended_intervention_id = fields.Many2one('agri.intervention.template', string="Recommended Treatment")
    
    description = fields.Text("Detailed Description")

class FarmKnowledgeArticle(models.Model):
    _inherit = 'knowledge.article'

    # 关联到特定的病虫害条目，实现知识库与结构化数据的打通
    pest_disease_id = fields.Many2one('farm.pest.disease', string="Related Pest/Disease")
