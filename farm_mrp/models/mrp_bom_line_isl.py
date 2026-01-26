# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    def _get_isl_model(self):
        """
        Hook for specialized modules to return their ISL model name for BOM lines.
        Each module should inherit this and return its specific model.
        """
        # Determine ISL model based on the parent BOM's industry_type
        parent_bom = self.bom_id
        if parent_bom:
            if parent_bom.industry_type == 'livestock':
                return 'farm.livestock.bom.line'
            elif parent_bom.industry_type == 'processing':
                return 'farm.processing.bom.line'
            elif parent_bom.industry_type == 'aquaculture':
                return 'farm.aquaculture.bom.line'
            elif parent_bom.industry_type == 'crop':
                return 'farm.crop.bom.line'
        return False

    @api.model_create_multi
    def create(self, vals_list):
        lines = super(MrpBomLine, self).create(vals_list)
        for line in lines:
            # Use farm_isl's redirection mechanism
            redirector = self.env['isl.model.redirector']
            # For BOM lines, we need to think differently - they are linked to BOMs
            # The ISL record will be automatically created by the ISL redirection utility for the parent BOM
            # If needed, BOM line ISL records can be created separately when needed
        return lines

    def get_formview_action(self, access_uid=None):
        """ Transparently redirect to ISL view if available for BOM line. """
        # Use the centralized ISL redirection mechanism from farm_isl
        # Note: BOM line ISL redirection might be more complex as it depends on parent context
        redirector = self.env['isl.model.redirector']
        isl_record = redirector.get_isl_record('mrp.bom.line', self.id)

        if isl_record:
            return {
                'type': 'ir.actions.act_window',
                'res_model': isl_record._name,
                'res_id': isl_record.id,
                'view_mode': 'form',
                'context': dict(self.env.context, isl_active=True)
            }
        # If no ISL record exists, use the default behavior
        return super(MrpBomLine, self).get_formview_action(access_uid=access_uid)

    def write(self, vals):
        # Check if any records have ISL counterparts and if any protected fields are being modified
        if not self.env.context.get('bypass_isl_restrictions'):
            # Use centralized ISL infrastructure to get corresponding ISL record
            redirector = self.env['isl.model.redirector']

            for record in self:
                isl_record = redirector.get_isl_record('mrp.bom.line', record.id)
                if isl_record:
                    # Check for protected fields depending on the specific ISL model type
                    protected_fields = []
                    isl_model_name = isl_record._name

                    if 'livestock' in isl_model_name:
                        protected_fields = ['dilution_ratio', 'feeding_ratio', 'feed_purpose']
                    elif 'processing' in isl_model_name:
                        protected_fields = ['blend_ratio', 'additive_type', 'processing_role']
                    elif 'aquaculture' in isl_model_name:
                        protected_fields = ['dose_rate_ppm', 'application_method', 'water_condition']
                    elif 'crop' in isl_model_name:
                        protected_fields = ['application_rate', 'spray_volume', 'weather_condition']

                    # Check if protected fields are being modified
                    for field in protected_fields:
                        if field in vals:
                            raise UserError(_(
                                "Field '%s' is managed by the specialized ISL interface. Please modify through the %s interface."
                            ) % (field.replace('_', ' ').title(), isl_model_name.replace('farm.', '').replace('.bom.line', '').replace('.', ' ').title()))

        return super(MrpBomLine, self).write(vals)

    def unlink(self):
        # Check if any records have ISL counterparts - prevent direct deletion
        if not self.env.context.get('bypass_isl_restrictions'):
            redirector = self.env['isl.model.redirector']
            for record in self:
                isl_record = redirector.get_isl_record('mrp.bom.line', record.id)
                if isl_record:
                    raise UserError(_("Cannot directly delete base BOM line when ISL record exists. Please delete through the specialized ISL interface."))

        # Allow deletion if no ISL records exist or if bypass flag is set
        return super(MrpBomLine, self).unlink()

    # ISL navigation and indicator
    isl_record_type = fields.Char(string="ISL Record Type", compute='_compute_isl_record_type', store=False)

    def _compute_isl_record_type(self):
        """ Compute the ISL record type if one exists for BOM line """
        for record in self:
            # Use the centralized ISL redirection mechanism from farm_isl
            redirector = self.env['isl.model.redirector']
            isl_record = redirector.get_isl_record('mrp.bom.line', record.id)
            if isl_record:
                # Extract human-readable name from model name
                model_name = isl_record._name
                if 'livestock' in model_name:
                    record.isl_record_type = 'Livestock'
                elif 'processing' in model_name:
                    record.isl_record_type = 'Processing'
                elif 'aquaculture' in model_name:
                    record.isl_record_type = 'Aquaculture'
                elif 'crop' in model_name:
                    record.isl_record_type = 'Crop'
                elif 'bom.line' in model_name:
                    record.isl_record_type = model_name.replace('farm.', '').replace('.bom.line', '').replace('.', ' ').title()
                else:
                    record.isl_record_type = isl_record._name
            else:
                record.isl_record_type = False

    def action_view_isl_record(self):
        """ Action to redirect to the specialized ISL view if one exists for BOM line """
        self.ensure_one()
        # Use the centralized ISL redirection mechanism
        redirector = self.env['isl.model.redirector']
        isl_record = redirector.get_isl_record('mrp.bom.line', self.id)

        if isl_record:
            return {
                'name': _('View ISL BOM Line'),
                'type': 'ir.actions.act_window',
                'res_model': isl_record._name,
                'res_id': isl_record.id,
                'view_mode': 'form',
                'target': 'current',
            }
        # If no ISL record exists, show a message
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('No ISL Record'),
                'message': _('No specialized ISL record exists for this BOM line.'),
                'type': 'info',
                'sticky': False,
            }
        }