# -*- coding: utf-8 -*-
from odoo import models, fields

class AgriInterventionTest(models.Model):
    """
    Test implementation of the Intervention Engine.
    """
    _name = 'agri.intervention.test'
    _description = 'Agricultural Intervention (Test)'
    _inherit = ['agri.intervention.base', 'mail.thread', 'mail.activity.mixin']
    _order = 'date_planned_start desc, id desc'
