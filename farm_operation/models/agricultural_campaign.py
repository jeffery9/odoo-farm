from odoo import models, fields

class AgriculturalCampaign(models.Model):
    _name = 'agricultural.campaign'
    _description = 'Agricultural Production Season'
    _order = 'date_start desc'
    _inherit = ['farm.agricultural.campaign.base']  # Use the shared base logic

    project_task_ids = fields.One2many(
        'project.task',
        'campaign_id',
        string="Associated Tasks"
    )
