from odoo import models, fields, api

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    # 加工能耗记录 [US-62]
    energy_meter_start = fields.Float("Energy Meter Start", help="Meter reading before processing")
    energy_meter_end = fields.Float("Energy Meter End", help="Meter reading after processing")
    energy_consumption = fields.Float("Energy Consumption", compute='_compute_energy_consumption', store=True)
    
    # 质量控制扩展
    moisture_content = fields.Float("Moisture Content (%)", help="Final moisture content for dried products")
    process_temperature = fields.Float("Process Temperature (℃)")

    @api.depends('energy_meter_start', 'energy_meter_end')
    def _compute_energy_consumption(self):
        for mo in self:
            if mo.energy_meter_end > mo.energy_meter_start:
                mo.energy_consumption = mo.energy_meter_end - mo.energy_meter_start
            else:
                mo.energy_consumption = 0.0

class StockLot(models.Model):
    _inherit = 'stock.lot'

    # 批次溯源：指向原材料批次
    parent_lot_id = fields.Many2one('stock.lot', string="Parent Lot/Origin", help="Trace back to the raw material lot")
    child_lot_ids = fields.One2many('stock.lot', 'parent_lot_id', string="Derived Products")
