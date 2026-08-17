# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
from .agri_isl_abstract_models import INDUSTRY_SELECTION

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
        [SOLID Refactored & Cached] Get the corresponding ISL record for a base record.
        Uses Odoo delegation inheritance metadata (_inherits) with registry lookup cache mapping.
        """
        if not base_record_id:
            return None
            
        base_record = self.env[base_model_name].browse(base_record_id)
        if not base_record.exists():
            return None

        industry = getattr(base_record, 'industry_type', False)
        
        # 1. Access Registry-Bound Lookup Cache to replace O(N) scanning
        registry = self.env.registry
        if not hasattr(registry, '_isl_inherits_cache'):
            registry._isl_inherits_cache = {}
            
        cache = registry._isl_inherits_cache
        if base_model_name not in cache:
            # Recompile/populate candidate list once for base_model_name
            candidates = []
            for model_name, model_obj in registry.items():
                inherits = getattr(model_obj, '_inherits', {})
                if base_model_name in inherits:
                    candidates.append((model_name, inherits[base_model_name]))
            cache[base_model_name] = candidates

        # 2. Iterate only over cached candidates of base_model_name
        for model_name, link_field in cache[base_model_name]:
            if model_name not in self.env:
                continue
            domain = [(link_field, '=', base_record_id)]
            isl_record = self.env[model_name].search(domain, limit=1)
            
            if isl_record:
                if industry and hasattr(isl_record, 'industry_type'):
                    if isl_record.industry_type == industry:
                        return isl_record
                else:
                    return isl_record

        return None


    @api.model
    def create_isl_record(self, base_model_name, base_record_id, industry_type='general'):
        """
        [SOLID Refactored] Create an ISL record for a base record if it doesn't exist.
        Uses metadata discovery and Naming Conventions instead of hardcoded mappings.
        """
        # Sanitize and validate industry_type
        valid_industries = ['field_crop', 'livestock', 'aquaculture', 'general']
        if industry_type not in valid_industries:
            industry_type = 'general'

        if not base_model_name or not base_record_id:
            return None

        target_model = False
        link_field = False
        
        # 1. Strategy: Industry-Specific Discovery (Convention: agri.isl.{industry}.{suffix})
        for model_name, model_obj in self.env.registry.items():
            inherits = getattr(model_obj, '_inherits', {})
            if base_model_name in inherits:
                # Priority match: Name includes industry identifier
                if f".{industry_type}." in model_name or f"_{industry_type}_" in model_name:
                    target_model = model_name
                    link_field = inherits[base_model_name]
                    break
        
        # 2. Strategy: Generic Discovery (Convention: agri.isl.{suffix_without_dots})
        if not target_model:
            potential_generic = f"agri.isl.{base_model_name}"
            if potential_generic in self.env:
                target_model = potential_generic
                link_field = self.env[target_model]._inherits[base_model_name]
            else:
                # Fallback to underscores if dots not found
                suffix = base_model_name.replace('.', '_')
                potential_generic_us = f"agri.isl.{suffix}"
                if potential_generic_us in self.env:
                    target_model = potential_generic_us
                    link_field = self.env[target_model]._inherits[base_model_name]

        if not target_model:
            return None

        # 3. Check if ISL record already exists
        existing_record = self.env[target_model].search([
            (link_field, '=', base_record_id)
        ], limit=1)

        if existing_record:
            return existing_record

        # 4. Create new ISL record
        isl_record = self.env[target_model].create({
            link_field: base_record_id,
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
    industry_type = fields.Selection(
        selection=INDUSTRY_SELECTION,
        string='Industry Type', 
        required=True
    )

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