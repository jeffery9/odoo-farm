from odoo import models

class MrpProductionExtension(models.Model):
    _name = 'mrp.production'
    _inherit = 'mrp.production'

    def action_update_yield_estimate_btn(self):
        return self.action_update_yield_estimate(0.0)

    def action_apply_agri_intervention_btn(self):
        return self.action_apply_agri_intervention(None)
