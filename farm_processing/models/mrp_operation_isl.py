# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class FarmIndustryOperation(models.Model):
    _name = 'farm.industry.operation'
    _description = 'Industry-Specific Process Operation (ISL Layer)'
    _inherits = {'mrp.routing.workcenter': 'operation_id'}

    operation_id = fields.Many2one('mrp.routing.workcenter', string='Base Operation', required=True, ondelete='cascade')

class MrpRoutingWorkcenter(models.Model):
    _inherit = 'mrp.routing.workcenter'

    def get_formview_action(self, access_uid=None):
        """ US-TECH-06-23: Transparent redirection to Industry Specialized Operation View. """
        res = super(MrpRoutingWorkcenter, self).get_formview_action(access_uid=access_uid)
        isl_record = self.env['farm.industry.operation'].search([('operation_id', '=', self.id)], limit=1)
        if isl_record:
            res.update({
                'res_model': 'farm.industry.operation',
                'res_id': isl_record.id,
            })
        return res
