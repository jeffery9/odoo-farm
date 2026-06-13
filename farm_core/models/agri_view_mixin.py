from odoo import models, api

class AgriViewMixin(models.AbstractModel):
    """
    [Level 0: Foundation] - Base UI/UX adaptation mixin.
    Extended by farm_ux for advanced de-industrialization.
    """
    _name = 'agri.view.mixin'
    _description = 'Agri UI/UX View Foundation Mixin'

    @api.model
    def _apply_agri_term_mapping(self, arch):
        """ Base implementation returns arch as is. """
        return arch
