from odoo import models, fields, api, _
import logging
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)


class SustainabilityDashboard(models.Model):
    """
    Farm-specific extension of the agricultural sustainability dashboard model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.sustainability.dashboard'
    _description = 'Sustainability Dashboard (Deprecated - Use agri.sustainability.dashboard)'
    _inherit = 'agri.sustainability.dashboard'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(
            "farm.sustainability.dashboard is deprecated. "
            "Please update your code to use agri.sustainability.dashboard instead."
        )
        return super()._register_hook()


class SustainabilityReport(models.Model):
    """
    Farm-specific extension of the agricultural sustainability report model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.sustainability.report'
    _description = 'Sustainability Report (Deprecated - Use agri.sustainability.report)'
    _inherit = 'agri.sustainability.report'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(
            "farm.sustainability.report is deprecated. "
            "Please update your code to use agri.sustainability.report instead."
        )
        return super()._register_hook()