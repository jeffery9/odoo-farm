from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta

class FarmComplianceAuditStandard(models.Model):
    _name = 'farm.compliance.audit.standard'
    _description = 'Compliance Audit Standard'

    name = fields.Char("Standard Name", required=True)  # e.g., GlobalGAP, FSMA
    country_id = fields.Many2one('res.country', string="Applicable Country")
    code = fields.Char("Standard Code")
    active = fields.Boolean(default=True)

class FarmExportCompliance(models.Model):
    _name = 'farm.export.compliance'
    _inherit = 'farm.export.compliance'

    standard_id = fields.Many2one('farm.compliance.audit.standard', string="Compliance Standard")
    last_audit_run = fields.Datetime("Last Audit Run")
    audit_log = fields.Text("Audit Log Details")
    
    missing_records = fields.Boolean("Missing Required Records", compute='_compute_compliance_gaps', store=True)
    withdrawal_violation = fields.Boolean("Withdrawal Period Violation", compute='_compute_compliance_gaps', store=True)

    @api.depends('standard_id', 'product_id', 'target_market_id')
    def _compute_compliance_gaps(self):
        for rec in self:
            # Placeholder for complex audit logic
            # In a real scenario, this would query farm.operation and harvest records
            rec.missing_records = False
            rec.withdrawal_violation = False

    def action_generate_technical_dossier(self):
        """
        Israel Style: Generates a technical summary of the production quality.
        Aggregates VRA precision data, GDD curves, and Carbon metrics.
        """
        self.ensure_one()
        dossier = []
        dossier.append(_("--- TECHNICAL PRODUCTION DOSSIER ---"))
        dossier.append(_("Product: %s") % self.product_id.name)
        
        # 1. Precision VRA Data
        prescriptions = self.env['farm.vra.prescription'].search([
            ('location_id', '=', self.product_id.origin_location_id.id if hasattr(self.product_id, 'origin_location_id') else False)
        ], limit=1)
        if prescriptions:
            dossier.append(_("[VRA] Precision Variable Application enabled. Avg Rate: %s kg/mu") % prescriptions.base_rate)
        
        # 2. Biological Twin / Intelligence
        twin = self.env['farm.biological.twin'].search([
            ('product_id', '=', self.product_id.id)
        ], order='create_date desc', limit=1)
        if twin:
            dossier.append(_("[AI] Biological Twin monitored. Total GDD: %s C. Health Score: %s") % (twin.accumulated_gdd, twin.health_score))
            dossier.append(_("[ESG] Carbon Intensity: %s kg CO2e / kg") % twin.carbon_intensity)

        # 3. Quality Assurance
        if self.residue_limit_ok:
            dossier.append(_("[QC] MRL (Pesticide Residue) compliant with EU/US standards."))

        self.audit_log = "\n".join(dossier)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Dossier Generated'),
                'message': _('Technical production dossier is now available in the audit log.'),
                'type': 'success',
            }
        }

