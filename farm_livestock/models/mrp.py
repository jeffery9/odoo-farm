# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def _hook_pre_start(self):
        """[US-003-02] Livestock Health Gating before starting"""
        super()._hook_pre_start()
        if self.industry_type == 'livestock':
            # Identify the biological lot (animal group)
            # In farm_livestock, lot_id is often used on the intervention/task
            lot = getattr(self, 'lot_producing_id', False) # Odoo standard
            if lot and hasattr(lot, 'health_state') and lot.health_state == 'quarantine':
                raise UserError(_("HEALTH BLOCK: Cannot start intervention on animals in quarantine!"))

    def _get_isl_model(self):
        res = super(MrpProduction, self)._get_isl_model()
        if self.industry_type == 'livestock':
            return 'agri.isl.livestock.task'
        return res

class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    industry_type = fields.Selection(selection_add=[
        ('livestock', 'Livestock'),
    ], ondelete={'livestock': 'set null'})

    def _get_isl_model(self):
        res = super(MrpBom, self)._get_isl_model()
        if self.industry_type == 'livestock':
            return 'agri.isl.livestock.recipe'
        return res
