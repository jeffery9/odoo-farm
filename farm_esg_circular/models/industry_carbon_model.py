from odoo import models, fields, api
from odoo.exceptions import ValidationError

class IndustryCarbonModel(models.Model):
    """
    Farm-specific extension of the agricultural sustainability carbon model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.sustainability.industry.carbon.model'
    _description = 'Industry Specific Carbon Model (Deprecated - Use agri.sustainability.carbon.model)'
    _inherit = 'agri.sustainability.carbon.model'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(
            "farm.sustainability.industry.carbon.model is deprecated. "
            "Please update your code to use agri.sustainability.carbon.model instead."
        )
        return super()._register_hook()