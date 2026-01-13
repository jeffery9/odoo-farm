from odoo import models, fields, api

class AgriculturalCampaign(models.Model):
    _inherit = 'agricultural.campaign'

    # 汇总该生产季下所有任务的养分投入
    total_n = fields.Float("Total Nitrogen (kg)", compute='_compute_campaign_nutrients', store=True)
    total_p = fields.Float("Total Phosphorus (kg)", compute='_compute_campaign_nutrients', store=True)
    total_k = fields.Float("Total Potassium (kg)", compute='_compute_campaign_nutrients', store=True)

    # 减量化对比指标 [US-08-03]
    n_reduction_rate = fields.Float("N Reduction %", compute='_compute_reduction_rates')
    p_reduction_rate = fields.Float("P Reduction %", compute='_compute_reduction_rates')
    k_reduction_rate = fields.Float("K Reduction %", compute='_compute_reduction_rates')

    def _compute_reduction_rates(self):
        for campaign in self:
            # 寻找同家族的上一个产季
            prev_campaign = self.search([
                ('date_start', '<', campaign.date_start or fields.Date.today()),
                ('id', '!=', campaign.id)
            ], order='date_start desc', limit=1)
            
            if prev_campaign and prev_campaign.total_n > 0:
                campaign.n_reduction_rate = ((prev_campaign.total_n - campaign.total_n) / prev_campaign.total_n) * 100
            else:
                campaign.n_reduction_rate = 0.0
                
            if prev_campaign and prev_campaign.total_p > 0:
                campaign.p_reduction_rate = ((prev_campaign.total_p - campaign.total_p) / prev_campaign.total_p) * 100
            else:
                campaign.p_reduction_rate = 0.0

            if prev_campaign and prev_campaign.total_k > 0:
                campaign.k_reduction_rate = ((prev_campaign.total_k - campaign.total_k) / prev_campaign.total_k) * 100
            else:
                campaign.k_reduction_rate = 0.0

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
        ('biodiversity', 'Biodiversity'),
        ('soil_health', 'Soil Health'),
        ('water_protection', 'Water Protection')
    ], string="Impact Category", required=True)
