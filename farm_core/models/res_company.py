from odoo import models, fields

class ResCompany(models.Model):
    _name = 'res.company'
    _inherit = 'res.company'
    
    properties_definition = fields.PropertiesDefinition('Farm Properties Definition')
