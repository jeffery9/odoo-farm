from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import drop_view_if_exists
import logging

_logger = logging.getLogger(__name__)


class CircularFlow(models.Model):
    """
    Farm-specific extension of the agricultural sustainability circular flow model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.sustainability.circular.flow'
    _description = 'Farm Circular Flow (Deprecated - Use agri.sustainability.circular.flow)'
    _inherit = 'agri.sustainability.circular.flow'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(
            "farm.sustainability.circular.flow is deprecated. "
            "Please update your code to use agri.sustainability.circular.flow instead."
        )
        return super()._register_hook()


class CircularFlowAnalysis(models.Model):
    """
    Farm-specific extension of the agricultural sustainability circular flow analysis model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.sustainability.circular.flow.analysis'
    _description = 'Farm Circular Flow Analysis (Deprecated - Use agri.sustainability.circular.flow.analysis)'
    _inherit = 'agri.sustainability.circular.flow.analysis'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(
            "farm.sustainability.circular.flow.analysis is deprecated. "
            "Please update your code to use agri.sustainability.circular.flow.analysis instead."
        )
        return super()._register_hook()