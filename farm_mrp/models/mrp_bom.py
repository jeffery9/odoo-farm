# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    industry_type = fields.Selection(selection=[
        ('food_processing', 'Food Processing'),
        ('pharmaceutical', 'Pharmaceutical'),
        ('chemical', 'Chemical'),
        ('general', 'General Manufacturing'),
        ('standard', 'Standard'),
        ('livestock', 'Livestock'),
        ('processing', 'Processing'),
        ('aquaculture', 'Aquaculture'),
        ('crop', 'Crop'),
        ('pharma', 'Pharmaceutical'),
        ('chemical', 'Chemical'),
    ], string="Industry Type", default='standard')

    isl_record_type = fields.Char(string="ISL Record Type", compute='_compute_isl_record_type', store=False)

    def _compute_isl_record_type(self):
        """ Compute the ISL record type if one exists """
        for record in self:
            # Use the centralized ISL redirection mechanism from farm_isl
            redirector = self.env['isl.model.redirector']
            isl_record = redirector.get_isl_record('mrp.bom', record.id)
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
                elif 'mrp' in model_name:
                    record.isl_record_type = model_name.replace('farm.', '').replace('.bom', '').replace('.', ' ').title()
                else:
                    record.isl_record_type = isl_record._name
            else:
                record.isl_record_type = False

    def _get_isl_model(self):
        """ Hook for specialized modules to return their ISL model name. """
        return False

    @api.model_create_multi
    def create(self, vals_list):
        boms = super(MrpBom, self).create(vals_list)
        for bom in boms:
            # Use farm_isl's redirection mechanism
            redirector = self.env['isl.model.redirector']
            # The ISL record will be automatically created by the ISL redirection utility
            # if the industry_type is specified
            if bom.industry_type and bom.industry_type != 'standard':
                isl_record = redirector.create_isl_record('mrp.bom', bom.id, bom.industry_type)
        return boms

    def write(self, vals):
        # Check if any records have ISL counterparts and if any protected fields are being modified
        if not self.env.context.get('bypass_isl_restrictions'):
            # Use centralized ISL infrastructure to get corresponding ISL record
            redirector = self.env['isl.model.redirector']

            for record in self:
                isl_record = redirector.get_isl_record('mrp.bom', record.id)
                if isl_record:
                    # Check for protected fields depending on the specific ISL model type
                    protected_fields = []
                    isl_model_name = isl_record._name

                    if 'livestock' in isl_model_name:
                        protected_fields = ['growth_days_expected', 'daily_feed_intake']
                    elif 'processing' in isl_model_name:
                        protected_fields = ['is_parameter_required', 'target_temp', 'target_ph', 'target_brix', 'target_proofing_time', 'standard_duration', 'haccp_instructions']
                    elif 'aquaculture' in isl_model_name:
                        protected_fields = ['pond_type', 'target_dissolved_oxygen', 'target_ph_range', 'stocking_density_limit']
                    elif 'crop' in isl_model_name:
                        protected_fields = ['growing_season', 'phi_days']

                    # Check if protected fields are being modified
                    for field in protected_fields:
                        if field in vals:
                            raise UserError(_(
                                "Field '%s' is managed by the specialized ISL interface. Please modify through the %s interface."
                            ) % (field.replace('_', ' ').title(), isl_model_name.replace('farm.', '').replace('.bom', '').replace('.', ' ').title()))

        return super(MrpBom, self).write(vals)

    def unlink(self):
        # Check if any records have ISL counterparts - prevent direct deletion
        if not self.env.context.get('bypass_isl_restrictions'):
            redirector = self.env['isl.model.redirector']
            for record in self:
                isl_record = redirector.get_isl_record('mrp.bom', record.id)
                if isl_record:
                    raise UserError(_("Cannot directly delete base BOM when ISL record exists. Please delete through the specialized ISL interface."))

        # Allow deletion if no ISL records exist or if bypass flag is set
        return super(MrpBom, self).unlink()

    def get_formview_action(self, access_uid=None):
        """ US-TECH-06-19: Redirect to ISL-specialized view if available. """
        # Use the centralized ISL redirection mechanism from farm_isl
        redirector = self.env['isl.model.redirector']
        isl_record = redirector.get_isl_record('mrp.bom', self.id)

        if isl_record:
            return {
                'type': 'ir.actions.act_window',
                'res_model': isl_record._name,
                'res_id': isl_record.id,
                'view_mode': 'form',
                'context': dict(self.env.context, isl_active=True)
            }
        # If no ISL record exists, use the default behavior
        return super(MrpBom, self).get_formview_action(access_uid=access_uid)

    def action_view_isl_record(self):
        """ Action to redirect to the specialized ISL view if one exists """
        self.ensure_one()
        # Use the centralized ISL redirection mechanism
        redirector = self.env['isl.model.redirector']
        isl_record = redirector.get_isl_record('mrp.bom', self.id)

        if isl_record:
            return {
                'name': _('View ISL Record'),
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
                'message': _('No specialized ISL record exists for this BOM.'),
                'type': 'info',
                'sticky': False,
            }
        }
