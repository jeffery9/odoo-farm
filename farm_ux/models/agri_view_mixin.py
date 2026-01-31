from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
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

            # 3. [Level 0+: Agri TODO Alert]
            # Inject a "Pending Community Contributions" banner into form views if needed
            if view_type == 'form' and self._name in ['mrp.production', 'stock.lot', 'res.partner']:
                todo_count = self.env['agri.clearing.ledger'].search_count([('state', '=', 'draft')])
                if todo_count > 0:
                    alert_div = etree.Element('div', {
                        'class': 'alert alert-info',
                        'role': 'alert',
                        'style': 'margin-bottom: 10px; font-weight: bold;'
                    })
                    alert_div.text = _("🌱 %d Community Contributions are awaiting your confirmation.") % todo_count
                    
                    header = doc.xpath("//header")
                    if header:
                        header[0].addprevious(alert_div)
                    else:
                        doc.insert(0, alert_div)

            res['arch'] = etree.tostring(doc, encoding='unicode')

        # 4. Replace strings in fields definitions (Field labels and help texts)
        if res.get('fields'):
            for field_name, field_info in res['fields'].items():
                if field_info.get('string'):
                    field_info['string'] = TermMapping.apply_term_mapping_to_text(field_info['string'])
                if field_info.get('help'):
                    field_info['help'] = TermMapping.apply_term_mapping_to_text(field_info['help'])

        return res

    def translate_exception(self, exception_msg):
        """
        Level 0 Deep Interception: Translates standard industrial errors to agricultural ones.
        Example: "Insufficient Stock for MO" -> "Input evidence missing for Intervention".
        """
        mapping = {
            'manufacturing order': _('agricultural intervention'),
            'bill of materials': _('cultivation recipe'),
            'work order': _('field task'),
            'insufficient stock': _('insufficient physical input evidence'),
            'inventory': _('resource registry'),
        }
        
        translated_msg = exception_msg.lower()
        for industrial, agri in mapping.items():
            translated_msg = translated_msg.replace(industrial, agri)
            
        return translated_msg.capitalize()

    def handle_validation_error(self, e):
        """
        Hook to be called in models to wrap validation errors with agricultural context.
        """
        agri_msg = self.translate_exception(str(e))
        raise ValidationError(agri_msg)
