# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

# Concrete ISL Models using _inherits mechanism

class AgriMRPProduction(models.Model):
    """
    ISL model for MRP Production Orders with industry specialization
    Implements US-084-01: MRP production order ISL model implementation
    """
    _name = 'agri.mrp.production'
    # TODO: [DE-INDUSTRIAL] Use 'Agri ISL Intervention' or similar
    _description = 'Agri ISL MRP Production Order'
    _inherits = {'mrp.production': 'mrp_production_id'}
    _inherit = ['agri.manufacturing.mixin']

    mrp_production_id = fields.Many2one(
        'mrp.production',
        # TODO: [DE-INDUSTRIAL] Use 'Base Intervention'
        string='Base MRP Production',
        required=True,
        ondelete='cascade'
    )


    haccp_plan = fields.Html('HACCP Plan')  # Food processing
    gmp_compliance = fields.Boolean('GMP Compliance')  # Pharmaceutical
    safety_procedures = fields.Html('Safety Procedures')  # Chemical
    quality_gate_checks = fields.Text('Quality Gate Checks')

    # Industry-specific methods
    def _check_industry_compliance(self):
        """Check industry-specific compliance before production"""
        if self.industry_type == 'food_processing':
            if not self.haccp_plan:
                raise UserError(_("Food processing production requires HACCP plan"))
        elif self.industry_type == 'pharmaceutical':
            if not self.gmp_compliance:
                raise UserError(_("Pharmaceutical production requires GMP compliance"))
        elif self.industry_type == 'chemical':
            if not self.safety_procedures:
                raise UserError(_("Chemical production requires safety procedures"))
        return super()._validate_industry_requirements()


class AgriMRPBom(models.Model):
    """
    ISL model for MRP BOMs with industry specialization
    Implements US-084-02: MRP BOM ISL model implementation
    """
    _name = 'agri.mrp.bom'
    # TODO: [DE-INDUSTRIAL] Use 'Agri ISL Cultivation Recipe'
    _description = 'Agri ISL MRP Bill of Materials'
    _inherits = {'mrp.bom': 'mrp_bom_id'}
    _inherit = ['agri.manufacturing.mixin']

    mrp_bom_id = fields.Many2one(
        'mrp.bom',
        # TODO: [DE-INDUSTRIAL] Use 'Base Recipe'
        string='Base MRP BOM',
        required=True,
        ondelete='cascade'
    )


    # Industry-specific fields for BOMs
    allergen_control = fields.Boolean('Allergen Control')  # Food processing
    active_ingredient = fields.Char('Active Ingredient')  # Pharmaceutical
    safety_coefficient = fields.Float('Safety Coefficient')  # Chemical
    recipe_validation = fields.Html('Recipe Validation')
    ingredient_compliance = fields.Text('Ingredient Compliance')

    def _validate_recipe_compliance(self):
        """Validate recipe compliance based on industry type"""
        if self.industry_type == 'food_processing':
            # Check for allergen control
            if not self.allergen_control and any('allergen' in comp.name.lower() for comp in self.bom_line_ids):
                raise UserError(_("Food BOM with allergens requires allergen control"))
        elif self.industry_type == 'pharmaceutical':
            if not self.active_ingredient:
                raise UserError(_("Pharmaceutical BOM requires active ingredient specification"))
        return True

class AgriMRPWorkcenter(models.Model):
    """
    Implements US-084-03: MRP work center ISL model implementation
    """
    _name = 'agri.mrp.workcenter'
    # TODO: [DE-INDUSTRIAL] Use 'Agri ISL Processing Unit' or 'Farm Facility'
    _description = 'Agri ISL MRP Work Center'
    _inherits = {'mrp.workcenter': 'workcenter_id'}
    _inherit = ['agri.manufacturing.mixin']

    workcenter_id = fields.Many2one(
        'mrp.workcenter',
        # TODO: [DE-INDUSTRIAL] Use 'Base Facility'
        string='Base Work Center',
        required=True,
        ondelete='cascade'
    )


    # Industry-specific fields for work centers
    cip_required = fields.Boolean('CIP Required')  # Clean-in-place, for food/pharma
    explosion_proof = fields.Boolean('Explosion Proof')  # For chemical industry
    clean_room_class = fields.Char('Clean Room Class')  # For pharma
    capacity_uom = fields.Char('Capacity Unit of Measure')
    efficiency_factor = fields.Float('Efficiency Factor', default=1.0)

    def _validate_workcenter_compliance(self):
        """Validate work center compliance based on industry type"""
        if self.industry_type in ['food_processing', 'pharmaceutical']:
            if not self.cip_required:
                raise UserError(_("Food/pharmaceutical work centers require CIP capability"))
        elif self.industry_type == 'chemical':
            if not self.explosion_proof:
                raise UserError(_("Chemical work centers require explosion-proof equipment"))
        return True


