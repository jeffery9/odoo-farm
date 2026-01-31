from odoo import models


class FarmAgriculturalBomMixin(models.Model):
    """
    Farm-specific extension of the agricultural BOM mixin.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.agricultural.bom.mixin'
    _description = 'Farm Agricultural BOM Shared Logic (Deprecated - Use agri.bom.mixin)'
    _inherit = 'agri.bom.mixin'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(
            "farm.agricultural.bom.mixin is deprecated. "
            "Please update your code to use agri.bom.mixin instead."
        )
        return super()._register_hook()


class FarmAgriculturalBomLineMixin(models.Model):
    """
    Farm-specific extension of the agricultural BOM line mixin.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.agricultural.bom.line.mixin'
    _description = 'Farm Agricultural BOM Line Shared Logic (Deprecated - Use agri.bom.line.mixin)'
    _inherit = 'agri.bom.line.mixin'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(
            "farm.agricultural.bom.line.mixin is deprecated. "
            "Please update your code to use agri.bom.line.mixin instead."
        )
        return super()._register_hook()