from odoo import models


class FarmAgriculturalInterventionMixin(models.Model):
    """
    Farm-specific extension of the agricultural intervention mixin.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.agricultural.intervention.mixin'
    _description = 'Farm Agricultural Intervention Shared Logic (Deprecated - Use agri.intervention.mixin)'
    _inherit = 'agri.intervention.mixin'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(
            "farm.agricultural.intervention.mixin is deprecated. "
            "Please update your code to use agri.intervention.mixin instead."
        )
        return super()._register_hook()