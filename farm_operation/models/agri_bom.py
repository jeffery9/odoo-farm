from odoo import models, fields, api, _

class MrpBom(models.Model):
    """
    Agricultural Recipe (BOM):
    Injecting Nutrient and View Mixins to transform industrial BOM into Bio-Recipe.
    """
    _name = 'mrp.bom'
    _inherit = [
        'mrp.bom', 
        'agri.bom.mixin',
        'agri.view.mixin',           # Level 0: UI Isolation
        'agri.nutrient.mixin',       # Level 1: Nutrient Composition
        'agri.sustainability.mixin', # Level 0: Standard
    ]

    def _get_embedding_content(self):
        self.ensure_one()
        return f"Recipe {self.code or self.product_tmpl_id.name}: N={self.nitrogen_qty}, P={self.phosphorus_qty}."

class MrpBomLine(models.Model):
    _name = 'mrp.bom.line'
    _inherit = [
        'mrp.bom.line', 
        'agri.bom.line.mixin',
        'agri.nutrient.mixin', 
    ]

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.onchange('bom_id', 'product_qty', 'product_uom_id')
    def _onchange_bom_id(self):
        """ 拦截并根据稀释比例和饲喂比例修正物料需求量 """
        res = super()._onchange_bom_id()
        for mo in self:
            lot = mo.agri_task_id.biological_lot_id if hasattr(mo, 'agri_task_id') else False
            for move in mo.move_raw_ids:
                bom_line = mo.bom_id.bom_line_ids.filtered(lambda l: l.product_id == move.product_id)
                if not bom_line:
                    continue
                if bom_line.dilution_ratio > 0:
                    move.product_uom_qty = mo.product_qty / bom_line.dilution_ratio
                elif bom_line.feeding_ratio > 0 and lot:
                    total_biomass = (getattr(lot, 'animal_count', 0) * getattr(lot, 'average_weight', 0.0))
                    move.product_uom_qty = total_biomass * (bom_line.feeding_ratio / 100.0)
        return res

    def _get_moves_raw_values(self):
        """ 针对实际保存逻辑的覆盖（后台创建 MO 时生效） """
        res = super()._get_moves_raw_values()
        for move_vals in res:
            bom_line = self.env['mrp.bom.line'].browse(move_vals.get('bom_line_id'))
            if bom_line and bom_line.dilution_ratio > 0:
                move_vals['product_uom_qty'] = self.product_qty / bom_line.dilution_ratio
        return res