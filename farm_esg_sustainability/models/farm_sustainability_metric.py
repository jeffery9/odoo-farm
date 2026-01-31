from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class FarmSustainabilityMetric(models.Model):
    """
    Farm-specific extension of the agricultural sustainability metric model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.sustainability.metric'
    _description = 'Sustainability Metric (Deprecated - Use agri.sustainability.metric)'
    _inherit = 'agri.sustainability.metric'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(
            "farm.sustainability.metric is deprecated. "
            "Please update your code to use agri.sustainability.metric instead."
        )
        return super()._register_hook()


class FarmSustainabilityMetricValue(models.Model):
    """
    Farm-specific extension of the agricultural sustainability metric value model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.sustainability.metric.value'
    _description = 'Sustainability Metric Value (Deprecated - Use agri.sustainability.metric.value)'
    _inherit = 'agri.sustainability.metric.value'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(
            "farm.sustainability.metric.value is deprecated. "
            "Please update your code to use agri.sustainability.metric.value instead."
        )
        return super()._register_hook()


class FarmSustainabilityMetricValueWizard(models.TransientModel):
    """
    Farm-specific extension of the agricultural sustainability metric value wizard.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.sustainability.metric.value.wizard'
    _description = 'Sustainability Metric Value Update Wizard (Deprecated - Use agri.sustainability.metric.value.wizard)'
    _inherit = 'agri.sustainability.metric.value.wizard'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(
            "farm.sustainability.metric.value.wizard is deprecated. "
            "Please update your code to use agri.sustainability.metric.value.wizard instead."
        )
        return super()._register_hook()