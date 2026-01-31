# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)

class FarmHealthSchedule(models.Model):
    """
    Farm-specific extension of the agricultural health schedule model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.health.schedule'
    _description = 'Livestock Vaccination & Health Schedule (Deprecated - Use agri.health.schedule)'
    _inherit = 'agri.health.schedule'

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        _logger.warning(
            "farm.health.schedule is deprecated. "
            "Please update your code to use agri.health.schedule instead."
        )
        return super()._register_hook()

class StockLotHealth(models.Model):
    """
    Farm-specific extension of the stock lot health model.
    This ensures backward compatibility while using the new agri.* namespace.
    """
    _name = 'farm.stock.lot.health'
    _description = 'Stock Lot Health (Deprecated - Use stock.lot with agri.health.schedule)'
    _inherit = 'stock.lot'

    # Track health activities specifically
    health_activity_ids = fields.One2many('mail.activity', 'res_id',
                                         domain=[('res_model', '=', 'stock.lot')],
                                         string="Planned Health Actions")

    @api.onchange('life_stage')
    def _onchange_life_stage_health(self):
        """ US-03-03: Auto-schedule health activities when life stage changes. """
        for lot in self:
            if lot.lot_purpose == 'biological_asset' and lot.life_stage:
                schedules = self.env['agri.health.schedule'].search([
                    ('product_tmpl_id', '=', lot.product_id.product_tmpl_id.id),
                    ('target_life_stage', '=', lot.life_stage)
                ])
                for sch in schedules:
                    lot.activity_schedule(
                        activity_type_id=self.env.ref('mail.mail_activity_data_todo').id,
                        summary=sch.activity_summary,
                        note=sch.activity_note,
                        date_deadline=fields.Date.today() + timedelta(days=sch.days_offset),
                    )

    def _register_hook(self):
        """Display deprecation warning when module is installed."""
        _logger.warning(
            "farm.stock.lot.health is deprecated. "
            "Please update your code to use stock.lot with agri.health.schedule instead."
        )
        return super()._register_hook()
