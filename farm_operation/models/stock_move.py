from odoo import models, fields

class StockMove(models.Model):
    _inherit = 'stock.move'

    # 收获分级字段 [US-02-04]
    quality_grade = fields.Selection([
        ('grade_a', 'Grade A (特级/优等)'),
        ('grade_b', 'Grade B (一级/合格)'),
        ('grade_c', 'Grade C (二级/次品)'),
    ], string="Quality Grade")

    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        """ 重写以确保分级信息传递到移动行和最终批次 """
        vals = super()._prepare_move_line_vals(quantity=quantity, reserved_quant=reserved_quant)
        if self.quality_grade:
            vals['quality_grade'] = self.quality_grade
        return vals
