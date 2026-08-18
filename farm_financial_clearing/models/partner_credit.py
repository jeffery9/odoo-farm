# -*- coding: utf-8 -*-
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    impact_credits = fields.Float("Cooperative Impact Credits", default=0.0)
