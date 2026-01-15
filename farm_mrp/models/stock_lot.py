# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class StockLot(models.Model):
    _inherit = 'stock.lot'

    isl_summary_info = fields.Char("ISL Contextual Info", compute='_compute_isl_summary_info')

    def _compute_isl_summary_info(self):
        """ Decoupled hook for ISL summary info. """
        for lot in self:
            info_parts = lot._get_isl_summary_parts()
            lot.isl_summary_info = " | ".join(info_parts) if info_parts else ""

    def _get_isl_summary_parts(self):
        """ 
        Specialized modules should override this and return a list of strings.
        Example: return ["Breed: Angus", "Weight: 500kg"]
        """
        return []
