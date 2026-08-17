from odoo import models, fields, api, _
from datetime import timedelta

class FarmCSAPlan(models.Model):
    _inherit = 'farm.csa.plan'

    def action_aggregate_jit_harvest(self):
        """
        [US-CSA-02] Demand-Driven JIT Harvest
        Aggregates all active subscriptions needing delivery within the next 3 days
        and dispatches a single consolidated harvesting intervention.
        """
        today = fields.Date.today()
        target_date = today + timedelta(days=3)
        
        subs = self.env['farm.csa.subscription'].search([
            ('plan_id', '=', self.id),
            ('state', '=', 'active'),
            ('sub_type', '=', 'bag'),
            ('next_delivery_date', '<=', target_date)
        ])
        
        if not subs:
            return False
            
        total_qty = len(subs) * 1.0 # Assuming 1 unit per sub for simplicity
        
        # Dispatch Harvesting Intervention
        intervention = self.env['mrp.production'].create({
            'product_id': self.product_id.id,
            'product_qty': total_qty,
            'intervention_type': 'harvesting',
            'origin': f"JIT CSA Aggregation: {self.name} ({len(subs)} orders)",
        })
        
        intervention.message_post(body=_("JIT Harvest Dispatched: %s units of %s needed for %s upcoming deliveries. Intervention: %s") % (
            total_qty, self.product_id.name, len(subs), intervention.name
        ))
        
        return intervention
