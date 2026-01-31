# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    industry_type = fields.Selection(related='bom_id.industry_type', string="Industry Standard", store=True, readonly=True)
    isl_record_type = fields.Char(string="ISL Record Type", compute='_compute_isl_record_type', store=False)

    def _compute_isl_record_type(self):
        """ Compute the ISL record type if one exists """
        for record in self:
            # Use the centralized ISL redirection mechanism from farm_isl
            redirector = self.env['agri.isl.model.redirector']
            isl_record = redirector.get_isl_record('mrp.production', record.id)
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
                    record.isl_record_type = model_name.replace('agri.', '').replace('.production', '').replace('.', ' ').title()
                else:
                    record.isl_record_type = isl_record._name
            else:
                record.isl_record_type = False

    def _get_isl_model(self):
        """
        Hook for specialized modules to return their ISL model name.
        Each module should inherit this and return its specific model.
        """
        return False

    @api.model_create_multi
    def create(self, vals_list):
        orders = super(MrpProduction, self).create(vals_list)
        for order in orders:
            # Use farm_isl's redirection mechanism
            redirector = self.env['agri.isl.model.redirector']
            # The ISL record will be automatically created by the ISL redirection utility
            # if the industry_type is specified
            if order.bom_id and hasattr(order.bom_id, 'industry_type') and order.bom_id.industry_type:
                isl_record = redirector.create_isl_record('mrp.production', order.id, order.bom_id.industry_type)
        return orders

    def get_formview_action(self, access_uid=None):
        """ US-TECH-06-19: Transparently redirect to ISL view if available. """
        # Use the centralized ISL redirection mechanism from farm_isl
        redirector = self.env['agri.isl.model.redirector']
        isl_record = redirector.get_isl_record('mrp.production', self.id)

        if isl_record:
            return {
                'type': 'ir.actions.act_window',
                'res_model': isl_record._name,
                'res_id': isl_record.id,
                'view_mode': 'form',
                'context': dict(self.env.context, isl_active=True)
            }
        # If no ISL record exists, use the default behavior
        return super(MrpProduction, self).get_formview_action(access_uid=access_uid)

    def action_confirm(self):
        res = super(MrpProduction, self).action_confirm()
        for order in self:
            self._trigger_isl_hook('isl_post_confirm', order.id)
        return res

    def button_mark_done(self):
        res = super(MrpProduction, self).button_mark_done()
        for order in self:
            self._trigger_isl_hook('isl_post_done', order.id)
        return res

    def write(self, vals):
        # Check if any records have ISL counterparts and if any protected fields are being modified
        if not self.env.context.get('bypass_isl_restrictions'):
            # Use centralized ISL infrastructure to get corresponding ISL record
            redirector = self.env['agri.isl.model.redirector']

            for record in self:
                isl_record = redirector.get_isl_record('mrp.production', record.id)
                if isl_record:
                    # Check for protected fields depending on the specific ISL model type
                    protected_fields = []
                    isl_model_name = isl_record._name

                    if 'livestock' in isl_model_name:
                        protected_fields = ['initial_total_weight', 'final_total_weight', 'fcr']
                    elif 'processing' in isl_model_name:
                        protected_fields = ['energy_reading_start', 'energy_reading_end', 'energy_cost_total']
                    elif 'aquaculture' in isl_model_name:
                        protected_fields = ['water_temp', 'dissolved_oxygen', 'ph_level', 'avg_individual_weight', 'survival_rate']
                    elif 'crop' in isl_model_name:
                        protected_fields = ['area_to_treat']

                    # Check if protected fields are being modified
                    for field in protected_fields:
                        if field in vals:
                            raise UserError(_(
                                "Field '%s' is managed by the specialized ISL interface. Please modify through the %s interface."
                            ) % (field.replace('_', ' ').title(), isl_model_name.replace('agri.', '').replace('.production', '').replace('.', ' ').title()))

        return super(MrpProduction, self).write(vals)

    def unlink(self):
        # Check if any records have ISL counterparts - prevent direct deletion
        if not self.env.context.get('bypass_isl_restrictions'):
            redirector = self.env['agri.isl.model.redirector']
            for record in self:
                isl_record = redirector.get_isl_record('mrp.production', record.id)
                if isl_record:
                    raise UserError(_("Cannot directly delete base production order when ISL record exists. Please delete through the specialized ISL interface."))

        # Allow deletion if no ISL records exist or if bypass flag is set
        return super(MrpProduction, self).unlink()

    def _trigger_isl_hook(self, hook_name, base_id):
        """ Helper to route events to ISL sub-models. """
        redirector = self.env['agri.isl.model.redirector']
        isl_rec = redirector.get_isl_record('mrp.production', base_id)
        if isl_rec and hasattr(isl_rec, hook_name):
            getattr(isl_rec, hook_name)()

    def action_view_isl_record(self):
        """ Action to redirect to the specialized ISL view if one exists """
        self.ensure_one()
        # Use the centralized ISL redirection mechanism
        redirector = self.env['agri.isl.model.redirector']
        isl_record = redirector.get_isl_record('mrp.production', self.id)

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
                'message': _('No specialized ISL record exists for this production order.'),
                'type': 'info',
                'sticky': False,
            }
        }
