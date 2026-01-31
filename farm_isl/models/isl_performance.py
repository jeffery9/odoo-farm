# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

# Performance Optimization & Caching (US-54-13)

class ISLOptimizationMixin(models.AbstractModel):
    """
    Farm-specific extension of the agricultural ISL optimization mixin.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'isl.optimization.mixin'
    _description = 'ISL Optimization Mixin (Deprecated - Use agri.isl.optimization.mixin)'
    _inherit = ['agri.isl.optimization.mixin']

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        _logger.warning(
            "isl.optimization.mixin is deprecated. "
            "Please update your code to use agri.isl.optimization.mixin instead."
        )
        return super()._register_hook()