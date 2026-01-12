from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class TermMapping(models.Model):
    """
    术语映射管理 [US-16-01]
    """
    _name = 'term.mapping'
    _description = 'Term Mapping for Agricultural Terminology'
    _order = 'source_term asc'

    name = fields.Char('Mapping Name', required=True, translate=True)
    source_term = fields.Char('Source Term (Industrial)', required=True, help='Original industrial term (e.g. Manufacturing Order)')
    target_term = fields.Char('Target Term (Agricultural)', required=True, help='Agricultural equivalent term (e.g. Intervention)')
    language_code = fields.Char('Language Code', default='zh_CN', help='Language code for localization')
    industry_context = fields.Selection([
        ('general', 'General Agriculture'),
        ('planting', 'Planting'),
        ('livestock', 'Livestock'),
        ('aquaculture', 'Aquaculture'),
        ('winemaking', 'Winemaking'),
        ('bakery', 'Bakery'),
        ('dairy', 'Dairy'),
        ('processing', 'Processing'),
    ], string='Industry Context', default='general')
    region_specific = fields.Boolean('Region Specific', help='Is this term specific to certain regions?')
    region_code = fields.Char('Region Code', help='Specific region code if region-specific')
    is_active = fields.Boolean('Is Active', default=True)
    description = fields.Text('Description', translate=True)
    example_usage = fields.Text('Example Usage', translate=True)

    @api.constrains('source_term', 'target_term')
    def _check_unique_mapping(self):
        """确保术语映射唯一"""
        for record in self:
            existing = self.search([
                ('source_term', '=', record.source_term),
                ('language_code', '=', record.language_code),
                ('region_code', '=', record.region_code or False),
                ('id', '!=', record.id)
            ])
            if existing:
                raise ValidationError(_("Term mapping already exists for '%s' in this language/region context") % record.source_term)

    def apply_term_mapping(self, text):
        """应用术语映射到文本"""
        for mapping in self.search([('is_active', '=', True)]):
            text = text.replace(mapping.source_term, mapping.target_term)
        return text