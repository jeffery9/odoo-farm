# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class StockLot(models.Model):
    _inherit = 'stock.lot'

    def _get_isl_summary_parts(self):
        res = super(StockLot, self)._get_isl_summary_parts()
        isl = self.env['farm.lot.livestock'].search([('lot_id', '=', self.id)], limit=1)
        if isl:
            res.append(_("Husbandry: %s, Weight: %skg") % (isl.gender or 'N/A', isl.current_weight))
        return res
