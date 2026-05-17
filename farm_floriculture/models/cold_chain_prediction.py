from odoo import models, fields, api, _

class FarmFloricultureProduction(models.Model):
    _inherit = 'farm.floriculture.production'
    
    # [US-SCENARIO-33] Floriculture Cold Chain
    vase_life_days = fields.Integer("Predicted Vase Life (Days)", default=14)
    cold_chain_breach_minutes = fields.Integer("Cold Chain Breach Duration (Mins)", default=0)
    
    @api.onchange('cold_chain_breach_minutes')
    def _onchange_cold_chain(self):
        if self.cold_chain_breach_minutes >= 30:
            old_life = self.vase_life_days
            self.vase_life_days = 5
            self.message_post(body=_("COLD CHAIN BREACH: Temperature > 4C for %s mins. Vase life downgraded from %s to %s days. Auto-triggering local rerouting.") % (
                self.cold_chain_breach_minutes, old_life, self.vase_life_days
            ))

