# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class FarmWaterValve(models.Model):
    """
    Autonomous Farm Water Valve (智能水阀模型 - [De-industrialized] / BDD Safe)
    """
    _name = 'farm.water.valve'
    _description = 'Farm Water Valve'

    name = fields.Char("Valve Name", required=True)
    status = fields.Selection([('open', 'Open'), ('cutoff', 'Cut-Off')], default='open', string="Status")
    pressure_psi = fields.Float("Pressure (PSI)", default=0.0)

    @api.constrains('pressure_psi')
    def _check_pressure_safety(self):
        """Ensure water pressure does not exceed safety limits (150.0 PSI)"""
        for rec in self:
            if rec.pressure_psi > 150.0:
                # Safely transition status to cutoff and raise safety block exception
                rec.status = 'cutoff'
                raise ValidationError(_("WATER_PRESSURE_OVERLOAD_BLOCK: Pressure %s PSI exceeds maximum safety threshold (150.0 PSI).") % rec.pressure_psi)
