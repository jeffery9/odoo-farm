# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    industry_type = fields.Selection([
        ('standard', 'Standard'),
        ('livestock', 'Livestock'),
        ('processing', 'Processing'),
        ('aquaculture', 'Aquaculture'),
        ('crop', 'Crop'),
    ], string="Industry Type", default='standard')

    isl_record_type = fields.Char(string="ISL Record Type", compute='_compute_isl_record_type', store=False)

    def _compute_isl_record_type(self):
        """ Compute the ISL record type if one exists """
        for record in self:
            isl_model = record._get_isl_model()
            if isl_model:
                isl_record = self.env[isl_model].search([('bom_id', '=', record.id)], limit=1)
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
                        record.isl_record_type = isl_model.replace('farm.', '').replace('.bom', '').replace('.', ' ').title()
                else:
                    record.isl_record_type = False
            else:
                record.isl_record_type = False

    def _get_isl_model(self):
        """ Hook for specialized modules to return their ISL model name. """
        return False

    @api.model_create_multi
    def create(self, vals_list):
        boms = super(MrpBom, self).create(vals_list)
        for bom in boms:
            isl_model = bom._get_isl_model()
            if isl_model:
                existing = self.env[isl_model].search([('bom_id', '=', bom.id)], limit=1)
                if not existing:
                    self.env[isl_model].create({'bom_id': bom.id})
        return boms

    def write(self, vals):
        # Check if any records have ISL counterparts and if any protected fields are being modified
        if not self.env.context.get('bypass_isl_restrictions'):
            # Identify protected fields that should only be modified through ISL
            protected_fields = {
                'farm.livestock.bom': ['growth_days_expected', 'daily_feed_intake'],
                'farm.processing.bom': ['is_parameter_required', 'target_temp', 'target_ph', 'target_brix', 'target_proofing_time', 'standard_duration', 'haccp_instructions'],
                'farm.aquaculture.bom': ['pond_type', 'target_dissolved_oxygen', 'target_ph_range', 'stocking_density_limit'],
                'farm.crop.bom': ['growing_season', 'phi_days']
            }

            for record in self:
                isl_model = record._get_isl_model()
                if isl_model and isl_model in protected_fields:
                    isl_record = self.env[isl_model].search([('bom_id', '=', record.id)], limit=1)
                    if isl_record:
                        # Check if protected fields are being modified
                        for field in protected_fields[isl_model]:
                            if field in vals:
                                raise UserError(_(
                                    "Field '%s' is managed by the specialized ISL interface. Please modify through the %s interface."
                                ) % (field.replace('_', ' ').title(), isl_model.replace('farm.', '').replace('.bom', '').replace('.', ' ').title()))

        return super(MrpBom, self).write(vals)

    def unlink(self):
        # Check if any records have ISL counterparts - prevent direct deletion
        if not self.env.context.get('bypass_isl_restrictions'):
            for record in self:
                isl_model = record._get_isl_model()
                if isl_model:
                    isl_record = self.env[isl_model].search([('bom_id', '=', record.id)], limit=1)
                    if isl_record:
                        raise UserError(_("Cannot directly delete base BOM when ISL record exists. Please delete through the specialized ISL interface."))

        # Allow deletion if no ISL records exist or if bypass flag is set
        return super(MrpBom, self).unlink()

    def get_formview_action(self, access_uid=None):
        """ US-TECH-06-19: Redirect to ISL-specialized view if available. """
        res = super(MrpBom, self).get_formview_action(access_uid=access_uid)
        isl_model = self._get_isl_model()
        if isl_model:
            isl_record = self.env[isl_model].search([('bom_id', '=', self.id)], limit=1)
            if isl_record:
                res.update({
                    'res_model': isl_model,
                    'res_id': isl_record.id,
                    'context': dict(self.env.context, isl_active=True)
                })
        return res

    def action_view_isl_record(self):
        """ Action to redirect to the specialized ISL view if one exists """
        self.ensure_one()
        isl_model = self._get_isl_model()
        if isl_model:
            isl_record = self.env[isl_model].search([('bom_id', '=', self.id)], limit=1)
            if isl_record:
                return {
                    'name': _('View ISL Record'),
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
                'message': _('No specialized ISL record exists for this BOM.'),
                'type': 'info',
                'sticky': False,
            }
        }
