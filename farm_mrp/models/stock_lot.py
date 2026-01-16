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
            # Check each possible ISL model for this lot
            isl_models = ['farm.lot.livestock', 'farm.lot.aquaculture', 'farm.lot.harvest', 'farm.crop.lot']
            found_isl = False
            for isl_model in isl_models:
                isl_record = self.env[isl_model].search([('lot_id', '=', record.id)], limit=1)
                if isl_record:
                    # Extract human-readable name from model name
                    if 'livestock' in isl_model:
                        record.isl_record_type = 'Livestock'
                    elif 'aquaculture' in isl_model:
                        record.isl_record_type = 'Aquaculture'
                    elif 'harvest' in isl_model:
                        record.isl_record_type = 'Harvest'
                    elif 'crop' in isl_model:
                        record.isl_record_type = 'Crop'
                    else:
                        record.isl_record_type = isl_model.replace('farm.', '').replace('.lot', '').replace('.', ' ').title()
                    found_isl = True
                    break
            if not found_isl:
                record.isl_record_type = False

    def _compute_isl_summary_info(self):
        """ Decoupled hook for ISL summary info. """
        for lot in self:
            info_parts = lot._get_isl_summary_parts()
            lot.isl_summary_info = " | ".join(info_parts) if info_parts else ""

    def write(self, vals):
        # Check if any records have ISL counterparts and if any protected fields are being modified
        if not self.env.context.get('bypass_isl_restrictions'):
            # Identify protected fields that should only be modified through ISL
            protected_fields = {
                'farm.lot.livestock': ['birth_date', 'gender', 'current_weight'],
                'farm.lot.aquaculture': ['stocking_date', 'initial_count', 'current_count', 'water_volume_m3'],
                'farm.lot.harvest': ['plot_id', 'terroir_attributes_json'],
                'farm.crop.lot': ['plot_origin_id', 'terroir_json']
            }

            for record in self:
                # Check if any ISL model is linked to this lot
                for isl_model, fields_list in protected_fields.items():
                    isl_record = self.env[isl_model].search([('lot_id', '=', record.id)], limit=1)
                    if isl_record:
                        # Check if protected fields are being modified
                        for field in fields_list:
                            if field in vals:
                                raise UserError(_(
                                    "Field '%s' is managed by the specialized ISL interface. Please modify through the %s interface."
                                ) % (field.replace('_', ' ').title(), isl_model.replace('farm.', '').replace('.lot', '').replace('.', ' ').title()))

        return super(StockLot, self).write(vals)

    def unlink(self):
        # Check if any records have ISL counterparts - prevent direct deletion
        if not self.env.context.get('bypass_isl_restrictions'):
            for record in self:
                # Check any ISL models linked to this lot
                isl_models = ['farm.lot.livestock', 'farm.lot.aquaculture', 'farm.lot.harvest', 'farm.crop.lot']
                for isl_model in isl_models:
                    isl_record = self.env[isl_model].search([('lot_id', '=', record.id)], limit=1)
                    if isl_record:
                        raise UserError(_("Cannot directly delete base lot when ISL record exists. Please delete through the specialized ISL interface."))

        # Allow deletion if no ISL records exist or if bypass flag is set
        return super(StockLot, self).unlink()

    def action_view_isl_record(self):
        """ Action to redirect to the specialized ISL view if one exists """
        self.ensure_one()
        # Check each possible ISL model for this lot
        isl_models = ['farm.lot.livestock', 'farm.lot.aquaculture', 'farm.lot.harvest', 'farm.crop.lot']

        for isl_model in isl_models:
            isl_record = self.env[isl_model].search([('lot_id', '=', self.id)], limit=1)
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
