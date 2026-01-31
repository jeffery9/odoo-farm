from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class FarmAllergen(models.Model):
    """
    Farm-specific extension of the agricultural allergen model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.allergen'
    _description = 'Food Allergen (Deprecated - Use agri.allergen)'
    _inherit = 'agri.allergen'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(
            "farm.allergen is deprecated. "
            "Please update your code to use agri.allergen instead."
        )
        return super()._register_hook()
