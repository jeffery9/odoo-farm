from odoo import models, fields, api

class StockLot(models.Model):
    _inherit = 'stock.lot'

    # US-30-01: Accumulated Carbon Footprint for this batch
    carbon_footprint = fields.Float("Carbon Footprint (kg CO2e)", compute='_compute_carbon_footprint', store=True)

    @api.depends('create_date') # Simplified trigger
    def _compute_carbon_footprint(self):
        for lot in self:
            # Accumulated from the intervention that produced this lot
            mo = self.env['mrp.production'].search([('lot_producing_id', '=', lot.id)], limit=1)
            lot.carbon_footprint = mo.calculated_carbon_emission if mo else 0.0