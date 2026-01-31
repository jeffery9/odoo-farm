# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

# Performance Optimization & Caching (US-54-13)

class AgriISLOptimizationMixin(models.AbstractModel):
    """
    Performance optimization and caching for ISL architecture
    Implements US-54-13: Performance optimization & caching
    """
    _name = 'agri.isl.optimization.mixin'
    _description = 'Agri ISL Optimization Mixin'

    # Add methods for performance optimization
    @api.model
    def _get_cached_isl_record(self, base_model_name, base_record_id):
        """
        Get ISL record with caching to improve performance
        """
        cache_key = f"isl_{base_model_name}_{base_record_id}"
        # In production, this would use proper caching (Redis, etc.)
        # For now, we'll simulate with a simple approach
        cached_record = self.env.context.get(cache_key)

        if cached_record:
            return cached_record

        isl_record = self.env['agri.isl.model.redirector'].get_isl_record(
            base_model_name, base_record_id
        )

        # Add to context for this request
        context = self.env.context.copy()
        context[cache_key] = isl_record
        self.env.context = context

        return isl_record

    def _clear_isl_cache(self, base_model_name, base_record_ids):
        """
        Clear cache for specific records
        """
        # In production, this would clear the actual cache
        # For now, we'll just log the action
        _logger.info(f"Clearing ISL cache for {base_model_name}: {base_record_ids}")