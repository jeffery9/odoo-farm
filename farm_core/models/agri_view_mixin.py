from odoo import models, fields, api

class AgriViewMixin(models.AbstractModel):
    """
    [Level 4: Cognitive Interface] - UI/UX adaptation mixin for agricultural entities.
    Handles semantic term mapping and specific display logic for de-industrialized UX.
    """
    _name = 'agri.view.mixin'
    _description = 'Agri UI/UX View Adaptation Mixin'

    def _get_agri_view_context(self):
        """Returns standard agricultural context for views"""
        return {
            'is_agri_view': True,
            'de_industrialize': True
        }

    @api.model
    def _apply_agri_term_mapping(self, arch):
        """
        Logic to dynamically transform industrial terms (MO/BOM) into agricultural terms.
        Stub for front-end integration.
        """
        return arch
