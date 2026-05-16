from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class SupplyChainNodeMixin(models.AbstractModel):
    """
    Farm-specific extension of the agricultural supply chain node mixin.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'supply.chain.node.mixin'
    _description = 'Supply Chain Node Mixin (Deprecated - Use agri.supply.chain.node.mixin)'
    _inherit = 'agri.supply.chain.node.mixin'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        _logger.warning(
            "supply.chain.node.mixin is deprecated. "
            "Please update your code to use agri.supply.chain.node.mixin instead."
        )
        return super()._register_hook()