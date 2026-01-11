from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    requires_cold_chain = fields.Boolean("Cold Chain Required", default=False)
    target_temperature_min = fields.Float("Min Temp (℃)")
    target_temperature_max = fields.Float("Max Temp (℃)")

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    is_cold_chain = fields.Boolean("Is Cold Chain Transport", compute='_compute_is_cold_chain', store=True)
    actual_transport_temp = fields.Float("Actual Transport Temp (℃)")
    
    packaging_level = fields.Selection([
        ('box', 'Box/Carton'),
        ('crate', 'Crate'),
        ('pallet', 'Pallet')
    ], string="Primary Packaging")

    @api.depends('move_ids.product_id')
    def _compute_is_cold_chain(self):
        for picking in self:
            picking.is_cold_chain = any(picking.move_ids.mapped('product_id.requires_cold_chain'))
