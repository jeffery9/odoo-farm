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

    bom_id = fields.Many2one(
        'mrp.bom',
        string='Process Recipe / 生产工艺配方',
        tracking=True,
        help="The specific process recipe or formula executed by this treatment batch."
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

        # GxP Recipe & Matter Compatibility Validation
        if self.bom_id:
            allowed_products = self.env['product.product']
            # Include main target output product
            if self.bom_id.product_id:
                allowed_products |= self.bom_id.product_id
            elif self.bom_id.product_tmpl_id:
                allowed_products |= self.bom_id.product_tmpl_id.product_variant_ids
            # Include input ingredients/components
            allowed_products |= self.bom_id.bom_line_ids.mapped('product_id')

            for carrier in self.carrier_ids:
                carrier_products = carrier.quant_ids.mapped('product_id')
                for prod in carrier_products:
                    if prod not in allowed_products:
                        raise UserError(_(
                            "GxP Recipe Compatibility Violation: Carrier %s contains product '%s' "
                            "which is not part of the selected process recipe '%s' (inputs or output)."
                        ) % (carrier.name, prod.display_name, self.bom_id.display_name))

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
