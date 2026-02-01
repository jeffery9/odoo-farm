# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def action_verify_flower_quality(self):
        """ [ISL Bridge] Check Vase-life before confirming sale. """
        for line in self:
            # If picking is linked or lot is selected
            for move in line.move_ids:
                for lot in move.lot_ids:
                    flower_lot = self.env['farm.lot.flower'].search([('lot_id', '=', lot.id)], limit=1)
                    if flower_lot and flower_lot.predicted_vase_life < 3:
                        raise UserError(_("QUALITY BLOCK: Flower Lot %s has insufficient vase-life (%s days) for sale.") % 
                                       (lot.name, flower_lot.predicted_vase_life))
        return True

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        """ Enforce quality check on confirmation. """
        for order in self:
            order.order_line.action_verify_flower_quality()
        return super(SaleOrder, self).action_confirm()

# (Rest of flower_isl.py remains same, ensured via write_file below)
