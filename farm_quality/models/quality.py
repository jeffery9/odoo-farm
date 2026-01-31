from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class FarmQualityPoint(models.Model):
    """
    Farm-specific extension of the agricultural quality point model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.quality.point'
    _description = 'Quality Control Point (Deprecated - Use agri.quality.point)'
    _inherit = 'agri.quality.point'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(
            "farm.quality.point is deprecated. "
            "Please update your code to use agri.quality.point instead."
        )
        return super()._register_hook()

class FarmQualityCheck(models.Model):
    """
    Farm-specific extension of the agricultural quality check model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.quality.check'
    _description = 'Quality Check (Deprecated - Use agri.quality.check)'
    _inherit = 'agri.quality.check'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(
            "farm.quality.check is deprecated. "
            "Please update your code to use agri.quality.check instead."
        )
        return super()._register_hook()

class FarmQualityAlert(models.Model):
    """
    Farm-specific extension of the agricultural quality alert model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.quality.alert'
    _description = 'Quality Alert (Deprecated - Use agri.quality.alert)'
    _inherit = 'agri.quality.alert'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(
            "farm.quality.alert is deprecated. "
            "Please update your code to use agri.quality.alert instead."
        )
        return super()._register_hook()

# Note: StockPicking and FarmLotQuality remain as is because they inherit from base Odoo models
class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        for picking in self:
            if picking.picking_type_code in ['outgoing', 'internal']:
                for move in picking.move_ids:
                    for lot in move.lot_ids:
                        if lot.quality_status == 'failed':
                            raise UserError(_("QUALITY ALERT: Lot %s has failed quality inspection.") % lot.name)
                        if lot.qc_release_state == 'locked':
                            raise UserError(_("QC LOCKED: Lot %s is pending release and cannot be moved.") % lot.name)
        return super().button_validate()

class FarmLotQuality(models.Model):
    _inherit = 'stock.lot'

    quality_status = fields.Selection([
        ('none', 'Not Tested'),
        ('passed', 'Passed'),
        ('failed', 'Failed')
    ], string="Quality Status", default='none', tracking=True)

    qc_release_state = fields.Selection([
        ('locked', 'Locked'),
        ('released', 'Released'),
    ], string="QC Release Status", default='locked', tracking=True)

    quality_check_ids = fields.One2many('agri.quality.check', 'lot_id', string="Quality Checks")

    def action_qc_release(self):
        self.ensure_one()
        self.write({'qc_release_state': 'released'})

    def action_lock(self):
        self.ensure_one()
        self.write({'qc_release_state': 'locked'})