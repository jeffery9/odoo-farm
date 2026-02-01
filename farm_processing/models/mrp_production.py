# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class MrpProduction(models.Model):
    _inherit = ['mrp.production', 'agri.quality.gate.mixin']

    # --- Processing Specific Gate Logic ---
    def _get_isl_model(self):
        res = super(MrpProduction, self)._get_isl_model()
        if self.industry_type == 'food_processing':
            return 'farm.processing.production'
        return res

    def action_confirm(self):
        """ Processing-specific pre-confirmation checks. """
        for order in self:
            if order.industry_type == 'food_processing':
                # [Level 2: DNA Gate] Enforce Quality Gate
                order.validate_quality_gate()
                # US-14-09: HACCP / Quality Gate Pre-check
                pass
        return super(MrpProduction, self).action_confirm()

    def button_mark_done(self):
        """ Processing-specific pre-done checks. [Level 2: HACCP Gate] """
        for order in self:
            # US-114-02: Check if all related HACCP/CCP points are passed
            haccp_violations = self.env['farm.haccp.check'].search([
                ('quality_check_id.production_id', '=', order.id),
                ('is_violated', '=', True)
            ])
            if haccp_violations:
                raise UserError(_("HACCP BLOCK: Production cannot be completed. "
                                "Critical Limit violations detected in CCP checks: %s") % 
                                ", ".join(haccp_violations.mapped('point_id.name')))
            
            if order.industry_type == 'food_processing':
                # Energy checks etc.
                pass
        return super(MrpProduction, self).button_mark_done()