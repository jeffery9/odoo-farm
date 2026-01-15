from odoo import models, fields, api, _

class FarmAllergen(models.Model):
    _name = 'farm.allergen'
    _description = 'Food Allergen'

    name = fields.Char("Allergen Name", required=True, translate=True)
    code = fields.Char("Code")
    description = fields.Text("Description")
