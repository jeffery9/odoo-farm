from odoo import models, fields, api, _
from datetime import date

class ResCompany(models.Model):
    _inherit = 'res.company'

    # 合作社备案信息 [US-041-08]
    unified_social_credit_code = fields.Char("Unified Social Credit Code")
    registration_no = fields.Char("Registration No.")
    entity_type = fields.Selection([
        ('family_farm', 'Family Farm'),
        ('cooperative', 'Cooperative'),
        ('enterprise', 'Agricultural Enterprise'),
    ], string="Entity Type")
    
    # 证照管理
    license_attachment_ids = fields.Many2many('ir.attachment', 'company_license_rel', 'company_id', 'attachment_id', string="Electronic Licenses")
    license_expiry_date = fields.Date("License Expiry Date")
    
    is_license_expired = fields.Boolean("License Expired", compute='_compute_license_status')

    @api.depends('license_expiry_date')
    def _compute_license_status(self):
        today = date.today()
        for company in self:
            company.is_license_expired = company.license_expiry_date and company.license_expiry_date < today

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    unified_social_credit_code = fields.Char(related='company_id.unified_social_credit_code', readonly=False)
    registration_no = fields.Char(related='company_id.registration_no', readonly=False)
    entity_type = fields.Selection(related='company_id.entity_type', readonly=False)
    license_expiry_date = fields.Date(related='company_id.license_expiry_date', readonly=False)
    license_attachment_ids = fields.Many2many(related='company_id.license_attachment_ids', readonly=False)
    is_license_expired = fields.Boolean(related='company_id.is_license_expired')

class FarmCooperativeMember(models.Model):
    _name = 'farm.cooperative.member'
    _description = 'Cooperative Member'

    company_id = fields.Many2one('res.company', string="Cooperative", required=True)
    partner_id = fields.Many2one('res.partner', string="Member Name", required=True)
    membership_date = fields.Date("Membership Date", default=fields.Date.today)
    share_capital = fields.Float("Share Capital")
    is_chairman = fields.Boolean("Is Chairman", default=False)
