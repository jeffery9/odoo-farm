# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    industry_type = fields.Selection([
        ('standard', 'Standard'),
    ], string="Industry Type", default='standard')

    def _get_isl_model(self):
        """ Hook for specialized modules to return their ISL model name. """
        return False

    @api.model_create_multi
    def create(self, vals_list):
        boms = super(MrpBom, self).create(vals_list)
        for bom in boms:
            isl_model = bom._get_isl_model()
            if isl_model:
                existing = self.env[isl_model].search([('bom_id', '=', bom.id)], limit=1)
                if not existing:
                    self.env[isl_model].create({'bom_id': bom.id})
        return boms

    def get_formview_action(self, access_uid=None):
        """ US-TECH-06-19: Redirect to ISL-specialized view if available. """
        res = super(MrpBom, self).get_formview_action(access_uid=access_uid)
        isl_model = self._get_isl_model()
        if isl_model:
            isl_record = self.env[isl_model].search([('bom_id', '=', self.id)], limit=1)
            if isl_record:
                res.update({
                    'res_model': isl_model,
                    'res_id': isl_record.id,
                    'context': dict(self.env.context, isl_active=True)
                })
        return res
