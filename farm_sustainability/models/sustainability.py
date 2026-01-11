from odoo import models, fields, api

class AgriculturalCampaign(models.Model):
    _inherit = 'agricultural.campaign'

    # 汇总该生产季下所有任务的养分投入
    total_n = fields.Float("Total Nitrogen (kg)", compute='_compute_campaign_nutrients', store=True)
    total_p = fields.Float("Total Phosphorus (kg)", compute='_compute_campaign_nutrients', store=True)
    total_k = fields.Float("Total Potassium (kg)", compute='_compute_campaign_nutrients', store=True)

    @api.depends('project_ids.task_ids.total_n', 'project_ids.task_ids.total_p', 'project_ids.task_ids.total_k')
    def _compute_campaign_nutrients(self):
        for campaign in self:
            tasks = self.env['project.task'].search([('campaign_id', '=', campaign.id)])
            campaign.total_n = sum(tasks.mapped('total_n'))
            campaign.total_p = sum(tasks.mapped('total_p'))
            campaign.total_k = sum(tasks.mapped('total_k'))

class FarmEcologicalActivity(models.Model):
    _name = 'farm.ecological.activity'
    _description = 'Ecological Maintenance Activity'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Activity Name", required=True) # e.g., Buffer zone weeding, Hedge planting
    date = fields.Date("Date", default=fields.Date.today)
    location_id = fields.Many2one('stock.location', string="Land Parcel/Zone", domain=[('is_land_parcel', '=', True)])
    description = fields.Text("Description")
    impact_category = fields.Selection([
        ('biodiversity', 'Biodiversity (生物多样性)'),
        ('soil_health', 'Soil Health (土壤健康)'),
        ('water_protection', 'Water Protection (水资源保护)')
    ], string="Impact Category", required=True)
