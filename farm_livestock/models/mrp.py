# -*- coding: utf-8 -*-
from odoo import models, fields, api

class MrpProduction(models.Model):
    _name = 'mrp.production'
    _inherit = 'mrp.production'

    def _get_isl_model(self):
        res = super(MrpProduction, self)._get_isl_model()
        if self.industry_type == 'livestock':
            return 'agri.isl.livestock.production'
        return res

class MrpBom(models.Model):
    _name = 'mrp.bom'
    _inherit = 'mrp.bom'

    industry_type = fields.Selection(selection_add=[
        ('livestock', 'Livestock'),
    ], ondelete={'livestock': 'set null'})

    def _get_isl_model(self):
        res = super(MrpBom, self)._get_isl_model()
        if self.industry_type == 'livestock':
            return 'agri.isl.livestock.bom'
        return res
