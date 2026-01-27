from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class ProductCertification(models.Model):
    """
    产品认证 [US-19-09]
    """
    _name = 'product.certification'
    _description = 'Product Certification'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Certification Name', required=True)
    code = fields.Char('Certification Code', required=True, copy=False)
    cooperative_id = fields.Many2one('cooperative.entity', string='Cooperative', required=True)
    member_id = fields.Many2one('cooperative.member', string='Member', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    standard_id = fields.Many2one('quality.control.standard', string='Quality Standard', required=True)
    certification_date = fields.Date('Certification Date', default=fields.Date.context_today)
    expiry_date = fields.Date('Expiry Date')
    quality_score = fields.Float('Quality Score (%)')
    is_certified = fields.Boolean('Is Certified', compute='_compute_certified_status', store=True)
    certification_document = fields.Binary('Certification Document')
    document_name = fields.Char('Document Name')
    description = fields.Text('Description')
    state = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ], string='State', default='pending', required=True)

    @api.model
    def create(self, vals):
        if 'code' not in vals or not vals['code']:
            vals['code'] = self.env['ir.sequence'].next_by_code('product.certification') or '/'
        return super().create(vals)

    @api.depends('quality_score', 'standard_id', 'expiry_date', 'state')
    def _compute_certified_status(self):
        for record in self:
            if (record.state == 'approved' and
                record.quality_score and
                record.standard_id and
                record.quality_score >= record.standard_id.quality_threshold and
                (not record.expiry_date or record.expiry_date >= fields.Date.context_today(self))):
                record.is_certified = True
            else:
                record.is_certified = False

    def action_approve(self):
        """批准认证"""
        for certification in self:
            certification.state = 'approved'

    def action_reject(self):
        """拒绝认证"""
        for certification in self:
            certification.state = 'rejected'