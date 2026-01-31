from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class FarmQualitySample(models.Model):
    """
    Farm-specific extension of the agricultural quality sample model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.quality.sample'
    _description = 'Quality Sample (Deprecated - Use agri.quality.sample)'
    _inherit = 'agri.quality.sample'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(
            "farm.quality.sample is deprecated. "
            "Please update your code to use agri.quality.sample instead."
        )
        return super()._register_hook()
