# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class StockLot(models.Model):
    _inherit = 'stock.lot'

    def _get_isl_summary_parts(self):
        res = super(StockLot, self)._get_isl_summary_parts()
        isl = self.env['farm.crop.lot'].search([('lot_id', '=', self.id)], limit=1)
        if isl:
            # Note: farm.crop.lot uses plot_origin_id instead of plot_id
            res.append(_("Field: %s") % (isl.plot_origin_id.name or 'Unknown'))
        return res
