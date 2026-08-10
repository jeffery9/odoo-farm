from odoo import models, fields, api, _

class FarmBiologicalTwin(models.Model):
    _inherit = 'agri.biological.twin'

    def action_optimize_environment(self):
        """
        Override: L5 Autonomous Logic for Greenhouse Control.
        If GDD accumulation is too slow in a greenhouse, boost temperature.
        """
        # Run base implementation (if any hooks exist)
        super(FarmBiologicalTwin, self).action_optimize_environment()

        for rec in self:
            # Check if the twin is monitored in a greenhouse
            if not rec.location_id.is_greenhouse:
                continue
            
            # Simple GDD pacing logic
            days_elapsed = (fields.Date.today() - rec.start_date).days or 1
            if days_elapsed < 5: continue # Too early to judge
            
            actual_rate = rec.accumulated_gdd / days_elapsed
            # Assume 100 days total target for prototype simplicity (should come from stage data)
            target_rate = rec.target_gdd_harvest / 100.0 
            
            if actual_rate < target_rate * 0.9: # 10% behind schedule
                # We need to boost temp. 
                # Find temp control rule for this greenhouse
                rule = self.env['farm.greenhouse.control.rule'].search([
                    ('greenhouse_id', '=', rec.location_id.id),
                    ('parameter', '=', 'temp'),
                    ('is_ai_controlled', '=', True)
                ], limit=1)
                
                if rule:
                    # Boost by 2 degrees
                    new_low = rule.threshold_low + 2.0
                    new_high = rule.threshold_high + 2.0
                    
                    if rule.update_threshold_from_twin(new_low, new_high, _("GDD lagging behind target rate (%.2f < %.2f)") % (actual_rate, target_rate)):
                        rec.message_post(body=_("L5 AUTONOMOUS: Boosting greenhouse temperature to catch up GDD."))
                        
        return True
