from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class FarmAgriculturalCampaignMixin(models.AbstractModel):
    """
    Farm-specific extension of the agricultural campaign mixin.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.agricultural.campaign.mixin'
    _description = 'Farm Agricultural Campaign Shared Logic (Deprecated - Use agri.agricultural.campaign.mixin)'
    _inherit = 'agri.agricultural.campaign.mixin'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        _logger.warning(
            "farm.agricultural.campaign.mixin is deprecated. "
            "Please update your code to use agri.agricultural.campaign.mixin instead."
        )
        return super()._register_hook()