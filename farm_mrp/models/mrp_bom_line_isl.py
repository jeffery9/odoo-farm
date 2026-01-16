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
            isl_model = line._get_isl_model()
            if isl_model:
                # Check if ISL record already exists (to avoid duplicates if created from ISL side)
                existing = self.env[isl_model].search([('bom_line_id', '=', line.id)], limit=1)
                if not existing:
                    self.env[isl_model].create({'bom_line_id': line.id})
        return lines

    def get_formview_action(self, access_uid=None):
        """ Transparently redirect to ISL view if available for BOM line. """
        res = super(MrpBomLine, self).get_formview_action(access_uid=access_uid)
        isl_model = self._get_isl_model()
        if isl_model:
            isl_record = self.env[isl_model].search([('bom_line_id', '=', self.id)], limit=1)
            if isl_record:
                res.update({
                    'res_model': isl_model,
                    'res_id': isl_record.id,
                    'context': dict(self.env.context, isl_active=True)
                })
        return res

    def write(self, vals):
        # Check if any records have ISL counterparts and if any protected fields are being modified
        if not self.env.context.get('bypass_isl_restrictions'):
            # Identify protected fields that should only be modified through ISL
            protected_fields = {
                'farm.livestock.bom.line': ['dilution_ratio', 'feeding_ratio', 'feed_purpose'],
                'farm.processing.bom.line': ['blend_ratio', 'additive_type', 'processing_role'],
                'farm.aquaculture.bom.line': ['dose_rate_ppm', 'application_method', 'water_condition'],
                'farm.crop.bom.line': ['application_rate', 'spray_volume', 'weather_condition']
            }

            for record in self:
                isl_model = record._get_isl_model()
                if isl_model and isl_model in protected_fields:
                    isl_record = self.env[isl_model].search([('bom_line_id', '=', record.id)], limit=1)
                    if isl_record:
                        # Check if protected fields are being modified
                        for field in protected_fields[isl_model]:
                            if field in vals:
                                raise UserError(_(
                                    "Field '%s' is managed by the specialized ISL interface. Please modify through the %s interface."
                                ) % (field.replace('_', ' ').title(), isl_model.replace('farm.', '').replace('.bom.line', '').replace('.', ' ').title()))

        return super(MrpBomLine, self).write(vals)

    def unlink(self):
        # Check if any records have ISL counterparts - prevent direct deletion
        if not self.env.context.get('bypass_isl_restrictions'):
            for record in self:
                isl_model = record._get_isl_model()
                if isl_model:
                    isl_record = self.env[isl_model].search([('bom_line_id', '=', record.id)], limit=1)
                    if isl_record:
                        raise UserError(_("Cannot directly delete base BOM line when ISL record exists. Please delete through the specialized ISL interface."))

        # Allow deletion if no ISL records exist or if bypass flag is set
        return super(MrpBomLine, self).unlink()

    # ISL navigation and indicator
    isl_record_type = fields.Char(string="ISL Record Type", compute='_compute_isl_record_type', store=False)

    def _compute_isl_record_type(self):
        """ Compute the ISL record type if one exists for BOM line """
        for record in self:
            isl_model = record._get_isl_model()
            if isl_model:
                isl_record = self.env[isl_model].search([('bom_line_id', '=', record.id)], limit=1)
                if isl_record:
                    # Extract human-readable name from model name
                    if 'livestock' in isl_model:
                        record.isl_record_type = 'Livestock'
                    elif 'processing' in isl_model:
                        record.isl_record_type = 'Processing'
                    elif 'aquaculture' in isl_model:
                        record.isl_record_type = 'Aquaculture'
                    elif 'crop' in isl_model:
                        record.isl_record_type = 'Crop'
                    else:
                        record.isl_record_type = isl_model.replace('farm.', '').replace('.bom.line', '').replace('.', ' ').title()
                else:
                    record.isl_record_type = False
            else:
                record.isl_record_type = False

    def action_view_isl_record(self):
        """ Action to redirect to the specialized ISL view if one exists for BOM line """
        self.ensure_one()
        isl_model = self._get_isl_model()
        if isl_model:
            isl_record = self.env[isl_model].search([('bom_line_id', '=', self.id)], limit=1)
            if isl_record:
                return {
                    'name': _('View ISL BOM Line'),
                    'type': 'ir.actions.act_window',
                    'res_model': isl_model,
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