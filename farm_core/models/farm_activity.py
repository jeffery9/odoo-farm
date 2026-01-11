from odoo import models, fields

class FarmActivity(models.Model):
    _inherit = 'project.project'

    is_agri_activity = fields.Boolean(
        string="Is Agricultural Activity", 
        default=False,
        help="Mark this project as an agricultural activity to enable specialized features."
    )
    
    activity_family = fields.Selection([
        ('planting', 'Planting (种植)'),
        ('livestock', 'Livestock (畜牧)'),
        ('aquaculture', 'Aquaculture (养鱼/水产)'),
        ('agritourism', 'Agritourism (观光农业)'),
    ], string="Activity Family", help="Specify the agricultural sector.")
