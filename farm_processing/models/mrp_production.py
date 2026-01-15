# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    # --- Processing Specific Gate Logic ---
    def _get_isl_model(self):
        res = super(MrpProduction, self)._get_isl_model()
        if self.industry_type == 'food_processing':
            return 'farm.processing.production'
        return res

    def action_confirm(self):
        """ Processing-specific pre-confirmation checks. """
        for order in self:
            if order.industry_type == 'food_processing':
                # US-14-09: HACCP / Quality Gate Pre-check
                pass
        return super(MrpProduction, self).action_confirm()

    def button_mark_done(self):
        """ Processing-specific pre-done checks. """
        for order in self:
            if order.industry_type == 'food_processing':
                # Energy checks etc.
                pass
        return super(MrpProduction, self).button_mark_done()