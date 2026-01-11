from odoo import models, fields

class AgriIntervention(models.Model):
    _inherit = 'mrp.production'

    agri_task_id = fields.Many2one(
        'project.task', 
        string="Production Task",
        help="The specific production task this intervention belongs to."
    )
    
    # 增加农业特有的作业分类（可选，基于 mrp 原生字段扩展）
    intervention_type = fields.Selection([
        ('tillage', 'Soil Preparation (耕作)'),
        ('sowing', 'Sowing/Planting (播种/移栽)'),
        ('fertilizing', 'Fertilizing (施肥)'),
        ('irrigation', 'Irrigation (灌溉)'),
        ('protection', 'Crop Protection (植保)'),
        ('harvesting', 'Harvesting (收获)'),
        ('feeding', 'Feeding (饲喂)'),
        ('medical', 'Medical/Prevention (医疗/防疫)'),
    ], string="Intervention Type")
