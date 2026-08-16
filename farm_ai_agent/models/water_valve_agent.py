# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class FarmWaterValve(models.Model):
    _name = 'farm.water.valve'
    _inherit = ['farm.water.valve', 'agri.agent.sandbox.mixin']
