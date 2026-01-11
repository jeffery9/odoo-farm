from odoo import models, fields, api

class PosOrder(models.Model):
    _inherit = 'pos.order'

    # 关联采摘地块 [US-16]
    picking_location_id = fields.Many2one(
        'stock.location', 
        string="Picking Source Plot",
        domain=[('is_land_parcel', '=', True)],
        help="The specific land parcel where these products were picked."
    )

    def _prepare_invoice_vals(self):
        vals = super()._prepare_invoice_vals()
        # 传递地块信息到发票（可选）
        return vals

class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    # 支持行级别的批次指定（溯源）
    lot_id = fields.Many2one('stock.lot', string="Production Lot")
