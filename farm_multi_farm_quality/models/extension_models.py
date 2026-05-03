from odoo import models, fields

class CooperativeEntityExtensionQuality(models.Model):
    _name = 'cooperative.entity'
    _inherit = 'cooperative.entity'

    quality_control_standard_ids = fields.One2many('quality.control.standard', 'cooperative_id', string='Quality Standards')
