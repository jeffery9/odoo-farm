from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re

class DouyinQualification(models.Model):
    """
    US-21-01: 抖音入驻资质预审
    职责：小店所需的法定资料
    """
    _name = 'douyin.qualification'
    _description = 'Douyin Onboarding Qualification'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Application Title", required=True, default="New Douyin Application")
    company_id = fields.Many2one('res.company', string="Farm Company", default=lambda self: self.env.company)
    
    # 核心资质信息
    business_license = fields.Binary("Business License", required=True)
    uscc = fields.Char("Unified Social Credit Code", required=True)
    
    legal_person_name = fields.Char("Legal Representative", required=True)
    id_card_front = fields.Binary("ID Card Front")
    id_card_back = fields.Binary("ID Card Back")
    
    # 行业特定资质
    food_license = fields.Binary("Food Business License")
    cert_expiry_date = fields.Date("License Expiry Date")
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('validating', 'Self-Validating'),
        ('passed', 'Pre-audit Passed'),
        ('rejected', 'Data Missing')
    ], default='draft', tracking=True)

    @api.constrains('uscc')
    def _check_uscc_format(self):
        for rec in self:
            # 中国统一社会信用代码为 18 位
            if rec.uscc and not re.match(r'^[0-9A-Z]{18}$', rec.uscc):
                raise ValidationError(_("Unified Social Credit Code must be 18 characters (Numbers and Uppercase letters)."))

    def action_perform_pre_audit(self):
        """ 执行系统自动化预审逻辑 """
        self.ensure_one()
        errors = []
        
        if not self.business_license: errors.append("Missing Business License image.")
        if not self.id_card_front or not self.id_card_back: errors.append("Missing ID Card photos.")
        
        if self.cert_expiry_date and self.cert_expiry_date < fields.Date.today():
            errors.append("Qualification has expired.")
            
        if errors:
            self.state = 'rejected'
            self.message_post(body=_("Pre-audit failed: <br/>") + "<br/>".join(errors))
        else:
            self.state = 'passed'
            self.message_post(body=_("Congratulations! Internal pre-audit passed. You are ready to apply on Douyin Platform."))

    def action_go_to_douyin_register(self):
        """ 引导跳转至抖音企业号开通官网 """
        return {
            'type': 'ir.actions.act_url',
            'url': 'https://e.douyin.com/site/',
            'target': 'new',
        }
