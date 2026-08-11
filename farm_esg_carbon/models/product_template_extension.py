from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # US-060-01: Carbon Emission Factor (kg CO2e / unit)
    carbon_emission_factor = fields.Float("Carbon Emission Factor (kg CO2e / unit)", help="CO2 equivalent emissions per unit of this product.")