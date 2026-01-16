from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CreationMethodMixin(models.AbstractModel):
    """
    Mixin class for common create method patterns
    """
    _name = 'farm.supply.creation.method.mixin'
    _description = 'Farm Supply Creation Method Mixin'

    @api.model
    def create(self, vals):
        """
        Base create method with common logic that can be extended
        """
        # Common logic can be added here
        record = super().create(vals)
        return record


class ComputedFieldMixin(models.AbstractModel):
    """
    Mixin class for common computed field patterns
    """
    _name = 'farm.supply.computed.field.mixin'
    _description = 'Farm Supply Computed Field Mixin'

    def _compute_total_amount(self):
        """
        Common method to compute total amount for various models
        """
        for record in self:
            # Default implementation - can be overridden in specific models
            record.total_amount = 0.0

    def _compute_total_energy(self):
        """
        Common method to compute total energy consumption
        """
        for record in self:
            # Default implementation - can be overridden in specific models
            record.total_energy_consumption = 0.0


class ComplianceMixin(models.AbstractModel):
    """
    Mixin class for common compliance and validation patterns
    """
    _name = 'farm.supply.compliance.mixin'
    _description = 'Farm Supply Compliance Mixin'

    def _compute_compliance_warning(self):
        """
        Common method to compute compliance warnings
        """
        for record in self:
            # Default implementation - can be overridden in specific models
            record.is_compliance_warning = False