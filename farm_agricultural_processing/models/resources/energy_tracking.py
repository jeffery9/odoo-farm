# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class FarmWorkcenterExtension(models.Model):    _inherit = 'farm.industry.workcenter'

    # 能耗核算基础 [US-037-04]
    energy_type = fields.Selection([
        ('electricity', 'Electricity'),
        ('water', 'Water'),
        ('gas', 'Gas'),
    ], string="Primary Energy Type")
    energy_cost_per_hour = fields.Float("Energy Cost per Hour")


class FarmWorkorderEnergyExtension(models.Model):
    _inherit = 'mrp.workorder'  # Note: no specific ISL model for workorders yet in farm_processing

    # 实际工序能耗记录 [US-037-04]
    actual_energy_consumption = fields.Float("Actual Energy Consumption")
    process_parameters = fields.Text("Process Parameters (e.g. Temperature, Pressure)")

    def action_record_energy_consumption(self):
        """Record energy consumption for the work order"""
        # This would integrate with IoT devices or manual entry
        pass