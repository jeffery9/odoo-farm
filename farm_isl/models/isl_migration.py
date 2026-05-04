# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

# Data Migration & Compatibility (US-084-14)

class ISLMigrationUtility(models.TransientModel):
    """
    Farm-specific extension of the agricultural ISL migration utility.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'isl.migration.utility'
    _description = 'ISL Data Migration Utility (Deprecated - Use agri.isl.migration.utility)'
    _inherit = ['agri.isl.migration.utility']

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        _logger.warning(
            "isl.migration.utility is deprecated. "
            "Please update your code to use agri.isl.migration.utility instead."
        )
        return super()._register_hook()