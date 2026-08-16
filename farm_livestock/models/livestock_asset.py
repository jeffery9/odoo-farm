# -*- coding: utf-8 -*-
from odoo import models, fields

class FarmLivestockAsset(models.Model):
    _name = 'farm.livestock.asset'
    _description = 'Livestock Biological Asset (畜牧生物资产)'

    ear_tag_code = fields.Char("Ear Tag Code (耳标编号)", required=True)
    species = fields.Char("Species (物种)")
