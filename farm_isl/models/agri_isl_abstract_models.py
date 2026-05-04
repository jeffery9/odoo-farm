# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

# Abstract Base Models for ISL Architecture (US-084-01 through US-084-10)

class AgriManufacturingMixin(models.AbstractModel):
    """
    Abstract base model for manufacturing-related ISL models
    Implements US-084-01, US-084-02, US-084-03, US-084-09
    """
    _name = 'agri.manufacturing.mixin'
    _description = 'Agri Manufacturing ISL Abstract Base Model'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Common fields that all manufacturing ISL models will inherit
    industry_type = fields.Selection([
        ('food_processing', 'Food Processing'),
        ('pharmaceutical', 'Pharmaceutical'),
        ('chemical', 'Chemical'),
        ('general', 'General Manufacturing')
    ], string='Industry Type', default='general', required=True, ondelete={'food_processing': 'cascade', 'pharmaceutical': 'cascade', 'chemical': 'cascade', 'general': 'cascade'})

    industry_specialization = fields.Char('Industry Specialization')
    compliance_requirements = fields.Text('Compliance Requirements')
    industry_standards = fields.Char('Industry Standards')
    safety_requirements = fields.Text('Safety Requirements')
    quality_control_points = fields.Text('Quality Control Points')

    # Industry-specific computed fields
    industry_notes = fields.Html('Industry Notes')
    industry_attachments = fields.Binary('Industry Attachments')

    # Track if this is an ISL model instance
    is_isl_model = fields.Boolean('Is ISL Model', default=True, readonly=True)

    def _get_industry_specific_fields(self):
        """Return fields specific to the industry type"""
        return {
            'food_processing': ['quality_control_points', 'compliance_requirements', 'safety_requirements'],
            'pharmaceutical': ['quality_control_points', 'compliance_requirements', 'industry_standards'],
            'chemical': ['safety_requirements', 'compliance_requirements', 'industry_standards'],
            'general': [],
        }

    def _validate_industry_requirements(self):
        """Validate that industry-specific requirements are met"""
        if self.industry_type == 'food_processing':
            if not self.quality_control_points:
                raise UserError(_("Food processing industry requires quality control points to be defined"))
        elif self.industry_type == 'pharmaceutical':
            if not self.industry_standards:
                raise UserError(_("Pharmaceutical industry requires industry standards to be defined"))
        return True


class AgriInventoryMixin(models.AbstractModel):
    """
    Abstract base model for inventory-related ISL models
    Implements US-084-04, US-084-08
    """
    _name = 'agri.inventory.mixin'
    _description = 'Agri Inventory ISL Abstract Base Model'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Common fields for inventory ISL models
    industry_type = fields.Selection([
        ('food_processing', 'Food Processing'),
        ('pharmaceutical', 'Pharmaceutical'),
        ('chemical', 'Chemical'),
        ('general', 'General Manufacturing')
    ], string='Industry Type', default='general', required=True, ondelete={'food_processing': 'cascade', 'pharmaceutical': 'cascade', 'chemical': 'cascade', 'general': 'cascade'})

    shelf_life_tracking = fields.Boolean('Shelf Life Tracking', default=False)
    batch_tracking = fields.Boolean('Batch Tracking', default=True)
    lot_tracking = fields.Boolean('Lot Tracking', default=True)
    expiry_tracking = fields.Boolean('Expiry Tracking', default=False)

    # Industry-specific inventory requirements
    inventory_compliance = fields.Text('Inventory Compliance')
    storage_requirements = fields.Text('Storage Requirements')
    temperature_control = fields.Boolean('Temperature Control', default=False)
    humidity_control = fields.Boolean('Humidity Control', default=False)
    light_sensitive = fields.Boolean('Light Sensitive', default=False)

    # Track if this is an ISL model instance
    is_isl_model = fields.Boolean('Is ISL Model', default=True, readonly=True)


class AgriSalesPurchaseMixin(models.AbstractModel):
    """
    Abstract base model for sales/purchase-related ISL models
    Implements US-084-05, US-084-06
    """
    _name = 'agri.sales.purchase.mixin'
    _description = 'Agri Sales/Purchase ISL Abstract Base Model'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Common fields for sales/purchase ISL models
    industry_type = fields.Selection([
        ('food_processing', 'Food Processing'),
        ('pharmaceutical', 'Pharmaceutical'),
        ('chemical', 'Chemical'),
        ('general', 'General Manufacturing')
    ], string='Industry Type', default='general', required=True, ondelete={'food_processing': 'cascade', 'pharmaceutical': 'cascade', 'chemical': 'cascade', 'general': 'cascade'})

    industry_certification = fields.Char('Industry Certification')
    compliance_requirements = fields.Text('Compliance Requirements')

    # Industry-specific requirements
    sales_compliance = fields.Text('Sales Compliance')
    purchase_compliance = fields.Text('Purchase Compliance')
    quality_assurance = fields.Boolean('Quality Assurance', default=False)

    # Track if this is an ISL model instance
    is_isl_model = fields.Boolean('Is ISL Model', default=True, readonly=True)


class AgriProductMixin(models.AbstractModel):
    """
    Abstract base model for product-related ISL models
    Implements US-084-07
    """
    _name = 'agri.product.mixin'
    _description = 'Agri Product ISL Abstract Base Model'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Common fields for product ISL models
    industry_type = fields.Selection([
        ('food_processing', 'Food Processing'),
        ('pharmaceutical', 'Pharmaceutical'),
        ('chemical', 'Chemical'),
        ('general', 'General Manufacturing')
    ], string='Industry Type', default='general', required=True, ondelete={'food_processing': 'cascade', 'pharmaceutical': 'cascade', 'chemical': 'cascade', 'general': 'cascade'})

    industry_category = fields.Char('Industry Category')
    safety_data_sheet = fields.Binary('Safety Data Sheet')
    safety_data_sheet_name = fields.Char('SDS Name')
    regulatory_compliance = fields.Text('Regulatory Compliance')
    shelf_life = fields.Float('Shelf Life (Days)')
    storage_temperature = fields.Float('Storage Temperature (°C)')
    storage_humidity = fields.Float('Storage Humidity (%)')

    # Track if this is an ISL model instance
    is_isl_model = fields.Boolean('Is ISL Model', default=True, readonly=True)


class AgriQualityMixin(models.AbstractModel):
    """
    Abstract base model for quality control ISL models
    Implements US-084-10
    """
    _name = 'agri.quality.mixin'
    _description = 'Agri Quality Control ISL Abstract Base Model'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Common fields for quality ISL models
    industry_type = fields.Selection([
        ('food_processing', 'Food Processing'),
        ('pharmaceutical', 'Pharmaceutical'),
        ('chemical', 'Chemical'),
        ('general', 'General Manufacturing')
    ], string='Industry Type', default='general', required=True, ondelete={'food_processing': 'cascade', 'pharmaceutical': 'cascade', 'chemical': 'cascade', 'general': 'cascade'})

    quality_standard = fields.Char('Quality Standard')
    quality_procedures = fields.Html('Quality Procedures')
    inspection_frequency = fields.Char('Inspection Frequency')
    critical_control_points = fields.Text('Critical Control Points')
    quality_metrics = fields.Text('Quality Metrics')

    # Track if this is an ISL model instance
    is_isl_model = fields.Boolean('Is ISL Model', default=True, readonly=True)