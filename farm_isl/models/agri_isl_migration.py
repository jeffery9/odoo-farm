# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

# Data Migration & Compatibility (US-54-14)

class AgriISLMigrationUtility(models.TransientModel):
    """
    Data migration utility for ISL architecture
    Implements US-54-14: Data migration & compatibility
    """
    _name = 'agri.isl.migration.utility'
    _description = 'Agri ISL Data Migration Utility'

    industry_type = fields.Selection([
        ('food_processing', 'Food Processing'),
        ('pharmaceutical', 'Pharmaceutical'),
        ('chemical', 'Chemical'),
        ('general', 'General Manufacturing')
    ], string='Industry Type', default='general', required=True)

    model_to_migrate = fields.Selection([
        ('mrp.production', 'MRP Production'),
        ('mrp.bom', 'MRP BOM'),
        ('mrp.workcenter', 'MRP Work Center'),
        ('stock.lot', 'Stock Lot'),
        ('sale.order', 'Sale Order'),
        ('purchase.order', 'Purchase Order'),
        ('product.template', 'Product Template'),
        ('stock.picking', 'Stock Picking'),
        ('mrp.workorder', 'MRP Work Order'),
        ('quality.point', 'Quality Point'),
    ], string='Model to Migrate', required=True)

    confirmation = fields.Boolean('Confirm Migration')

    def action_migrate_data(self):
        """
        Migrate existing data to ISL models
        """
        if not self.confirmation:
            raise UserError(_("Please confirm the migration before proceeding"))

        base_model_name = self.model_to_migrate
        isl_model_name_map = {
            'mrp.production': 'agri.mrp.production',
            'mrp.bom': 'agri.mrp.bom',
            'mrp.workcenter': 'agri.mrp.workcenter',
            'stock.lot': 'agri.stock.lot',
            'sale.order': 'agri.sale.order',
            'purchase.order': 'agri.purchase.order',
            'product.template': 'agri.product.template',
            'stock.picking': 'agri.stock.picking',
            'mrp.workorder': 'agri.mrp.workorder',
            'quality.point': 'agri.quality.control',
        }

        if base_model_name not in isl_model_name_map:
            raise UserError(_("Unsupported model for migration"))

        isl_model_name = isl_model_name_map[base_model_name]

        # Get all records of the base model
        base_records = self.env[base_model_name].search([])

        # Create ISL records for each base record
        migrated_count = 0
        for base_record in base_records:
            # Check if ISL record already exists
            existing_isl = self.env['agri.isl.model.redirector'].get_isl_record(
                base_model_name, base_record.id
            )

            if not existing_isl:
                field_name = base_model_name.replace('.', '_') + '_id'
                self.env[isl_model_name].create({
                    field_name: base_record.id,
                    'industry_type': self.industry_type,
                })
                migrated_count += 1

        message = _("Migration completed. %d records migrated to ISL architecture.", migrated_count)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Migration Complete'),
                'message': message,
                'type': 'success'
            }
        }