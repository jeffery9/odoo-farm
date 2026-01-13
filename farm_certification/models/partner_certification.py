from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    agri_certification_ids = fields.One2many(
        'farm.partner.certification', 'partner_id', string="Agri Certifications"
    )
    has_valid_agri_cert = fields.Boolean(
        "Has Valid Agri Cert", compute='_compute_cert_status'
    )

    @api.depends('agri_certification_ids.date_expiry', 'agri_certification_ids.state')
    def _compute_cert_status(self):
        today = fields.Date.today()
        for partner in self:
            partner.has_valid_agri_cert = any(
                cert.state == 'valid' and cert.date_expiry >= today 
                for cert in partner.agri_certification_ids
            )

class FarmPartnerCertification(models.Model):
    _name = 'farm.partner.certification'
    _description = 'Supplier Agricultural Certification'

    partner_id = fields.Many2one('res.partner', string="Supplier", required=True, ondelete='cascade')
    cert_type = fields.Selection([
        ('organic', 'Organic (有机)'),
        ('green', 'Green Food (绿色食品)'),
        ('gi', 'Geographical Indication (地理标志)'),
        ('gap', 'GAP (良好农业规范)')
    ], string="Certification Type", required=True)
    cert_number = fields.Char("Certificate No.", required=True)
    date_start = fields.Date("Issue Date")
    date_expiry = fields.Date("Expiry Date", required=True)
    state = fields.Selection([
        ('valid', 'Valid'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked')
    ], string="Status", default='valid')

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        """ US-09-06: 供应商合规资质硬核查 + Activity 驱动工作流 """
        today = fields.Date.today()
        for order in self:
            if order.partner_id.agri_certification_ids:
                valid_certs = order.partner_id.agri_certification_ids.filtered(
                    lambda c: c.state == 'valid' and c.date_expiry >= today
                )
                if not valid_certs:
                    # 1. 创建合规补全 Activity [Workflow]
                    compliance_user = self.env.ref('farm_core.group_farm_admin').users[:1] # 演示逻辑：发给农场管理员
                    order.activity_schedule(
                        'mail.mail_activity_data_todo',
                        summary=_('供应商资质过期：需补全 [%s]') % order.partner_id.name,
                        note=_('该订单涉及核心农资采购，但供应商资质已失效。请立即更新资质文档，否则订单无法继续执行。'),
                        user_id=compliance_user.id if compliance_user else self.env.user.id
                    )
                    # 2. 抛出警告但不强制锁死，改为由 Activity 驱动后续动作
                    raise ValidationError(_(
                        "CORE-CLOSURE: 供应商 [%s] 农业资质已过期.\n"
                        "已自动为合规专员创建待办任务，请更新资质后再试。"
                    ) % order.partner_id.name)
        return super(PurchaseOrder, self).button_confirm()
