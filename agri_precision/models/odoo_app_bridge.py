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

    # ---------------------------------------------------------
    # [ISL Hooks] Agricultural Vertical Implementation
    # ---------------------------------------------------------
    def _check_phase_readiness(self, phase):
        """ 
        [ISL Hook Override] 
        Adds IoT Environmental gating before starting an agricultural intervention.
        """
        super()._check_phase_readiness(phase)
        
        # Check IoT/Environmental status via agri.precision.mixin
        if self.iot_status == 'critical' and not self.is_process_locked:
            raise UserError(_(
                "ENVIRONMENTAL BLOCK: Cannot start Intervention '%s'. "
                "IoT sensors are reporting a CRITICAL environmental condition. "
                "Please apply corrective intervention first."
            ) % phase.name)
        return True

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

    # ---------------------------------------------------------
    # [ISL Hooks] VRA Dynamic Parameter Execution
    # ---------------------------------------------------------
    def action_trigger_vra_sync_from_iot(self, lat, lng):
        """
        Called when a tractor/drone reports a new GPS position.
        Triggers the calculation of dynamic setpoints (like spraying rate)
        based on the scientific VRA prescription map.
        """
        self.ensure_one()
        if self.state != 'progress':
            return False
            
        # Call the base VRA calculation logic in precision_production
        if hasattr(self.production_id, 'action_calculate_spatial_setpoint'):
            self.production_id.action_calculate_spatial_setpoint(lat, lng)
            
            # Log the geospatial sync
            self.production_id.message_post(
                body=_("VRA Sync: Adjusted active parameters for Intervention '%s' at [%s, %s]") % (self.name, lat, lng)
            )
        return True

    def action_update_yield_estimate_btn(self):
        return self.action_update_yield_estimate(0.0)

    def action_apply_agri_intervention_btn(self):
        return self.action_apply_agri_intervention(None)
