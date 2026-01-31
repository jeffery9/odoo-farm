from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class FarmEvidence(models.Model):
    """
    Farm-specific extension of the agricultural evidence model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.evidence'
    _description = 'Field Evidence (Deprecated - Use agri.evidence)'
    _inherit = 'agri.evidence'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(
            "farm.evidence is deprecated. "
            "Please update your code to use agri.evidence instead."
        )
        return super()._register_hook()