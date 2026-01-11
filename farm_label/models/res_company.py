from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    label_background_image = fields.Binary("Label Background Image", help="Background image for all agricultural labels.")

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    label_background_image = fields.Binary(
        related='company_id.label_background_image',
        string="Label Background Image",
        readonly=False
    )