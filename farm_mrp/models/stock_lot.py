# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class StockLot(models.Model):
    _inherit = 'stock.lot'

    isl_summary_info = fields.Char("ISL Contextual Info", compute='_compute_isl_summary_info')
    isl_record_type = fields.Char(string="ISL Record Type", compute='_compute_isl_record_type', store=False)

    def _compute_isl_record_type(self):
        """ Compute the ISL record type if one exists """
        for record in self:
            # Use the centralized ISL redirection mechanism from farm_isl
            redirector = self.env['agri.isl.model.redirector']
            isl_record = redirector.get_isl_record('stock.lot', record.id)
            if isl_record:
                # Extract human-readable name from model name
                model_name = isl_record._name
                if 'livestock' in model_name:
                    record.isl_record_type = 'Livestock'
                elif 'aquaculture' in model_name:
                    record.isl_record_type = 'Aquaculture'
                elif 'harvest' in model_name:
                    record.isl_record_type = 'Harvest'
                elif 'crop' in model_name:
                    record.isl_record_type = 'Crop'
                elif 'stock' in model_name:
                    record.isl_record_type = model_name.replace('farm.', '').replace('.lot', '').replace('.', ' ').title()
                else:
                    record.isl_record_type = isl_record._name
            else:
                record.isl_record_type = False

    def _compute_isl_summary_info(self):
        """ Decoupled hook for ISL summary info. """
        for lot in self:
            info_parts = lot._get_isl_summary_parts()
            lot.isl_summary_info = " | ".join(info_parts) if info_parts else ""

    def write(self, vals):
        # Check if any records have ISL counterparts and if any protected fields are being modified
        if not self.env.context.get('bypass_isl_restrictions'):
            # Use centralized ISL infrastructure to get corresponding ISL record
            redirector = self.env['agri.isl.model.redirector']

            for record in self:
                isl_record = redirector.get_isl_record('stock.lot', record.id)
                if isl_record:
                    # Check for protected fields depending on the specific ISL model type
                    protected_fields = []
                    isl_model_name = isl_record._name

                    if 'livestock' in isl_model_name:
                        protected_fields = ['birth_date', 'gender', 'current_weight']
                    elif 'aquaculture' in isl_model_name:
                        protected_fields = ['stocking_date', 'initial_count', 'current_count', 'water_volume_m3']
                    elif 'harvest' in isl_model_name:
                        protected_fields = ['plot_id', 'terroir_attributes_json']
                    elif 'crop' in isl_model_name:
                        protected_fields = ['plot_origin_id', 'terroir_json']

                    # Check if protected fields are being modified
                    for field in protected_fields:
                        if field in vals:
                            raise UserError(_(
                                "Field '%s' is managed by the specialized ISL interface. Please modify through the %s interface."
                            ) % (field.replace('_', ' ').title(), isl_model_name.replace('farm.', '').replace('.lot', '').replace('.', ' ').title()))

        return super(StockLot, self).write(vals)

    def unlink(self):
        # Check if any records have ISL counterparts - prevent direct deletion
        if not self.env.context.get('bypass_isl_restrictions'):
            redirector = self.env['agri.isl.model.redirector']
            for record in self:
                isl_record = redirector.get_isl_record('stock.lot', record.id)
                if isl_record:
                    raise UserError(_("Cannot directly delete base lot when ISL record exists. Please delete through the specialized ISL interface."))

        # Allow deletion if no ISL records exist or if bypass flag is set
        return super(StockLot, self).unlink()

    def action_view_isl_record(self):
        """ Action to redirect to the specialized ISL view if one exists """
        self.ensure_one()
        # Use the centralized ISL redirection mechanism
        redirector = self.env['agri.isl.model.redirector']
        isl_record = redirector.get_isl_record('stock.lot', self.id)

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
                'message': _('No specialized ISL record exists for this lot.'),
                'type': 'info',
                'sticky': False,
            }
        }

    def _get_isl_summary_parts(self):
        """
        Specialized modules should override this and return a list of strings.
        Example: return ["Breed: Angus", "Weight: 500kg"]
        """
        return []
