from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class ESGComplianceMonitoring(models.Model):
    """
    Farm-specific extension of the agricultural ESG compliance monitoring model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.esg.compliance.monitoring'
    _description = 'ESG Compliance Monitoring (Deprecated - Use agri.esg.compliance.monitoring)'
    _inherit = 'agri.esg.compliance.monitoring'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(
            "farm.esg.compliance.monitoring is deprecated. "
            "Please update your code to use agri.esg.compliance.monitoring instead."
        )
        return super()._register_hook()