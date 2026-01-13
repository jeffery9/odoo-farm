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
    source_term = fields.Char('Source Term (Industrial)', required=True,
                              help='Original industrial term (e.g. Manufacturing Order)')
    target_term = fields.Char('Target Term (Agricultural)', required=True,
                              help='Agricultural equivalent term (e.g. Intervention)')
    language_code = fields.Char(
        'Language Code', default='zh_CN', help='Language code for localization')
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
    region_specific = fields.Boolean(
        'Region Specific', help='Is this term specific to certain regions?')
    region_code = fields.Char(
        'Region Code', help='Specific region code if region-specific')
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

                raise ValidationError(
                    _("Term mapping already exists for '%s' in this language/region context") % record.source_term)

    @api.model
    def apply_term_mapping_to_text(self, text):
        """应用术语映射到文本"""

        if not text or not isinstance(text, str):

            return text

        # 获取活跃的术语映射

        term_mappings = self.search([('is_active', '=', True)])

        if not term_mappings:

            return text

        # 按长度排序，优先替换较长的术语

        sorted_mappings = sorted(
            term_mappings, key=lambda x: len(x.source_term), reverse=True)

        import re

        for mapping in sorted_mappings:

            if mapping.source_term and mapping.target_term:

                # 使用正则表达式进行词边界匹配，避免部分替换

                # 注意：对于中文，词边界 \b 可能不起作用，这里简单处理

                pattern = re.escape(mapping.source_term)

                text = re.sub(pattern, mapping.target_term,
                              text, flags=re.IGNORECASE)

        return text

    def apply_term_mapping(self, text):
        """兼容旧方法的调用"""

        return self.apply_term_mapping_to_text(text)
