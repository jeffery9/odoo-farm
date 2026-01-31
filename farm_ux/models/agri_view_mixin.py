from odoo import models, fields, api, _
import logging
from lxml import etree

_logger = logging.getLogger(__name__)


class AgriViewMixin(models.AbstractModel):
    """
    Mixin to isolate industrial terminology from the UI and replace it with agricultural terms.
    Implemented in farm_ux to manage terminology-driven UI transformation. [US-16-25]
    Level 0: UI De-industrialization Isolation
    """
    _name = 'agri.view.mixin'
    _description = 'Agricultural View Interceptor Mixin'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        """
        Intercept the view architecture and dynamically replace industrial terms
        using the central term.mapping repository.
        """
        res = super(AgriViewMixin, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )
        
        # Access the term mapping service
        TermMapping = self.env['term.mapping']
        
        if res.get('arch'):
            doc = etree.fromstring(res['arch'])
            
            # 1. Replace strings in the XML architecture (Labels, Strings)
            for node in doc.xpath("//*[@string]"):
                node.set('string', TermMapping.apply_term_mapping_to_text(node.get('string')))
            
            # 2. Replace titles in form/tree/kanban/search
            for node in doc.xpath("//form | //tree | //kanban | //search"):
                if node.get('string'):
                    node.set('string', TermMapping.apply_term_mapping_to_text(node.get('string')))

            res['arch'] = etree.tostring(doc, encoding='unicode')

        # 3. Replace strings in fields definitions (Field labels and help texts)
        if res.get('fields'):
            for field_name, field_info in res['fields'].items():
                if field_info.get('string'):
                    field_info['string'] = TermMapping.apply_term_mapping_to_text(field_info['string'])
                if field_info.get('help'):
                    field_info['help'] = TermMapping.apply_term_mapping_to_text(field_info['help'])

        return res
