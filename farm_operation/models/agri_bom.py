from odoo import models, fields, api

class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    # 稀释比例 [US-13]
    dilution_ratio = fields.Float(
        "Dilution Ratio (1:N)", 
        default=0.0,
        help="If set, the component quantity will be calculated as (Finished Qty / Ratio). E.g. 1:500."
    )
    
    # 饲喂比例 [US-09]
    feeding_ratio = fields.Float(
        "Feeding Ratio (%)", 
        default=0.0,
        help="Percentage of total biomass (Count * Avg Weight) for daily feeding."
    )

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.onchange('bom_id', 'product_qty', 'product_uom_id')
    def _onchange_bom_id(self):
        """ 拦截并根据稀释比例和饲喂比例修正物料需求量 """
        res = super()._onchange_bom_id()
        for mo in self:
            # 尝试获取生物资产信息（如果关联了任务）
            lot = mo.agri_task_id.biological_lot_id if hasattr(mo, 'agri_task_id') else False
            
            for move in mo.move_raw_ids:
                bom_line = mo.bom_id.bom_line_ids.filtered(lambda l: l.product_id == move.product_id)
                if not bom_line:
                    continue
                    
                if bom_line.dilution_ratio > 0:
                    move.product_uom_qty = mo.product_qty / bom_line.dilution_ratio
                elif bom_line.feeding_ratio > 0 and lot:
                    # 计算生物总量 = 数量 * 平均体重
                    total_biomass = (getattr(lot, 'animal_count', 0) * getattr(lot, 'average_weight', 0.0))
                    # 投入量 = 总量 * 比例 / 100
                    move.product_uom_qty = total_biomass * (bom_line.feeding_ratio / 100.0)
        return res

    def _get_moves_raw_values(self):
        """ 针对实际保存逻辑的覆盖（后台创建 MO 时生效） """
        res = super()._get_moves_raw_values()
        for move_vals in res:
            bom_line = self.env['mrp.bom.line'].browse(move_vals.get('bom_line_id'))
            if bom_line and bom_line.dilution_ratio > 0:
                # 修正数量
                move_vals['product_uom_qty'] = self.product_qty / bom_line.dilution_ratio
        return res
