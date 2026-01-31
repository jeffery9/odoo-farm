from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class ESGRedLineConfig(models.Model):
    """
    Farm-specific extension of the agricultural ESG red line config model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.esg.red.line.config'
    _description = 'ESG Red Line Configuration (Deprecated - Use agri.esg.red.line.config)'
    _inherit = 'agri.esg.red.line.config'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        _logger.warning(
            "farm.esg.red.line.config is deprecated. "
            "Please update your code to use agri.esg.red.line.config instead."
        )
        return super()._register_hook()


class ESGRedLineMonitoring(models.Model):
    """
    Farm-specific extension of the agricultural ESG red line monitoring model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.esg.red.line.monitoring'
    _description = 'ESG Red Line Monitoring (Deprecated - Use agri.esg.red.line.monitoring)'
    _inherit = 'agri.esg.red.line.monitoring'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        _logger.warning(
            "farm.esg.red.line.monitoring is deprecated. "
            "Please update your code to use agri.esg.red.line.monitoring instead."
        )
        return super()._register_hook()


class StockLot(models.Model):
    """Extend stock.lot to add ESG compliance checking - Farm-specific implementation"""
    _inherit = 'stock.lot'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        _logger.warning(
            "ESG compliance functionality for stock.lot in farm.* namespace is deprecated. "
            "ESG functionality is now available directly in the agri.* namespace through agri.esg.red.line.monitoring."
        )
        return super()._register_hook()