# -*- coding: utf-8 -*-
from odoo import models, fields, api

class AgriScienceSyncWizard(models.TransientModel):
    _name = 'agri.science.sync.wizard'
    _description = 'Environmental Data Sync Wizard'

    intervention_id = fields.Many2one('mrp.production', string="Intervention", default=lambda self: self.env.context.get('active_id'))
    temp_max = fields.Float("Max Temperature", required=True)
    temp_min = fields.Float("Min Temperature", required=True)

    def action_sync(self):
        self.ensure_one()
        if self.intervention_id:
            self.intervention_id.record_daily_environmental_data(self.temp_max, self.temp_min)
        return {'type': 'ir.actions.act_window_close'}
