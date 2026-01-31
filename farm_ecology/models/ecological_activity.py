from odoo import models, fields, api

class FarmEcologicalActivity(models.Model):
    """
    Farm-specific extension of the agricultural ecological activity model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.ecological.activity'
    _description = 'Ecological Maintenance Activity (Deprecated - Use agri.ecological.activity)'
    _inherit = 'agri.ecological.activity'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(
            "farm.ecological.activity is deprecated. "
            "Please update your code to use agri.ecological.activity instead."
        )
        return super()._register_hook()