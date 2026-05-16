# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

# ISL Model Redirection Mechanism (US-084-11)

class AgriISLModelRedirector(models.AbstractModel):
    """
    ISL model redirection mechanism to automatically redirect from base models to ISL models
    Implements US-084-11: ISL model redirection mechanism
    """
    _name = 'agri.isl.model.redirector'
    _description = 'Agri ISL Model Redirection Utility'


    @api.model
    def get_isl_record(self, base_model_name, base_record_id):
        """
        Get the corresponding ISL record for a base record, with industry awareness.
        """
        if not base_record_id:
            return None
            
        base_record = self.env[base_model_name].browse(base_record_id)
        if not base_record.exists():
            return None

        # 1. Try to find specialized industry ISL models first
        industry = getattr(base_record, 'industry_type', False)
        if industry:
            # Common pattern: farm.{industry}.{base_model_suffix}
            base_suffix = base_model_name.split('.')[-1]
            # Specialized mappings for specific industries/models
            special_mappings = {
                ('aquaculture', 'production'): 'farm.ras.production',
                ('livestock', 'bom'): 'farm.livestock.bom',
                ('livestock', 'production'): 'farm.livestock.production',
                ('crop', 'production'): 'farm.crop.production',
                ('processing', 'production'): 'farm.processing.production',
            }
            
            target_model = special_mappings.get((industry, base_suffix))
            if not target_model:
                # Try generic pattern
                potential_model = f'farm.{industry}.{base_suffix}'
                if potential_model in self.env:
                    target_model = potential_model
            
            if target_model and target_model in self.env:
                # Try both naming conventions for the link field: mrp_bom_id and bom_id
                field_name_long = base_model_name.replace('.', '_') + '_id'
                field_name_short = base_model_name.split('.')[-1] + '_id'
            
                domain = []
                if field_name_long in self.env[target_model]._fields:
                    domain = [(field_name_long, '=', base_record_id)]
                elif field_name_short in self.env[target_model]._fields:
                    domain = [(field_name_short, '=', base_record_id)]
                
                if domain:
                    isl_record = self.env[target_model].search(domain, limit=1)
                    if isl_record:
                        return isl_record


        # 2. Fallback to centralized core ISL models
        isl_model_map = {
            'mrp.production': 'agri.isl.mrp.production',
            'mrp.bom': 'agri.isl.mrp.bom',
            'mrp.workcenter': 'agri.isl.mrp.workcenter',
            'stock.lot': 'agri.isl.stock.lot',
            'sale.order': 'agri.isl.sale.order',
            'purchase.order': 'agri.isl.purchase.order',
            'product.template': 'agri.isl.product.template',
            'stock.picking': 'agri.isl.stock.picking',
            'mrp.workorder': 'agri.isl.mrp.workorder',
            'quality.point': 'agri.isl.quality.control',
        }

        if base_model_name in isl_model_map:
            isl_model_name = isl_model_map[base_model_name]
            if isl_model_name in self.env:
                field_name_long = base_model_name.replace('.', '_') + '_id'
                field_name_short = base_model_name.split('.')[-1] + '_id'
            
                domain = []
                if field_name_long in self.env[isl_model_name]._fields:
                    domain = [(field_name_long, '=', base_record_id)]
                elif field_name_short in self.env[isl_model_name]._fields:
                    domain = [(field_name_short, '=', base_record_id)]

                if domain:
                    isl_record = self.env[isl_model_name].search(domain, limit=1)
                    return isl_record


        return None


    @api.model
    def create_isl_record(self, base_model_name, base_record_id, industry_type='general'):
        """
        Create an ISL record for a base record if it doesn't exist
        """
        # Map base models to their ISL counterparts
        isl_model_map = {
            'mrp.production': 'agri.isl.mrp.production',
            'mrp.bom': 'agri.isl.mrp.bom',
            'mrp.workcenter': 'agri.isl.mrp.workcenter',
            'stock.lot': 'agri.isl.stock.lot',
            'sale.order': 'agri.isl.sale.order',
            'purchase.order': 'agri.isl.purchase.order',
            'product.template': 'agri.isl.product.template',
            'stock.picking': 'agri.isl.stock.picking',
            'mrp.workorder': 'agri.isl.mrp.workorder',
            'agri.quality.point': 'agri.isl.quality.control',
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


# Industry-Specific Extension Mechanism (US-084-12)

class AgriISLIndustryExtension(models.Model):
    """
    Model for managing industry-specific extensions
    Implements US-084-12: Industry-specific extension mechanism
    """
    _name = 'agri.isl.extension'
    _description = 'Agri ISL Extension'

    name = fields.Char('Extension Name', required=True)
    industry_type = fields.Selection([
        ('field_crop', 'Field Crop'),
        ('livestock', 'Livestock'),
        ('aquaculture', 'Aquaculture'),
        ('general', 'General Agriculture'),
        ('field_crop', 'Field Crop'),
        ('livestock', 'Livestock'),
        ('aquaculture', 'Aquaculture'),
        ('general', 'General Agriculture')
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