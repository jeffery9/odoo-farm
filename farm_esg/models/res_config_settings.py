from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # US-101: Sustainability as a Plugin
    is_esg_sustainability_active = fields.Boolean(
        "Activate ESG Sustainability DNA",
        config_parameter='farm_esg.is_esg_sustainability_active',
        help="When enabled, sustainability metrics (Carbon, TBL, Social) are injected into all business domains."
    )
