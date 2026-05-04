from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class QualityControlStandard(models.Model):
    """
    统一质检与品牌准入 [US-042-09]
    """
    _name = 'quality.control.standard'
    _description = 'Quality Control Standard'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Standard Name', required=True)
    code = fields.Char('Standard Code', required=True, copy=False)
    cooperative_id = fields.Many2one('cooperative.entity', string='Cooperative', required=True)
    product_category_id = fields.Many2one('product.category', string='Product Category')
    quality_threshold = fields.Float('Quality Threshold (%)', help='Minimum合格率 to pass')
    inspection_criteria = fields.Text('Inspection Criteria')
    certification_required = fields.Boolean('Certification Required')
    certification_standard = fields.Char('Certification Standard')
    is_active = fields.Boolean('Is Active', default=True)
    description = fields.Text('Description')

    @api.model
    def create(self, vals):
        if 'code' not in vals or not vals['code']:
            vals['code'] = self.env['ir.sequence'].next_by_code('quality.control.standard') or '/'
        return super().create(vals)

    def check_product_compliance(self, product_id, quality_score):
        """检查产品是否符合标准"""
        # This would be called to check if a product meets the quality standards
        if quality_score >= self.quality_threshold:
            return True
        return False