# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

# ISL Model Redirection Mechanism (US-54-11)

class ISLModelRedirector(models.AbstractModel):
    """
    ISL model redirection mechanism to automatically redirect from base models to ISL models
    Implements US-54-11: ISL model redirection mechanism
    """
    _name = 'isl.model.redirector'
    _description = 'ISL Model Redirection Utility'

    @api.model
    def get_isl_record(self, base_model_name, base_record_id):
        """
        Get the corresponding ISL record for a base record
        """
        # Map base models to their ISL counterparts
        isl_model_map = {
            'mrp.production': 'farm.mrp.production',
            'mrp.bom': 'farm.mrp.bom',
            'mrp.workcenter': 'farm.mrp.workcenter',
            'stock.lot': 'farm.stock.lot',
            'sale.order': 'farm.sale.order',
            'purchase.order': 'farm.purchase.order',
            'product.template': 'farm.product.template',
            'stock.picking': 'farm.stock.picking',
            'mrp.workorder': 'farm.mrp.workorder',
            'quality.point': 'farm.quality.control',
        }

        if base_model_name not in isl_model_map:
            return None

        isl_model_name = isl_model_map[base_model_name]

        # Search for the ISL record that inherits from the base record
        isl_record = self.env[isl_model_name].search([
            (base_model_name.replace('.', '_') + '_id', '=', base_record_id)
        ], limit=1)

        return isl_record

    @api.model
    def create_isl_record(self, base_model_name, base_record_id, industry_type='general'):
        """
        Create an ISL record for a base record if it doesn't exist
        """
        # Map base models to their ISL counterparts
        isl_model_map = {
            'mrp.production': 'farm.mrp.production',
            'mrp.bom': 'farm.mrp.bom',
            'mrp.workcenter': 'farm.mrp.workcenter',
            'stock.lot': 'farm.stock.lot',
            'sale.order': 'farm.sale.order',
            'purchase.order': 'farm.purchase.order',
            'product.template': 'farm.product.template',
            'stock.picking': 'farm.stock.picking',
            'mrp.workorder': 'farm.mrp.workorder',
            'quality.point': 'farm.quality.control',
        }

        if base_model_name not in isl_model_map:
            return None

        isl_model_name = isl_model_map[base_model_name]

        # Check if ISL record already exists
        existing_record = self.env[isl_model_name].search([
            (base_model_name.replace('.', '_') + '_id', '=', base_record_id)
        ], limit=1)

        if existing_record:
            return existing_record

        # Create new ISL record
        field_name = base_model_name.replace('.', '_') + '_id'
        isl_record = self.env[isl_model_name].create({
            field_name: base_record_id,
            'industry_type': industry_type,
        })

        return isl_record

    def _auto_redirect_to_isl(self, base_record):
        """
        Auto redirect to ISL model if available
        """
        if hasattr(base_record, '_name') and hasattr(base_record, 'id'):
            isl_record = self.get_isl_record(base_record._name, base_record.id)
            if isl_record:
                return isl_record
        return base_record


# Industry-Specific Extension Mechanism (US-54-12)

class ISLIndustryExtension(models.Model):
    """
    Model for managing industry-specific extensions
    Implements US-54-12: Industry-specific extension mechanism
    """
    _name = 'farm.isl.extension'
    _description = 'Farm ISL Extension'

    name = fields.Char('Extension Name', required=True)
    industry_type = fields.Selection([
        ('food_processing', 'Food Processing'),
        ('pharmaceutical', 'Pharmaceutical'),
        ('chemical', 'Chemical'),
        ('general', 'General Manufacturing')
    ], string='Industry Type', required=True)

    model_name = fields.Char('Model Name', required=True)
    extension_fields = fields.Text('Extension Fields (JSON)')
    extension_methods = fields.Text('Extension Methods')
    active = fields.Boolean('Active', default=True)
    description = fields.Text('Description')

    def install_extension(self):
        """Install the industry extension"""
        # This would typically involve dynamic model creation or extension
        # For now, we'll log that the extension is being installed
        _logger.info(f"Installing ISL extension: {self.name} for {self.industry_type}")

        # In a real implementation, this would dynamically add fields/methods to the target model
        # based on the extension_fields and extension_methods
        pass