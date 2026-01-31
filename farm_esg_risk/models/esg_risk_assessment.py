from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class ESGRiskAssessment(models.Model):
    """
    Farm-specific extension of the agricultural ESG risk assessment model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.esg.risk.assessment'
    _description = 'ESG Risk Assessment (Deprecated - Use agri.esg.risk.assessment)'
    _inherit = 'agri.esg.risk.assessment'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(
            "farm.esg.risk.assessment is deprecated. "
            "Please update your code to use agri.esg.risk.assessment instead."
        )
        return super()._register_hook()