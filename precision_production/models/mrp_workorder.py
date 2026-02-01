# -*- coding: utf-8 -*-
from odoo import models, fields

class MrpWorkorder(models.Model):
    _inherit = ['mrp.workorder', 'precision.production.mixin']
    production_drive_type = fields.Selection(related='production_id.production_drive_type')
    is_intervention_required = fields.Boolean("Intervention Needed", compute='_compute_intervention_needed')

    def _compute_intervention_needed(self):
        for wo in self:
            wo.is_intervention_required = (wo.production_drive_type == 'parameter' and 
                                          wo.production_id.skill_execution_status == 'failed')