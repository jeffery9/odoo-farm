# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

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

        # Create a precision intervention record if precision_production is available
        if 'precision.intervention' in self.env:
            self.env['precision.intervention'].create({
                'name': f"{intervention_type} Intervention",
                'production_id': self.id,
                'intervention_type': 'manual',  # or 'auto' if triggered by sensors
                'description': description,
                'status': 'open'
            })

        self.message_post(body=_("AGRICULTURAL INTERVENTION [%s]: %s") % (intervention_type, description))
        return True


class StockLot(models.Model):
    _name = 'stock.lot'
    _inherit = ['stock.lot', 'agri.precision.mixin']

    # [Grading] Each lot carries its binning result
    def action_set_grade(self, grade):
        self.write({'quality_grade': grade})

class PrecisionRecipePhase(models.Model):
    """
    Bridge between precision.recipe.phase and agri precision logic
    """
    _name = 'precision.recipe.phase'
    _inherit = ['precision.recipe.phase', 'agri.precision.mixin']

    def action_apply_phase_intervention(self, intervention_type, description):
        """
        Apply intervention to a specific phase based on environmental conditions
        """
        self.ensure_one()
        self.intervention_count += 1

        # Create a precision intervention record
        if 'precision.intervention' in self.env:
            self.env['precision.intervention'].create({
                'name': f"Phase {self.name} - {intervention_type} Intervention",
                'production_id': self.production_id.id,
                'phase_id': self.id,
                'intervention_type': intervention_type,
                'description': description,
                'status': 'open'
            })

        self.production_id.message_post(
            body=_("PHASE INTERVENTION [%s] on Phase %s: %s") % (intervention_type, self.name, description)
        )
        return True

    def action_calibrate_phase_due_to_environment(self, reason):
        """
        Calibrate phase parameters based on environmental sensor readings
        """
        self.ensure_one()
        self.last_metrology_date = fields.Datetime.now()

        # Log the environmental intervention
        self.action_apply_phase_intervention('environmental', f"Phase calibrated due to: {reason}")

    def action_update_yield_estimate_btn(self):
        return self.action_update_yield_estimate(0.0)

    def action_apply_agri_intervention_btn(self):
        return self.action_apply_agri_intervention(None)
