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
        """ US-09-06: 供应商合规资质硬核查 """
        today = fields.Date.today()
        for order in self:
            # 只有当产品类别涉及合规要求时（如种子、农药）才强制核查
            # 这里简化为：如果供应商有任何农事证书记录，则必须有一张在有效期内
            if order.partner_id.agri_certification_ids:
                valid_certs = order.partner_id.agri_certification_ids.filtered(
                    lambda c: c.state == 'valid' and c.date_expiry >= today
                )
                if not valid_certs:
                    raise ValidationError(_(
                        "CORE-CLOSURE: 供应商 [%s] 的农业资质证书已过期或无效.\n"
                        "根据合规要求，严禁从资质失效的供应商处采购核心农资。"
                    ) % order.partner_id.name)
        return super(PurchaseOrder, self).button_confirm()
