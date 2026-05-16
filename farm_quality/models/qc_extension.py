from odoo import models, fields, api

class AgriQualityCheck(models.Model):
    _inherit = 'agri.quality.check'

    def action_trigger_recall(self):
        """ Creates a recall simulation from a failed QC """
        self.ensure_one()
        recall = self.env['farm.supply.recall'].create({
            'triggering_qc_id': self.id
        })
        return {
            'name': 'Emergency Recall',
            'view_mode': 'form',
            'res_model': 'farm.supply.recall',
            'res_id': recall.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
