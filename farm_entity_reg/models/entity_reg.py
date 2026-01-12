from odoo import models, fields, api, _
from datetime import date

class ResCompany(models.Model):
    _inherit = 'res.company'

    # 家庭农场/合作社备案信息 [US-18-08]
    unified_social_credit_code = fields.Char("Unified Social Credit Code (统一社会信用代码)")
    registration_no = fields.Char("Registration No. (备案编号)")
    entity_type = fields.Selection([
        ('family_farm', 'Family Farm (家庭农场)'),
        ('cooperative', 'Cooperative (合作社)'),
        ('enterprise', 'Agricultural Enterprise (农业企业)'),
    ], string="Entity Type")
    
    # 证照管理
    license_attachment_ids = fields.Many2many('ir.attachment', 'company_license_rel', 'company_id', 'attachment_id', string="Electronic Licenses (电子证照)")
    license_expiry_date = fields.Date("License Expiry Date")
    
    is_license_expired = fields.Boolean("License Expired", compute='_compute_license_status')

    @api.depends('license_expiry_date')
    def _compute_license_status(self):
        today = date.today()
        for company in self:
            company.is_license_expired = company.license_expiry_date and company.license_expiry_date < today

class FarmCooperativeMember(models.Model):
    _name = 'farm.cooperative.member'
    _description = 'Cooperative Member'

    company_id = fields.Many2one('res.company', string="Cooperative", required=True)
    partner_id = fields.Many2one('res.partner', string="Member Name", required=True)
    membership_date = fields.Date("Membership Date", default=fields.Date.today)
    share_capital = fields.Float("Share Capital (股金)")
    is_chairman = fields.Boolean("Is Chairman", default=False)
