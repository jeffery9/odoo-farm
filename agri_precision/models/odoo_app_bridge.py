# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class MrpProduction(models.Model):
    _name = 'mrp.production'
    _inherit = ['mrp.production', 'agri.precision.mixin']

    # Transform Order into Intervention
    display_name_agri = fields.Char("Intervention Label", compute='_compute_agri_name')

    def _compute_agri_name(self):
        for rec in self:
            rec.display_name_agri = f"Intervention: {rec.name}"

    def action_update_yield_estimate(self, new_qty):
        """ [Uncertainty] Mid-process yield calibration. """
        self.ensure_one()
        self.product_qty = new_qty
        self.last_metrology_date = fields.Datetime.now()
        self.message_post(body=_("YIELD CALIBRATION: New expected quantity set to %s.") % new_qty)

    def action_apply_agri_intervention(self, intervention_type, description):
        """
        Apply agricultural intervention based on sensor readings or environmental conditions
        """
        self.ensure_one()
        self.intervention_count += 1
        self.message_post(body=_("AGRICULTURAL INTERVENTION [%s]: %s") % (intervention_type, description))
        return True

    # ---------------------------------------------------------
    # [ISL Hooks] Agricultural Vertical Implementation
    # ---------------------------------------------------------
    def _get_quality_weights(self):
        """ 
        [ISL Hook Override] 
        Defines agricultural grading weights (e.g., Premium=100, Standard=70, Fail=0)
        """
        return {'premium': 100, 'standard': 70, 'fail': 0}


class StockLot(models.Model):
    _inherit = 'stock.lot'

    # [Grading] Each lot carries its binning result
    def action_set_grade(self, grade):
        self.write({'quality_grade': grade})