class AgriStockLot(models.Model):
    """
    ISL model for Stock Lots with industry specialization
    Implements US-084-04: Inventory batch ISL model implementation
    """
    _name = 'agri.stock.lot'
    _description = 'Agri ISL Stock Lot'
    _inherits = {'stock.lot': 'stock_lot_id'}
    _inherit = ['agri.inventory.mixin']

    stock_lot_id = fields.Many2one(
        'stock.lot',
        string='Base Stock Lot',
        required=True,
        ondelete='cascade'
    )


    # Industry-specific fields for lots
    harvest_date = fields.Date('Harvest Date')  # Agriculture
    kill_date = fields.Date('Kill Date')  # Food processing
    sterility_date = fields.Date('Sterility Date')  # Pharmaceuticals
    certificate_of_analysis = fields.Binary('Certificate of Analysis')
    certificate_of_analysis_name = fields.Char('COA Name')
    stability_data = fields.Html('Stability Data')
    storage_conditions = fields.Html('Storage Conditions')

    def _validate_lot_compliance(self):
        """Validate lot compliance based on industry type"""
        if self.industry_type == 'pharmaceutical':
            if not self.sterility_date:
                raise UserError(_("Pharmaceutical lots require sterility date"))
        elif self.industry_type == 'food_processing':
            if not self.kill_date:
                raise UserError(_("Food processing lots require kill date"))
        return True


class AgriSaleOrder(models.Model):
    """
    ISL model for Sale Orders with industry specialization
    Implements US-084-05: Sales order ISL model implementation
    """
    _name = 'agri.sale.order'
    _description = 'Agri ISL Sale Order'
    _inherits = {'sale.order': 'sale_order_id'}
    _inherit = ['agri.sales.purchase.mixin']

    sale_order_id = fields.Many2one(
        'sale.order',
        string='Base Sale Order',
        required=True,
        ondelete='cascade'
    )


    # Industry-specific fields for sales orders
    delivery_compliance = fields.Html('Delivery Compliance')
    traceability_requirements = fields.Html('Traceability Requirements')
    shipping_conditions = fields.Html('Shipping Conditions')
    certificate_requirements = fields.Html('Certificate Requirements')
    temperature_monitoring = fields.Boolean('Temperature Monitoring', default=False)

    def _validate_sales_compliance(self):
        """Validate sales compliance based on industry type"""
        if self.industry_type == 'food_processing':
            if not self.traceability_requirements:
                raise UserError(_("Food processing sales require traceability requirements"))
        elif self.industry_type == 'pharmaceutical':
            if not self.temperature_monitoring:
                raise UserError(_("Pharmaceutical sales require temperature monitoring"))
        return True


class AgriPurchaseOrder(models.Model):
    """
    ISL model for Purchase Orders with industry specialization
    Implements US-084-06: Purchase order ISL model implementation
    """
    _name = 'agri.purchase.order'
    _description = 'Agri ISL Purchase Order'
    _inherits = {'purchase.order': 'purchase_order_id'}
    _inherit = ['agri.sales.purchase.mixin']

    purchase_order_id = fields.Many2one(
        'purchase.order',
        string='Base Purchase Order',
        required=True,
        ondelete='cascade'
    )


    # Industry-specific fields for purchase orders
    supplier_certification = fields.Char('Supplier Certification')
    incoming_inspection = fields.Html('Incoming Inspection')
    certificate_verification = fields.Html('Certificate Verification')
    quality_agreement = fields.Html('Quality Agreement')

    def _validate_purchase_compliance(self):
        """Validate purchase compliance based on industry type"""
        if self.industry_type == 'pharmaceutical':
            if not self.quality_agreement:
                raise UserError(_("Pharmaceutical purchases require quality agreement"))
        elif self.industry_type == 'food_processing':
            if not self.certificate_verification:
                raise UserError(_("Food processing purchases require certificate verification"))
        return True


