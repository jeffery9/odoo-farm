# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class StockLot(models.Model):
    _inherit = 'stock.lot'

    def _get_isl_summary_parts(self):
        res = super(StockLot, self)._get_isl_summary_parts()
        isl = self.env['farm.lot.aquaculture'].search([('lot_id', '=', self.id)], limit=1)
        if isl:
            res.append(_("Aqua: %s, Count: %s") % (isl.current_count, isl.water_volume_m3))
        return res
