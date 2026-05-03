from odoo import models, fields, api

class AgriIntervention(models.Model):
    _name = 'mrp.production'
    _inherit = 'mrp.production'

    # US-30-01: Auto-calculated Carbon Emission for this intervention
    calculated_carbon_emission = fields.Float("Calculated Carbon Emission (kg CO2e)", compute='_compute_carbon_emission', store=True)

    @api.depends('move_raw_ids.product_uom_qty', 'move_raw_ids.product_id.carbon_emission_factor')
    def _compute_carbon_emission(self):
        for mo in self:
            total_emission = 0.0
            for move in mo.move_raw_ids:
                total_emission += move.product_uom_qty * (move.product_id.carbon_emission_factor or 0.0)
            mo.calculated_carbon_emission = total_emission