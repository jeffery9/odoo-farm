from odoo import models, fields, api
import lxml.etree as ET

class AgriViewMixin(models.AbstractModel):
    """
    [Level 4: Cognitive Interface] - UI/UX adaptation mixin for agricultural entities.
    Handles semantic term mapping and specific display logic for de-industrialized UX.
    """
    _name = 'agri.view.mixin'
    _description = 'Agri UI/UX View Adaptation Mixin'

    @api.model
    def get_view(self, view_id=None, view_type='form', **options):
        res = super().get_view(view_id=view_id, view_type=view_type, **options)
        # Always de-industrialize if this mixin is present, or check context
        arch_node = res['arch']
        # Convert string to lxml if it's a string (though Odoo 17+ get_view usually returns a node or string depending on version)
        # In Odoo 19, it's typically a string in the dict.
        new_arch = self._apply_agri_term_mapping(arch_node)
        res['arch'] = new_arch
        return res

    @api.model
    def _apply_agri_term_mapping(self, arch):
        """
        Logic to dynamically transform industrial terms (MO/BOM) into agricultural terms.
        """
        if not arch:
            return arch
            
        mapping = {
            'Manufacturing Order': 'Agricultural Intervention',
            'Manufacturing Orders': 'Agricultural Interventions',
            'Bill of Materials': 'Agricultural Recipe',
            'Bills of Materials': 'Agricultural Recipes',
            'MO': 'Intervention',
            'Work Center': 'Processing Unit',
            'Work Centers': 'Processing Units',
        }
        
        content = arch
        for old, new in mapping.items():
            content = content.replace(f'string="{old}"', f'string="{new}"')
            content = content.replace(f'>{old}<', f'>{new}<')
            
        return content
