# -*- coding: utf-8 -*-
from odoo import models, fields

class FarmCropCycle(models.Model):
    _name = 'farm.crop.cycle'
    _description = 'Crop Growth Cycle (作物生长周期)'

    name = fields.Char("Cycle Name", required=True)
