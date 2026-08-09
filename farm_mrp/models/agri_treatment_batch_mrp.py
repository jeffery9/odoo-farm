# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AgriTreatmentBatch(models.Model):
    _inherit = 'agri.treatment.batch'

    workcenter_id = fields.Many2one(
        'mrp.workcenter',
        string='Processing Workstation / Reactor Equipment (加工设备)',
        tracking=True
    )

    def action_start(self):
        self.ensure_one()
        if not self.workcenter_id:
            raise UserError(_("Please specify an active workstation/equipment first."))
        return super(AgriTreatmentBatch, self).action_start()
