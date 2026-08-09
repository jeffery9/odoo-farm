# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class StockMatterTracking(models.Model):
    _inherit = 'stock.matter.tracking'

    current_phase_id = fields.Many2one(
        'mrp.routing.workcenter',
        string='Current Process Phase',
        index=True,
        tracking=True,
        help="The manufacturing/routing step currently being executed on this material."
    )

    is_vessel_locked = fields.Boolean(
        string='Is Vessel Locked',
        default=False,
        tracking=True,
        help="Indicates whether this vessel is physically locked to a workcenter or equipment."
    )

    def action_lock_vessel(self):
        self.ensure_one()
        self.write({'is_vessel_locked': True})
        return True

    def action_unlock_vessel(self):
        self.ensure_one()
        self.write({'is_vessel_locked': False})
        return True


class StockMatterTrackingSnapshot(models.Model):
    _inherit = 'stock.matter.tracking.snapshot'

    phase_id = fields.Many2one(
        'mrp.routing.workcenter',
        string='Process Phase'
    )


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    current_phase_id = fields.Many2one(
        'mrp.routing.workcenter',
        string='Current Process Phase',
        index=True,
        help="The specific process or manufacturing phase this matter (quant) currently belongs to."
    )
