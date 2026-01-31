# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import logging

_logger = logging.getLogger(__name__)

class FarmTrainingSkill(models.Model):
    """
    Farm-specific extension of the agricultural training skill model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.training.skill'
    _description = 'Farm Training Skill (Deprecated - Use agri.training.skill)'
    _inherit = 'agri.training.skill'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        _logger.warning(
            "farm.training.skill is deprecated. "
            "Please update your code to use agri.training.skill instead."
        )
        return super()._register_hook()

class FarmTrainingCertification(models.Model):
    """
    Farm-specific extension of the agricultural training certification model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.training.certification'
    _description = 'Farm Training Certification (Deprecated - Use agri.training.certification)'
    _inherit = 'agri.training.certification'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        _logger.warning(
            "farm.training.certification is deprecated. "
            "Please update your code to use agri.training.certification instead."
        )
        return super()._register_hook()

class FarmTrainingTrainingRecord(models.Model):
    """
    Farm-specific extension of the agricultural training record model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.training.training_record'
    _description = 'Farm Training Record (Deprecated - Use agri.training.training_record)'
    _inherit = 'agri.training.training_record'
    _rec_name = 'display_name'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        _logger.warning(
            "farm.training.training_record is deprecated. "
            "Please update your code to use agri.training.training_record instead."
        )
        return super()._register_hook()

