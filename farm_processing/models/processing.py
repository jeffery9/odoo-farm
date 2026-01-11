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
    
    # 损耗与平衡校验 [US-44]
    scrap_qty = fields.Float("Process Loss (kg)", help="Quantity lost during cleaning/sorting/processing")
    total_output_qty = fields.Float("Total Output Qty", compute='_compute_total_output_qty')
    is_balanced = fields.Boolean("Mass Balanced", compute='_compute_total_output_qty')

    @api.depends('move_finished_ids.product_uom_qty', 'scrap_qty', 'move_raw_ids.product_uom_qty')
    def _compute_total_output_qty(self):
        for mo in self:
            # 产出总量 = 成品 + 副产品 + 损耗
            finished_qty = sum(mo.move_finished_ids.mapped('product_uom_qty'))
            mo.total_output_qty = finished_qty + mo.scrap_qty
            
            # 投入总量
            raw_qty = sum(mo.move_raw_ids.mapped('product_uom_qty'))
            # 允许 0.1% 的微小舍入误差
            mo.is_balanced = abs(mo.total_output_qty - raw_qty) < (raw_qty * 0.001) if raw_qty > 0 else True

    def button_mark_done(self):
        """ 强制平衡校验 """
        for mo in self:
            if not mo.is_balanced:
                from odoo.exceptions import UserError
                raise UserError(_("MASS BALANCE ERROR: Total input (%s) does not match total output + loss (%s). Please adjust.") % (
                    sum(mo.move_raw_ids.mapped('product_uom_qty')), mo.total_output_qty
                ))
        return super().button_mark_done()

class StockLot(models.Model):
    _inherit = 'stock.lot'

    # 批次溯源：指向原材料批次
    parent_lot_id = fields.Many2one('stock.lot', string="Parent Lot/Origin", help="Trace back to the raw material lot")
    child_lot_ids = fields.One2many('stock.lot', 'parent_lot_id', string="Derived Products")
