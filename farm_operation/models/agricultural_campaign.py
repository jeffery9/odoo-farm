from odoo import models, fields

class AgriculturalCampaign(models.Model):
    _name = 'agricultural.campaign'
    _description = 'Agricultural Production Season'
    _order = 'date_start desc'

    name = fields.Char("Season Name", required=True)
    date_start = fields.Date("Start Date")
    date_end = fields.Date("End Date")
    is_active = fields.Boolean("Active", default=True)
    description = fields.Text("Description")
    
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
