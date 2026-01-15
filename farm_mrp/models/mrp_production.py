# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    industry_type = fields.Selection(related='bom_id.industry_type', string="Industry Standard", store=True, readonly=True)

    def _get_isl_model(self):
        """ 
        Hook for specialized modules to return their ISL model name. 
        Each module should inherit this and return its specific model.
        """
        return False

    @api.model_create_multi
    def create(self, vals_list):
        orders = super(MrpProduction, self).create(vals_list)
        for order in orders:
            isl_model = order._get_isl_model()
            if isl_model:
                # Check if ISL record already exists (to avoid duplicates if created from ISL side)
                existing = self.env[isl_model].search([('production_id', '=', order.id)], limit=1)
                if not existing:
                    self.env[isl_model].create({'production_id': order.id})
        return orders

    def get_formview_action(self, access_uid=None):
        """ US-TECH-06-19: Transparently redirect to ISL view if available. """
        res = super(MrpProduction, self).get_formview_action(access_uid=access_uid)
        isl_model = self._get_isl_model()
        if isl_model:
            isl_record = self.env[isl_model].search([('production_id', '=', self.id)], limit=1)
            if isl_record:
                res.update({
                    'res_model': isl_model, 
                    'res_id': isl_record.id,
                    'context': dict(self.env.context, isl_active=True)
                })
        return res

    def action_confirm(self):
        res = super(MrpProduction, self).action_confirm()
        for order in self:
            self._trigger_isl_hook('isl_post_confirm', order.id)
        return res

    def button_mark_done(self):
        res = super(MrpProduction, self).button_mark_done()
        for order in self:
            self._trigger_isl_hook('isl_post_done', order.id)
        return res

    def _trigger_isl_hook(self, hook_name, base_id):
        """ Helper to route events to ISL sub-models. """
        isl_model = self._get_isl_model()
        if isl_model:
            isl_rec = self.env[isl_model].search([('production_id', '=', base_id)], limit=1)
            if isl_rec and hasattr(isl_rec, hook_name):
                getattr(isl_rec, hook_name)()
