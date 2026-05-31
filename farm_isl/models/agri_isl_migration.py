# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
from .agri_isl_abstract_models import INDUSTRY_SELECTION

_logger = logging.getLogger(__name__)

# Data Migration & Compatibility (US-084-14)

class AgriISLMigrationUtility(models.TransientModel):
    """
    Data migration utility for ISL architecture
    Implements US-084-14: Data migration & compatibility
    """
    _name = 'agri.isl.migration.utility'
    _description = 'Agri ISL Data Migration Utility'

    industry_type = fields.Selection(
        selection=INDUSTRY_SELECTION,
        string='Industry Type', 
        default='general', 
        required=True
    )

    model_to_migrate = fields.Selection([
        ('mrp.production', 'Intervention'),
        ('mrp.bom', 'Cultivation Recipe'),
        ('mrp.workcenter', 'Facility Unit'),
        ('stock.lot', 'Stock Lot'),
        ('sale.order', 'Sale Order'),
        ('purchase.order', 'Purchase Order'),
        ('product.template', 'Product Template'),
        ('stock.picking', 'Stock Picking'),
        ('mrp.workorder', 'Operation Phase'),
    ], string='Base Model', required=True)

    confirmation = fields.Boolean('Confirm Migration')

    def action_migrate_data(self):
        """
        Migrate existing data to ISL models
        """
        if not self.confirmation:
            raise UserError(_("Please confirm the migration before proceeding"))

        base_model_name = self.model_to_migrate
        
        # 1. Get all records of the base model
        base_records = self.env[base_model_name].search([])

        # 2. Use Redirector to create ISL records (which uses Convention and Metadata)
        migrated_count = 0
        redirector = self.env['agri.isl.model.redirector']
        
        for base_record in base_records:
            # create_isl_record internally checks for existence and uses dynamic discovery
            isl_record = redirector.create_isl_record(
                base_model_name, 
                base_record.id, 
                industry_type=self.industry_type
            )
            if isl_record:
                migrated_count += 1

        message = _("Migration completed. %d records migrated to ISL architecture.") % migrated_count
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Migration Complete'),
                'message': message,
                'type': 'success'
            }
        }
