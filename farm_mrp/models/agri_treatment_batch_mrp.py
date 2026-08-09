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

    operation_id = fields.Many2one(
        'mrp.routing.workcenter',
        string='Process Operation / 工艺工序阶段',
        tracking=True,
        help="The specific process routing operation step this treatment batch executes."
    )

    @api.onchange('operation_id')
    def _onchange_operation_id(self):
        """ Dynamically default workcenter_id based on selected routing operation """
        if self.operation_id and self.operation_id.workcenter_id:
            self.workcenter_id = self.operation_id.workcenter_id.id

    def action_start(self):
        self.ensure_one()
        if not self.workcenter_id:
            raise UserError(_("Please specify an active workstation/equipment first."))
        res = super(AgriTreatmentBatch, self).action_start()
        # Synchronize current process phase onto linked carriers upon start
        if self.operation_id:
            self.carrier_ids.write({'current_phase_id': self.operation_id.id})
        return res

    def action_complete(self):
        self.ensure_one()
        res = super(AgriTreatmentBatch, self).action_complete()
        # Clear active process phase on carriers when batch execution completes
        self.carrier_ids.write({'current_phase_id': False})
        return res
