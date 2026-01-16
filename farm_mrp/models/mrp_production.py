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
            isl_model = record._get_isl_model()
            if isl_model:
                isl_record = self.env[isl_model].search([('production_id', '=', record.id)], limit=1)
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
                        record.isl_record_type = isl_model.replace('farm.', '').replace('.production', '').replace('.', ' ').title()
                else:
                    record.isl_record_type = False
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
            isl_model = order._get_isl_model()
            if isl_model:
                # Check if ISL record already exists (to avoid duplicates if created from ISL side)
                existing = self.env[isl_model].search([('production_id', '=', order.id)], limit=1)
                if not existing:
                    self.env[isl_model].create({'production_id': order.id})
        return orders

    def get_formview_action(self, access_uid=None):
        """ US-TECH-06-19: Transparently redirect to ISL view if available. """
        res = super(MrpProduction, self).get_formview_action(access_uid=access_uid)
        isl_model = self._get_isl_model()
        if isl_model:
            isl_record = self.env[isl_model].search([('production_id', '=', self.id)], limit=1)
            if isl_record:
                res.update({
                    'res_model': isl_model, 
                    'res_id': isl_record.id,
                    'context': dict(self.env.context, isl_active=True)
                })
        return res

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
            # Identify protected fields that should only be modified through ISL
            protected_fields = {
                'farm.livestock.production': ['initial_total_weight', 'final_total_weight', 'fcr'],
                'farm.processing.production': ['energy_reading_start', 'energy_reading_end', 'energy_cost_total'],
                'farm.aquaculture.production': ['water_temp', 'dissolved_oxygen', 'ph_level', 'avg_individual_weight', 'survival_rate'],
                'farm.crop.production': ['area_to_treat']
            }

            for record in self:
                isl_model = record._get_isl_model()
                if isl_model and isl_model in protected_fields:
                    isl_record = self.env[isl_model].search([('production_id', '=', record.id)], limit=1)
                    if isl_record:
                        # Check if protected fields are being modified
                        for field in protected_fields[isl_model]:
                            if field in vals:
                                raise UserError(_(
                                    "Field '%s' is managed by the specialized ISL interface. Please modify through the %s interface."
                                ) % (field.replace('_', ' ').title(), isl_model.replace('farm.', '').replace('.production', '').replace('.', ' ').title()))

        return super(MrpProduction, self).write(vals)

    def unlink(self):
        # Check if any records have ISL counterparts - prevent direct deletion
        if not self.env.context.get('bypass_isl_restrictions'):
            for record in self:
                isl_model = record._get_isl_model()
                if isl_model:
                    isl_record = self.env[isl_model].search([('production_id', '=', record.id)], limit=1)
                    if isl_record:
                        raise UserError(_("Cannot directly delete base production order when ISL record exists. Please delete through the specialized ISL interface."))

        # Allow deletion if no ISL records exist or if bypass flag is set
        return super(MrpProduction, self).unlink()

    def _trigger_isl_hook(self, hook_name, base_id):
        """ Helper to route events to ISL sub-models. """
        isl_model = self._get_isl_model()
        if isl_model:
            isl_rec = self.env[isl_model].search([('production_id', '=', base_id)], limit=1)
            if isl_rec and hasattr(isl_rec, hook_name):
                getattr(isl_rec, hook_name)()

    def action_view_isl_record(self):
        """ Action to redirect to the specialized ISL view if one exists """
        self.ensure_one()
        isl_model = self._get_isl_model()
        if isl_model:
            isl_record = self.env[isl_model].search([('production_id', '=', self.id)], limit=1)
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
                'message': _('No specialized ISL record exists for this production order.'),
                'type': 'info',
                'sticky': False,
            }
        }
