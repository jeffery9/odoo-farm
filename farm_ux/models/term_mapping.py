from odoo import models, fields, api, _, tools
from odoo.exceptions import ValidationError
import logging
import re

_logger = logging.getLogger(__name__)


class TermMapping(models.Model):
    """
    Term Mapping Management [US-16-01]
    Stores industrial-to-agricultural term translations for 2026 de-industrialization.
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
        """Ensures unique mapping for a term within a language/region context."""
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
    @tools.ormcache('text', 'industry_context')
    def apply_term_mapping_to_text(self, text, industry_context='general'):
        """
        [US-16-01] Optimized term replacement engine.
        Applies active mappings to the provided text based on context.
        """
        if not text or not isinstance(text, str):
            return text

        # Cache-aware retrieval of active mappings
        term_mappings = self.search([
            ('is_active', '=', True),
            ('industry_context', 'in', ['general', industry_context])
        ])

        if not term_mappings:
            return text

        # Sort by length descending to prevent partial replacements (e.g. 'Manufacturing Order' vs 'Manufacturing')
        sorted_mappings = sorted(term_mappings, key=lambda x: len(x.source_term), reverse=True)

        for mapping in sorted_mappings:
            if mapping.source_term and mapping.target_term:
                # Case-insensitive replacement
                pattern = re.compile(re.escape(mapping.source_term), re.IGNORECASE)
                text = pattern.sub(mapping.target_term, text)

        return text

    def apply_term_mapping(self, text):
        """Backward compatibility call."""
        return self.apply_term_mapping_to_text(text)

    @api.model_create_multi
    def create(self, vals_list):
        self.env.registry.clear_cache()
        return super().create(vals_list)

    def write(self, vals):
        self.env.registry.clear_cache()
        return super().write(vals)

    def unlink(self):
        self.env.registry.clear_cache()
        return super().unlink()