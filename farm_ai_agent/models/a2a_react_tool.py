# -*- coding: utf-8 -*-
from odoo import models, fields

class A2AReactTool(models.Model):
    """
    Registry of safe/authorized Odoo method calls that an AI Agent can execute.
    """
    _name = 'agri.a2a.react.tool'
    _description = 'A2A React Safe Tool'

    name = fields.Char('Tool Name', required=True)
    model_name = fields.Char('Model Name', required=True)
    method_name = fields.Char('Method Name', required=True)
    required_gxp_gating = fields.Boolean('Requires GxP Gating / CCP', default=False)
    is_active = fields.Boolean('Is Active', default=True)
