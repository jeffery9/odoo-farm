# -*- coding: utf-8 -*-
from odoo import models, fields, api

class MrpRoutingWorkcenter(models.Model):
    """
    Agri Operational Phase Step (Routing Line):
    Inherit agri.operation.mixin to equip operations with technical instruction SOPs
    and critical control parameters (CCPs) for smart MQTT setpoint routing.
    """
    _name = 'mrp.routing.workcenter'
    _inherit = ['mrp.routing.workcenter', 'agri.operation.mixin']
