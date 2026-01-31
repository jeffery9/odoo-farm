from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)

class FarmManureBatch(models.Model):
    """
    Farm-specific extension of the agricultural manure batch model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.manure.batch'
    _description = 'Manure Batch Record (Deprecated - Use agri.manure.batch)'
    _inherit = 'agri.manure.batch'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(
            "farm.manure.batch is deprecated. "
            "Please update your code to use agri.manure.batch instead."
        )
        return super()._register_hook()

class FarmManureLedger(models.Model):
    """
    Farm-specific extension of the agricultural manure ledger model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.manure.ledger'
    _description = 'Monthly Manure Resource Utilization Ledger (Deprecated - Use agri.manure.ledger)'
    _inherit = 'agri.manure.ledger'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(
            "farm.manure.ledger is deprecated. "
            "Please update your code to use agri.manure.ledger instead."
        )
        return super()._register_hook()