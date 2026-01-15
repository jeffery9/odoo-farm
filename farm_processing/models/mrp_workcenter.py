# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    # US-TECH-05-08: Industry Capability
    industry_capability = fields.Selection([
        ('standard', 'General Purpose'),
        ('agri_machinery', 'Agricultural Machinery / Field'),
        ('food_line', 'Food Processing Line'),
        ('livestock_pen', 'Livestock Pen / Facility'),
        ('lab', 'Laboratory / Testing')
    ], string='Industry Capability', default='standard', required=True)

class MrpRoutingWorkcenter(models.Model):
    _inherit = 'mrp.routing.workcenter'

    # Filter logic will be handled at the XML view level via domain
    pass
