# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def _hook_pre_confirm(self):
        """[US-001-09] Crop Rotation & Continuous Cropping Check"""
        super()._hook_pre_confirm()
        if self.intervention_type == 'sowing' and self.location_id and self.product_id:
            rotation_model = self.env['farm.crop.rotation.history']
            risk_info = rotation_model.check_continuous_cropping_risk(
                self.location_id.id, 
                self.product_id.product_tmpl_id,
                self.date_planned_start or fields.Date.today()
            )
            
            if risk_info['has_risk']:
                # For sowing, we might want to warn or block. 
                # According to BDD, it should at least warn.
                self.message_post(body=_("ROTATION WARNING: %s") % risk_info['message'])
                # If risk is too high (e.g. > 80), we could block
                if risk_info['risk_level'] >= 80:
                    raise UserError(_("CROP ROTATION BLOCK: Critical continuous cropping risk detected!"))
