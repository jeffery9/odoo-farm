# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

class AgriInterventionMixin(models.AbstractModel):
    _inherit = 'agri.intervention.mixin'

    # Scenario 51: Strict JA Brand SOP Enforcement
    sop_compliance_status = fields.Selection([
        ('compliant', 'Fully Compliant (JA Premium)'),
        ('warning', 'Minor Deviation'),
        ('violation', 'SOP Violation (Downgraded)')
    ], string='SOP Compliance', default='compliant', tracking=True)
    
    def action_log_violation(self, reason):
        """Called automatically if a task is late or IoT detects banned chemical."""
        self.write({
            'sop_compliance_status': 'violation'
        })
        # Automatically downgrade linked crop/asset
        if hasattr(self, 'asset_id') and self.asset_id:
            self.asset_id.write({'quality_grade': 'commodity'})
            self.asset_id.message_post(body=f"⚠️ Downgraded to Commodity due to SOP Violation: {reason}")
