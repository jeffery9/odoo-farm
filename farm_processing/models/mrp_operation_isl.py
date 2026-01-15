# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class FarmIndustryOperation(models.Model):
    _name = 'farm.industry.operation'
    _description = 'Industry-Specific Process Operation (ISL Layer)'
    _inherits = {'mrp.routing.workcenter': 'operation_id'}

    operation_id = fields.Many2one('mrp.routing.workcenter', string='Base Operation', required=True, ondelete='cascade')
    
    # --- Specialized Instructions ---
    technical_manual = fields.Html("Technical SOP", help="Detailed industry standard operating procedure.")
    
    # Critical Control Parameters (US-14-09 sync)
    param_monitoring_required = fields.Boolean("Monitor Critical Parameters")
    target_value = fields.Float("Target Value")
    tolerance_range = fields.Float("Tolerance (+/-)")

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
