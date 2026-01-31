# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

# ISL Model Redirection Mechanism (US-54-11)

class ISLModelRedirector(models.AbstractModel):
    """
    Farm-specific extension of the agricultural ISL model redirection utility.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'isl.model.redirector'
    _description = 'ISL Model Redirection Utility (Deprecated - Use agri.isl.model.redirector)'
    _inherit = ['agri.isl.model.redirector']

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        _logger.warning(
            "isl.model.redirector is deprecated. "
            "Please update your code to use agri.isl.model.redirector instead."
        )
        return super()._register_hook()


# Industry-Specific Extension Mechanism (US-54-12)

class ISLIndustryExtension(models.Model):
    """
    Farm-specific extension of the agricultural ISL extension model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.isl.extension'
    _description = 'Farm ISL Extension (Deprecated - Use agri.isl.extension)'
    _inherit = ['agri.isl.extension']

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        _logger.warning(
            "farm.isl.extension is deprecated. "
            "Please update your code to use agri.isl.extension instead."
        )
        return super()._register_hook()