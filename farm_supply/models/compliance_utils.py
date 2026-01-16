from odoo import models, fields, api


class ComplianceMixin(models.AbstractModel):
    """
    Mixin class for common compliance patterns
    """
    _name = 'farm.supply.compliance.utils'
    _description = 'Farm Supply Compliance Utilities'

    is_compliance_warning = fields.Boolean("Compliance Warning")
    compliance_status = fields.Selection([
        ('compliant', 'Compliant'),
        ('warning', 'Warning'),
        ('non_compliant', 'Non-Compliant'),
        ('pending_review', 'Pending Review'),
    ], string='Compliance Status', default='compliant')
    compliance_notes = fields.Text('Compliance Notes')
    last_compliance_check = fields.Datetime('Last Compliance Check')

    def _compute_compliance_warning(self):
        """
        Compute compliance warning based on various factors
        """
        for record in self:
            # Default implementation - to be overridden in specific models
            record.is_compliance_warning = False

    def trigger_compliance_check(self):
        """
        Trigger compliance check for the record
        """
        for record in self:
            record.last_compliance_check = fields.Datetime.now()
            # Additional compliance logic would go here