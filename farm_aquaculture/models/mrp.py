# -*- coding: utf-8 -*-
from odoo import models, fields, api

class MrpProduction(models.Model):    _inherit = 'mrp.production'

    def _get_isl_model(self):
        res = super(MrpProduction, self)._get_isl_model()
        if self.industry_type == 'aquaculture':
            return 'agri.isl.aquaculture.production'
        return res

class MrpBom(models.Model):    _inherit = 'mrp.bom'

    industry_type = fields.Selection(selection_add=[
        ('aquaculture', 'Aquaculture'),
    ], ondelete={'aquaculture': 'set null'})

    def _get_isl_model(self):
        res = super(MrpBom, self)._get_isl_model()
        if self.industry_type == 'aquaculture':
            return 'agri.isl.aquaculture.bom'
        return res
