# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class FarmAgriBomMixin(models.AbstractModel):
    """
    Farm-specific extension of the agricultural BOM mixin.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.agri.bom.mixin'
    _description = 'Farm Agricultural BOM Shared Logic (Deprecated - Use agri.bom.mixin)'
    _inherit = 'agri.bom.mixin'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        _logger.warning(
            "farm.agri.bom.mixin is deprecated. "
            "Please update your code to use agri.bom.mixin instead."
        )
        return super()._register_hook()

class FarmAgriProductionMixin(models.AbstractModel):
    """
    Farm-specific extension of the agricultural production mixin.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.agri.production.mixin'
    _description = 'Farm Agricultural Production Shared Logic (Deprecated - Use agri.production.mixin)'
    _inherit = 'agri.production.mixin'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        _logger.warning(
            "farm.agri.production.mixin is deprecated. "
            "Please update your code to use agri.production.mixin instead."
        )
        return super()._register_hook()