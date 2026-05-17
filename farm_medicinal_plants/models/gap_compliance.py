from odoo import models, fields, api, _
from odoo.exceptions import UserError

class FarmMedicinalProduction(models.Model):
    _inherit = 'farm.medicinal.production'

    hplc_lab_result_id = fields.Many2one('agri.quality.check', string="HPLC Lab Result", domain="[('test_type', '=', 'hplc')]")
    gap_certified = fields.Boolean("GAP Certified", compute="_compute_gap_compliance", store=True)

    @api.depends('is_daodi_verified', 'hplc_lab_result_id.quality_state', 'hplc_lab_result_id.measure', 'target_compound_level')
    def _compute_gap_compliance(self):
        """
        [US-SCENARIO-35] Medicinal Plants GAP Traceability
        Automatically evaluate if the lot meets Good Agricultural Practices (GAP).
        Requires geographical verification and a passed HPLC lab result demonstrating 
        the active ingredient meets the target threshold.
        """
        for record in self:
            if record.is_daodi_verified and record.hplc_lab_result_id and record.hplc_lab_result_id.quality_state == 'pass':
                if record.hplc_lab_result_id.measure >= record.target_compound_level:
                    record.gap_certified = True
                else:
                    record.gap_certified = False
            else:
                record.gap_certified = False

    def action_generate_passport(self):
        self.ensure_one()
        if not self.gap_certified:
            raise UserError(_("Cannot generate passport: Lot is not GAP certified. Ensure Daodi verification and valid HPLC lab results."))
        
        self.message_post(body=_("GAP Passport generated successfully. Active Compound Level: %s%%") % self.hplc_lab_result_id.measure)
        return True

