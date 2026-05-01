from odoo.tests.common import TransactionCase
import logging
_logger = logging.getLogger(__name__)

class TestRegistry(TransactionCase):
    def test_00_check_models(self):
        _logger.info("CHECKING MODELS IN REGISTRY")
        for model in ['agri.quality.point', 'agri.geospatial.grid.cell']:
            if model in self.env:
                _logger.info("Model %s is IN registry", model)
            else:
                _logger.info("Model %s is NOT in registry", model)
