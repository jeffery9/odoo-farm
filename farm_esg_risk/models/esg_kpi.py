from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class ESGKPI(models.Model):
    """
    Farm-specific extension of the agricultural ESG KPI model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.esg.kpi'
    _description = 'ESG KPI (Deprecated - Use agri.esg.kpi)'
    _inherit = 'agri.esg.kpi'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(
            "farm.esg.kpi is deprecated. "
            "Please update your code to use agri.esg.kpi instead."
        )
        return super()._register_hook()