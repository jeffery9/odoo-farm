from odoo import models, fields

class StockLot(models.Model):
    _inherit = 'stock.lot'

    # B2C Digital Twin Stream URL
    csa_stream_url = fields.Char("Public Stream URL", readonly=True, help="URL for the customer to watch their adopted asset.")
    csa_adopter_id = fields.Many2one('res.partner', string="Adopter")
