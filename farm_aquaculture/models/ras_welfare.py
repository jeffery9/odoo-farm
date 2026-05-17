from odoo import models, fields, api, _

class FarmRasProduction(models.Model):
    _inherit = 'farm.ras.production'
    
    # [US-SCENARIO-30] RAS Water Quality & Fish Welfare
    lss_status = fields.Selection([('normal', 'Normal'), ('emergency', 'Emergency Mode')], default='normal')
    ammonia_level = fields.Float("Ammonia Level (ppm)")
    
    @api.onchange('ammonia_level')
    def _onchange_ammonia_trigger_lss(self):
        if self.ammonia_level > 2.0:
            self.lss_status = 'emergency'
            self.message_post(body=_("EMERGENCY LSS ENGAGED: Ammonia spiked to %s ppm!") % self.ammonia_level)
            
            # Auto-calculate mortality impact
            # Assuming farm_financial_valuation is present, trigger devaluation
            if hasattr(self, 'asset_id') and self.asset_id:
                # 5% mortality drop
                self.asset_id.base_weight_kg *= 0.95
                if hasattr(self.asset_id, 'trigger_financial_revaluation'):
                    self.asset_id.trigger_financial_revaluation(reason="Ammonia Spike Mortality")

