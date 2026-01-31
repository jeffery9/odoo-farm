from odoo import models, fields, api, _

class AgriStockMove(models.Model):
    """
    Stock Move: The physical conduit of mass and value.
    Injects Nutrient and Sustainability Mixins to preserve physical evidence during flow.
    """
    _name = 'stock.move'
    _inherit = [
        'stock.move',
        'agri.nutrient.mixin',       # Level 1: Mass Balance
        'agri.sustainability.mixin', # Level 0: Value Standard
    ]

    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        """
        [Lossless Mode] Preserves nutrient data when moving into lines/lots.
        """
        vals = super(AgriStockMove, self)._prepare_move_line_vals(quantity=quantity, reserved_quant=reserved_quant)
        vals.update({
            'nitrogen_qty': self.nitrogen_qty,
            'phosphorus_qty': self.phosphorus_qty,
            'potassium_qty': self.potassium_qty,
        })
        return vals

class AgriStockMoveLine(models.Model):
    _name = 'stock.move.line'
    _inherit = [
        'stock.move.line',
        'agri.nutrient.mixin',
    ]
