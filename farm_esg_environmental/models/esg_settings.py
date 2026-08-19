# -*- coding: utf-8 -*-
from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_enable_carbon_tracking = fields.Boolean(
        "Enable Soil Carbon Footprint Tracking", 
        implied_group='farm_esg_environmental.group_esg_carbon'
    )
    group_enable_circular_tracking = fields.Boolean(
        "Enable Organic Circular Waste Management",
        implied_group='farm_esg_environmental.group_esg_circular'
    )