class AgriProductTemplate(models.Model):
    """
    ISL model for Product Templates with industry specialization
    Implements US-084-07: Product template ISL model implementation
    """
    _name = 'agri.product.template'
    _description = 'Agri ISL Product Template'
    _inherits = {'product.template': 'product_template_id'}
    _inherit = ['agri.product.mixin']

    product_template_id = fields.Many2one(
        'product.template',
        string='Base Product Template',
        required=True,
        ondelete='cascade'
    )


    # Industry-specific fields for product templates
    allergen_information = fields.Html('Allergen Information')  # Food processing
    pharmacological_class = fields.Char('Pharmacological Class')  # Pharmaceutical
    safety_data_sheet = fields.Binary('Safety Data Sheet')
    safety_data_sheet_name = fields.Char('SDS Name')
    hazard_class = fields.Char('Hazard Class')  # Chemical
    regulatory_class = fields.Char('Regulatory Class')

    def _validate_product_compliance(self):
        """Validate product compliance based on industry type"""
        if self.industry_type == 'food_processing':
            if not self.allergen_information:
                raise UserError(_("Food products require allergen information"))
        elif self.industry_type == 'pharmaceutical':
            if not self.pharmacological_class:
                raise UserError(_("Pharmaceutical products require pharmacological class"))
        elif self.industry_type == 'chemical':
            if not self.hazard_class:
                raise UserError(_("Chemical products require hazard class"))
        return True


class AgriStockPicking(models.Model):
    """
    ISL model for Stock Pickings with industry specialization
    Implements US-084-08: Inventory transfer ISL model implementation
    """
    _name = 'agri.stock.picking'
    _description = 'Agri ISL Stock Picking'
    _inherits = {'stock.picking': 'picking_id'}
    _inherit = ['agri.inventory.mixin']

    picking_id = fields.Many2one(
        'stock.picking',
        string='Base Stock Picking',
        required=True,
        ondelete='cascade'
    )


    # Industry-specific fields for stock pickings
    chain_of_custody = fields.Html('Chain of Custody')
    temperature_log = fields.Html('Temperature Log')
    humidity_log = fields.Html('Humidity Log')
    security_seal = fields.Char('Security Seal')
    compliance_verification = fields.Html('Compliance Verification')

    def _validate_picking_compliance(self):
        """Validate picking compliance based on industry type"""
        if self.industry_type in ['pharmaceutical', 'food_processing']:
            if self.temperature_control and not self.temperature_log:
                raise UserError(_("Temperature-controlled transfers require temperature log"))
        return True


class AgriMRPWorkorder(models.Model):
    """
    ISL model for MRP Work Orders with industry specialization
    Implements US-084-09: MRP work order ISL model implementation
    """
    _name = 'agri.mrp.workorder'
    _description = 'Agri ISL MRP Work Order'
    _inherits = {'mrp.workorder': 'workorder_id'}
    _inherit = ['agri.manufacturing.mixin']

    workorder_id = fields.Many2one(
        'mrp.workorder',
        string='Base Work Order',
        required=True,
        ondelete='cascade'
    )


    # Industry-specific fields for work orders
    operator_certification = fields.Html('Operator Certification')
    equipment_validation = fields.Html('Equipment Validation')
    in_process_inspection = fields.Html('In-Process Inspection')
    batch_record = fields.Html('Batch Record')

    def _validate_workorder_compliance(self):
        """Validate work order compliance based on industry type"""
        if self.industry_type == 'pharmaceutical':
            if not self.batch_record:
                raise UserError(_("Pharmaceutical work orders require batch record"))
        elif self.industry_type in ['food_processing', 'pharmaceutical']:
            if not self.in_process_inspection:
                raise UserError(_("Food/pharmaceutical work orders require in-process inspection"))
        return True


class AgriQualityControl(models.Model):
    """
    ISL model for Quality Control Points with industry specialization
    Implements US-084-10: Quality control point ISL model implementation
    """
    _name = 'agri.quality.control'
    _description = 'Agri ISL Quality Control'
    # _inherits = {.agri.quality.point.: .agri_quality_point_id.}
    _inherit = ['agri.quality.mixin']

    # agri_quality_point_id = fields.Many2one(
#         .agri.quality.point.,
#         string=.Base Agri Quality Point.,
#     )


    # Industry-specific fields for quality control
    ccp_monitoring = fields.Html('CCP Monitoring')  # Critical Control Points, HACCP
    aql_sampling = fields.Html('AQL Sampling')  # Acceptable Quality Level
    testing_procedures = fields.Html('Testing Procedures')
    acceptance_criteria = fields.Html('Acceptance Criteria')
    deviation_handling = fields.Html('Deviation Handling')

    def _validate_quality_compliance(self):
        """Validate quality control compliance based on industry type"""
        if self.industry_type == 'food_processing':
            if not self.ccp_monitoring:
                raise UserError(_("Food processing quality control requires CCP monitoring"))
        elif self.industry_type == 'pharmaceutical':
            if not self.aql_sampling:
                raise UserError(_("Pharmaceutical quality control requires AQL sampling"))
        return True