from odoo import models


class FarmPestDisease(models.Model):
    """
    Farm-specific extension of the agricultural pest and disease model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.pest.disease'
    _description = 'Pest & Disease Database (Deprecated - Use agri.pest.disease)'
    _inherit = 'agri.pest.disease'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(
            "farm.pest.disease is deprecated. "
            "Please update your code to use agri.pest.disease instead."
        )
        return super()._register_hook()
