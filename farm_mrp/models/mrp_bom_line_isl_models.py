# -*- coding: utf-8 -*-
from odoo import models, fields, api, _, exceptions
from odoo.exceptions import ValidationError

class MrpBomLineIslAbstract(models.AbstractModel):
    """
    Abstract base model for Industry Specialized Layer (ISL) models.
    This provides common functionality for all ISL implementations of mrp.bom.line.
    """
    _name = 'mrp.bom.line.isl.abstract'
    _description = 'Abstract ISL for BOM Line'
    _inherit = 'mrp.bom.line'

    def write(self, vals):
        """
        Prevent direct modification of protected fields when ISL record exists.
        Allow bypass for internal operations.
        """
        # Check if this is an internal bypass operation
        if vals.get('_isl_bypass'):
            vals.pop('_isl_bypass', None)
            return super().write(vals)

        # For regular operations, prevent modification of protected fields if ISL exists
        protected_fields = self._get_isl_protected_fields()
        if protected_fields:
            # Check if any protected field is being modified
            modifying_protected_fields = any(field in vals for field in protected_fields)
            if modifying_protected_fields:
                # Check if there's an associated ISL record
                isl_record = self._get_isl_record()
                if isl_record:
                    protected_field_names = ", ".join(protected_fields)
                    raise ValidationError(
                        _("Cannot modify '%s' directly. Please modify through the specialized interface '%s'.") %
                        (protected_field_names, isl_record._name)
                    )

        return super().write(vals)

    def unlink(self):
        """
        Prevent deletion of base records that have ISL counterparts.
        Allow bypass for internal operations.
        """
        # Check if this is an internal bypass operation
        if self.env.context.get('isl_bypass_unlink'):
            return super().unlink()

        # Check if any records have associated ISL records
        for record in self:
            isl_record = self._get_isl_record()
            if isl_record:
                raise ValidationError(
                    _("Cannot delete base record that has an associated ISL record. Please delete the ISL record first.")
                )

        return super().unlink()

    def _get_isl_protected_fields(self):
        """Override this method to return list of protected fields for specific ISL model"""
        return []

    def _get_isl_record(self):
        """Get associated ISL record for this base record using centralized infrastructure"""
        redirector = self.env['isl.model.redirector']
        return redirector.get_isl_record('mrp.bom.line', self.id)

    def action_view_isl_record(self):
        """Override this method to provide navigation to ISL record"""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('No ISL Record'),
                'message': _('This record does not have an associated ISL record.'),
                'type': 'info',
            }
        }

    def _compute_isl_record_type(self):
        """Override this method to compute ISL record type for display"""
        return None