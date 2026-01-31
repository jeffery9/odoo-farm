from odoo import models, fields, api, _

class AgriAllergen(models.Model):
    _name = 'agri.allergen'
    _description = 'Agricultural Food Allergen'

    name = fields.Char("Allergen Name", required=True, translate=True)
    code = fields.Char("Code")
    description = fields.Text("Description")