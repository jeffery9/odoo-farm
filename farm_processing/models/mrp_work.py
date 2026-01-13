from odoo import models, fields, api, _

class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    # 能耗核算基础 [US-14-04]
    energy_type = fields.Selection([
        ('electricity', 'Electricity (电)'),
        ('water', 'Water (水)'),
        ('gas', 'Gas (气/煤)'),
    ], string="Primary Energy Type")
    energy_cost_per_hour = fields.Float("Energy Cost per Hour")

class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    # 实际工序能耗记录 [US-14-04]
    actual_energy_consumption = fields.Float("Actual Energy Consumption")
    process_parameters = fields.Text("Process Parameters (e.g. Temperature, Pressure)")
