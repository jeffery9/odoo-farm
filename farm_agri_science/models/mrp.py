# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def _hook_post_done(self):
        """[US-045-07] Biological Clock Sync after completion"""
        super()._hook_post_done()
        # If this is a scientific intervention, trigger biomass update
        if hasattr(self, 'physiology_profile_id') and self.physiology_profile_id:
            # Sync cumulative GDD to lot if applicable
            lot = getattr(self, 'lot_producing_id', False)
            if lot and hasattr(lot, 'cumulative_gdd'):
                lot.cumulative_gdd = self.cumulative_gdd
                self.message_post(body=_("SCIENTIFIC SYNC: Biological clock (GDD) transferred to output lot %s") % lot.name)
