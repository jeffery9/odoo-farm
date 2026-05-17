from odoo import models, fields, api, _
from odoo.exceptions import UserError

class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    # [US-SCENARIO-31] Micro-Climate Gating for Greenhouse
    current_greenhouse_humidity = fields.Float("Live Humidity (%)")
    
    def action_confirm(self):
        # We intercept action_confirm for spraying in greenhouse
        for mo in self:
            if hasattr(mo, 'intervention_type') and mo.intervention_type == 'protection' and mo.land_parcel_id:
                # If location is a greenhouse
                if mo.land_parcel_id.location_type == 'greenhouse':
                    # Check humidity
                    if mo.current_greenhouse_humidity > 85.0:
                        raise UserError(_("CLIMATE LOCK: Current greenhouse humidity is %s%%. Conditions Unsuitable for Spraying (Max 85%%).") % mo.current_greenhouse_humidity)
        return super().action_confirm()

