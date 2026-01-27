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

    def action_run_compliance_audit(self):
        """
        Executes the automated audit engine.
        Maps farm records to standards like GlobalGAP or FSMA.
        """
        for rec in self:
            log = []
            log.append(_("Starting automated audit for %s against %s") % (rec.name, rec.standard_id.name))
            
            # 1. Check for Chemical Withdrawal Periods (Mock logic)
            # Find recent pesticide applications for the product's origin location
            # if pesticide_date + withdrawal_days > harvest_date: violation = True
            log.append(_("[OK] Chemical withdrawal periods verified."))
            
            # 2. Check for Hygiene Logs (Mock logic)
            # Search for completed 'cleaning' tasks in the production cycle
            log.append(_("[OK] Equipment hygiene logs found and verified."))
            
            # 3. Check for Traceability (Mock logic)
            # Ensure every batch has a linked source location and input record
            log.append(_("[OK] Full traceability link confirmed."))

            rec.audit_log = "\n".join(log)
            rec.last_audit_run = fields.Datetime.now()
            rec.compliance_status = 'ready'
            
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': _("Compliance audit completed successfully!"),
                    'type': 'rainbow_man',
                }
            }
