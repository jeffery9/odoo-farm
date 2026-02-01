# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class FarmHaccpPoint(models.Model):
    """
    [ISL Layer] Critical Control Point (CCP).
    Proxies quality.point to enforce food safety redlines.
    """
    _name = 'farm.haccp.point'
    _description = 'HACCP Critical Control Point'
    _inherits = {'quality.point': 'quality_point_id'}
    
    quality_point_id = fields.Many2one('quality.point', required=True, ondelete='cascade')

    # Critical Limits (CL) [US-114-01]
    is_ccp = fields.Boolean("Is Critical Control Point", default=True)
    cl_min = fields.Float("Critical Limit Min")
    cl_max = fields.Float("Critical Limit Max")
    cl_uom_id = fields.Many2one('uom.uom', string="CL Unit")
    
    hazard_description = fields.Text("Identified Hazard")
    corrective_action_plan = fields.Text("Standard Corrective Action")

class FarmHaccpCheck(models.Model):
    """
    [ISL Layer] HACCP Monitoring Record.
    Proxies quality.check to handle corrective actions and blocking.
    """
    _name = 'farm.haccp.check'
    _description = 'HACCP Monitoring Record'
    _inherits = {'quality.check': 'quality_check_id'}
    _inherit = ['agri.incident.alert.mixin']

    quality_check_id = fields.Many2one('quality.check', required=True, ondelete='cascade')

    # Monitoring results
    actual_value = fields.Float("Measured Value")
    is_violated = fields.Boolean("CL Violation", compute='_compute_violation', store=True)
    
    # Corrective Action [US-114-03]
    corrective_action_taken = fields.Text("Corrective Action Taken")
    ca_responsible_id = fields.Many2one('res.users', string="Action Done By")

    @api.depends('actual_value', 'point_id')
    def _compute_violation(self):
        for rec in self:
            # Look up the ISL proxy for the point
            haccp_point = self.env['farm.haccp.point'].search([('quality_point_id', '=', rec.point_id.id)], limit=1)
            if haccp_point and rec.actual_value:
                if (haccp_point.cl_min and rec.actual_value < haccp_point.cl_min) or \
                   (haccp_point.cl_max and rec.actual_value > haccp_point.cl_max):
                    rec.is_violated = True
                    # Trigger Incident DNA (Level 2)
                    rec.report_incident('high', 'HACCP CL Violation', 
                                       _("CCP %s violated! Measured: %s") % (haccp_point.name, rec.actual_value))
                else:
                    rec.is_violated = False
            else:
                rec.is_violated = False
