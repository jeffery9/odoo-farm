from odoo import models, fields, api, _

class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    # 能耗核算基础 [US-14-04]
    energy_type = fields.Selection([
        ('electricity', 'Electricity'),
        ('water', 'Water'),
        ('gas', 'Gas'),
    ], string="Primary Energy Type")
    energy_cost_per_hour = fields.Float("Energy Cost per Hour")

class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    # 实际工序能耗记录 [US-14-04]
    actual_energy_consumption = fields.Float("Actual Energy Consumption")
    process_parameters = fields.Text("Process Parameters (e.g. Temperature, Pressure)")

    # US-14-08: 单工序物料平衡与损耗
    qty_produced_workorder = fields.Float("Produced Qty (Workorder)", default=0.0,
                                         help="Actual quantity produced in this workorder.")
    qty_scrapped_workorder = fields.Float("Scrapped Qty (Workorder)", default=0.0,
                                         help="Actual quantity scrapped in this workorder.")
    qty_input_workorder = fields.Float("Input Qty (Workorder)", default=0.0,
                                      help="Actual quantity input to this workorder.")
    loss_rate_workorder = fields.Float("Loss Rate (Workorder) (%)", compute='_compute_loss_rate_workorder', store=True,
                                      help="Calculated loss rate for this workorder.")

    @api.depends('qty_produced_workorder', 'qty_scrapped_workorder', 'qty_input_workorder')
    def _compute_loss_rate_workorder(self):
        for wo in self:
            if wo.qty_input_workorder > 0:
                wo.loss_rate_workorder = (wo.qty_scrapped_workorder / wo.qty_input_workorder) * 100.0
            else:
                wo.loss_rate_workorder = 0.0

    def _check_workorder_balance(self):
        self.ensure_one()
        if self.qty_input_workorder <= 0:
            return True # No input, no balance check needed

        tolerance = 0.01 # 1% tolerance for workorder balance
        total_output = self.qty_produced_workorder + self.qty_scrapped_workorder
        if abs(self.qty_input_workorder - total_output) / self.qty_input_workorder > tolerance:
            from odoo.exceptions import UserError
            raise UserError(_("Workorder Material Balance Error: Input quantity (%s) does not match produced (%s) + scrapped (%s) within allowed tolerance (%s%%).") % (
                self.qty_input_workorder, self.qty_produced_workorder, self.qty_scrapped_workorder, tolerance * 100
            ))
        return True

    def button_finish(self):
        self.ensure_one()
        self._check_workorder_balance()
        # Update parent MO's scrap_qty with this workorder's scrap_qty
        if self.production_id:
            self.production_id.scrap_qty += self.qty_scrapped_workorder

        return super(MrpWorkorder, self).button_finish()
