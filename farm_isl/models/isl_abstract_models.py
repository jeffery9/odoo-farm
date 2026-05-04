# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

# Abstract Base Models for ISL Architecture (US-084-01 through US-084-10)

class FarmManufacturingMixin(models.AbstractModel):
    """
    Farm-specific extension of the agricultural manufacturing ISL mixin.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.manufacturing.mixin'
    _description = 'Farm Manufacturing ISL Abstract Base Model (Deprecated - Use agri.manufacturing.mixin)'
    _inherit = ['agri.manufacturing.mixin']

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        _logger.warning(
            "farm.manufacturing.mixin is deprecated. "
            "Please update your code to use agri.manufacturing.mixin instead."
        )
        return super()._register_hook()


class FarmInventoryMixin(models.AbstractModel):
    """
    Farm-specific extension of the agricultural inventory ISL mixin.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.inventory.mixin'
    _description = 'Farm Inventory ISL Abstract Base Model (Deprecated - Use agri.inventory.mixin)'
    _inherit = ['agri.inventory.mixin']

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        _logger.warning(
            "farm.inventory.mixin is deprecated. "
            "Please update your code to use agri.inventory.mixin instead."
        )
        return super()._register_hook()


class FarmSalesPurchaseMixin(models.AbstractModel):
    """
    Farm-specific extension of the agricultural sales/purchase ISL mixin.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.sales.purchase.mixin'
    _description = 'Farm Sales/Purchase ISL Abstract Base Model (Deprecated - Use agri.sales.purchase.mixin)'
    _inherit = ['agri.sales.purchase.mixin']

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        _logger.warning(
            "farm.sales.purchase.mixin is deprecated. "
            "Please update your code to use agri.sales.purchase.mixin instead."
        )
        return super()._register_hook()


class FarmProductMixin(models.AbstractModel):
    """
    Farm-specific extension of the agricultural product ISL mixin.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.product.mixin'
    _description = 'Farm Product ISL Abstract Base Model (Deprecated - Use agri.product.mixin)'
    _inherit = ['agri.product.mixin']

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        _logger.warning(
            "farm.product.mixin is deprecated. "
            "Please update your code to use agri.product.mixin instead."
        )
        return super()._register_hook()


class FarmQualityMixin(models.AbstractModel):
    """
    Farm-specific extension of the agricultural quality control ISL mixin.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.quality.mixin'
    _description = 'Farm Quality Control ISL Abstract Base Model (Deprecated - Use agri.quality.mixin)'
    _inherit = ['agri.quality.mixin']

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        _logger.warning(
            "farm.quality.mixin is deprecated. "
            "Please update your code to use agri.quality.mixin instead."
        )
        return super()._register_hook()