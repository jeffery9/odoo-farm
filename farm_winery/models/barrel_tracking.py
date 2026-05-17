from odoo import models, fields, api, _

class FarmWineryProduction(models.Model):
    _inherit = 'farm.winery.production'
    
    # [US-SCENARIO-32] Barrel Aging & Vintage Lot Identity
    barrel_id = fields.Many2one('maintenance.equipment', string="Oak Barrel")
    vintage_year = fields.Char("Vintage Year")
    sensory_score = fields.Float("AI Sensory Score (0-100)")
    
    def action_transfer_to_barrel(self, barrel):
        self.ensure_one()
        self.barrel_id = barrel.id
        self.message_post(body=_("Wine transferred to barrel %s. Terroir DNA preserved.") % barrel.name)
        
    def action_ai_blending_recommendation(self):
        """ Recommends Grand Vin vs Secondary Label based on sensory score """
        for mo in self:
            if mo.sensory_score >= 95:
                recommendation = "Grand Vin (正牌酒)"
            else:
                recommendation = "Secondary Label (副牌酒)"
            mo.message_post(body=_("AI Blending Recommendation: %s based on score %s.") % (recommendation, mo.sensory_score))

