# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

# Concrete ISL Models using _inherits mechanism

class AgriMRPProduction(models.Model):
    """
    ISL model for Agricultural Interventions with industry specialization
    Implements US-084-01: Intervention ISL model implementation
    """
    _name = 'agri.isl.mrp.production'
    _description = 'Agri ISL Agricultural Intervention'
    _inherits = {'mrp.production': 'mrp_production_id'}
    _inherit = [
        'agri.isl.manufacturing.mixin',
        'agri.isl.trait.food_safety',
        'agri.isl.trait.livestock',
        'agri.isl.trait.aquaculture'
    ]

    mrp_production_id = fields.Many2one(
        'mrp.production',
        string='Base Intervention',
        required=True,
        ondelete='cascade'
    )

    # Industry-specific methods
    def _check_industry_compliance(self):
        """Check industry-specific compliance before production"""
        if self.industry_type == 'field_crop':
            if not self.haccp_plan:
                raise UserError(_("Food processing production requires HACCP plan"))
        elif self.industry_type == 'livestock':
            if not self.gmp_compliance:
                raise UserError(_("Pharmaceutical production requires GMP compliance"))
        elif self.industry_type == 'aquaculture':
            if not self.safety_procedures:
                raise UserError(_("Chemical production requires safety procedures"))
        return super()._validate_industry_requirements()

    def unlink(self):
        # Multi-level Cascade Safeguard (多级级联物理删除防护)
        for rec in self:
            if 'farm.haccp.check' in self.env:
                unfinished_haccp = self.env['farm.haccp.check'].search([
                    ('quality_check_id.production_id', '=', rec.mrp_production_id.id),
                    ('is_violated', '=', True)
                ], limit=1)
                if unfinished_haccp:
                    raise UserError(_(
                        "Multi-level Cascade Safeguard: Cannot delete ISL Intervention '%s' "
                        "due to unresolved critical GxP/HACCP violations."
                    ) % rec.mrp_production_id.name)
        return super(AgriMRPProduction, self).unlink()


class AgriMRPBom(models.Model):
    """
    ISL model for Cultivation Recipes with industry specialization
    Implements US-084-02: Recipe ISL model implementation
    """
    _name = 'agri.isl.mrp.bom'
    _description = 'Agri ISL Cultivation Recipe'
    _inherits = {'mrp.bom': 'mrp_bom_id'}
    _inherit = [
        'agri.isl.manufacturing.mixin',
        'agri.isl.trait.food_safety',
        'agri.isl.trait.livestock',
        'agri.isl.trait.chemical'
    ]

    mrp_bom_id = fields.Many2one(
        'mrp.bom',
        string='Base Recipe',
        required=True,
        ondelete='cascade'
    )

    recipe_validation = fields.Html('Recipe Validation')
    ingredient_compliance = fields.Text('Ingredient Compliance')

    def _validate_recipe_compliance(self):
        """Validate recipe compliance based on industry type"""
        if self.industry_type == 'field_crop':
            # Check for allergen control
            if not self.allergen_control and any('allergen' in comp.name.lower() for comp in self.bom_line_ids):
                raise UserError(_("Food BOM with allergens requires allergen control"))
        elif self.industry_type == 'livestock':
            if not self.active_ingredient:
                raise UserError(_("Pharmaceutical BOM requires active ingredient specification"))
        return True

class AgriMRPWorkcenter(models.Model):
    """
    Implements US-084-03: Facility Unit ISL model implementation
    """
    _name = 'agri.isl.mrp.workcenter'
    _description = 'Agri ISL Facility Unit'
    _inherits = {'mrp.workcenter': 'workcenter_id'}
    _inherit = [
        'agri.isl.manufacturing.mixin',
        'agri.isl.trait.chemical'
    ]

    workcenter_id = fields.Many2one(
        'mrp.workcenter',
        string='Base Facility Unit',
        required=True,
        ondelete='cascade'
    )

    # Industry-specific fields for work centers
    cip_required = fields.Boolean('CIP Required')  # Clean-in-place, for food/pharma
    clean_room_class = fields.Char('Clean Room Class')  # For pharma
    capacity_uom = fields.Char('Capacity Unit of Measure')
    efficiency_factor = fields.Float('Efficiency Factor', default=1.0)

    def _validate_workcenter_compliance(self):
        """Validate work center compliance based on industry type"""
        if self.industry_type in ['field_crop', 'livestock']:
            if not self.cip_required:
                raise UserError(_("Food/pharmaceutical work centers require CIP capability"))
        elif self.industry_type == 'aquaculture':
            if not self.explosion_proof:
                raise UserError(_("Chemical work centers require explosion-proof equipment"))
        return True


class AgriStockLot(models.Model):
    """
    ISL model for Stock Lots with industry specialization
    Implements US-084-04: Inventory batch ISL model implementation
    """
    _name = 'agri.isl.stock.lot'
    _description = 'Agri ISL Stock Lot'
    _inherits = {'stock.lot': 'stock_lot_id'}
    _inherit = [
        'agri.isl.inventory.mixin',
        'agri.isl.trait.livestock'
    ]

    stock_lot_id = fields.Many2one(
        'stock.lot',
        string='Base Stock Lot',
        required=True,
        ondelete='cascade'
    )

    harvest_date = fields.Date('Harvest Date')  # Agriculture
    certificate_of_analysis = fields.Binary('Certificate of Analysis')
    certificate_of_analysis_name = fields.Char('COA Name')
    stability_data = fields.Html('Stability Data')
    storage_conditions = fields.Html('Storage Conditions')

    def _validate_lot_compliance(self):
        """Validate lot compliance based on industry type"""
        if self.industry_type == 'livestock':
            if not self.sterility_date:
                raise UserError(_("Pharmaceutical lots require sterility date"))
        elif self.industry_type == 'field_crop':
            if not self.kill_date:
                raise UserError(_("Food processing lots require kill date"))
        return True

    def unlink(self):
        # Multi-level Cascade Safeguard (多级级联物理删除防护)
        for rec in self:
            if 'stock.matter.tracking' in self.env:
                active_carrier = self.env['stock.matter.tracking'].search([
                    ('lot_id', '=', rec.stock_lot_id.id)
                ], limit=1)
                if active_carrier:
                    raise UserError(_(
                        "Multi-level Cascade Safeguard: Cannot delete ISL Lot '%s' because "
                        "it is linked to an active dynamic Matter Tracking carrier."
                    ) % rec.name)
        return super(AgriStockLot, self).unlink()


class AgriSaleOrder(models.Model):
    """
    ISL model for Sale Orders with industry specialization
    Implements US-084-05: Sales order ISL model implementation
    """
    _name = 'agri.isl.sale.order'
    _description = 'Agri ISL Sale Order'
    _inherits = {'sale.order': 'sale_order_id'}
    _inherit = [
        'agri.isl.sales.purchase.mixin',
        'agri.isl.trait.traceability'
    ]

    sale_order_id = fields.Many2one(
        'sale.order',
        string='Base Sale Order',
        required=True,
        ondelete='cascade'
    )

    delivery_compliance = fields.Html('Delivery Compliance')
    shipping_conditions = fields.Html('Shipping Conditions')
    certificate_requirements = fields.Html('Certificate Requirements')
    temperature_monitoring = fields.Boolean('Temperature Monitoring', default=False)

    def _validate_sales_compliance(self):
        """Validate sales compliance based on industry type"""
        if self.industry_type == 'field_crop':
            if not self.traceability_requirements:
                raise UserError(_("Food processing sales require traceability requirements"))
        elif self.industry_type == 'livestock':
            if not self.temperature_monitoring:
                raise UserError(_("Pharmaceutical sales require temperature monitoring"))
        return True


class AgriPurchaseOrder(models.Model):
    """
    ISL model for Purchase Orders with industry specialization
    Implements US-084-06: Purchase order ISL model implementation
    """
    _name = 'agri.isl.purchase.order'
    _description = 'Agri ISL Purchase Order'
    _inherits = {'purchase.order': 'purchase_order_id'}
    _inherit = ['agri.isl.sales.purchase.mixin']

    purchase_order_id = fields.Many2one(
        'purchase.order',
        string='Base Purchase Order',
        required=True,
        ondelete='cascade'
    )

    supplier_certification = fields.Char('Supplier Certification')
    incoming_inspection = fields.Html('Incoming Inspection')
    certificate_verification = fields.Html('Certificate Verification')
    quality_agreement = fields.Html('Quality Agreement')

    def _validate_purchase_compliance(self):
        """Validate purchase compliance based on industry type"""
        if self.industry_type == 'livestock':
            if not self.quality_agreement:
                raise UserError(_("Pharmaceutical purchases require quality agreement"))
        elif self.industry_type == 'field_crop':
            if not self.certificate_verification:
                raise UserError(_("Food processing purchases require certificate verification"))
        return True


class AgriProductTemplate(models.Model):
    """
    ISL model for Product Templates with industry specialization
    Implements US-084-07: Product template ISL model implementation
    """
    _name = 'agri.isl.product.template'
    _description = 'Agri ISL Product Template'
    _inherits = {'product.template': 'product_template_id'}
    _inherit = [
        'agri.isl.product.mixin',
        'agri.isl.trait.food_safety',
        'agri.isl.trait.livestock',
        'agri.isl.trait.chemical'
    ]

    product_template_id = fields.Many2one(
        'product.template',
        string='Base Product Template',
        required=True,
        ondelete='cascade'
    )

    safety_data_sheet = fields.Binary('Safety Data Sheet')
    safety_data_sheet_name = fields.Char('SDS Name')
    regulatory_compliance = fields.Text('Regulatory Compliance')
    shelf_life = fields.Float('Shelf Life (Days)')
    storage_temperature = fields.Float('Storage Temperature (°C)')
    storage_humidity = fields.Float('Storage Humidity (%)')

    def _validate_product_compliance(self):
        """Validate product compliance based on industry type"""
        if self.industry_type == 'field_crop':
            if not self.allergen_information:
                raise UserError(_("Food products require allergen information"))
        elif self.industry_type == 'livestock':
            if not self.pharmacological_class:
                raise UserError(_("Pharmaceutical products require pharmacological class"))
        elif self.industry_type == 'aquaculture':
            if not self.hazard_class:
                raise UserError(_("Chemical products require hazard class"))
        return True


class AgriStockPicking(models.Model):
    """
    ISL model for Stock Pickings with industry specialization
    Implements US-084-08: Inventory transfer ISL model implementation
    """
    _name = 'agri.isl.stock.picking'
    _description = 'Agri ISL Stock Picking'
    _inherits = {'stock.picking': 'picking_id'}
    _inherit = [
        'agri.isl.inventory.mixin',
        'agri.isl.trait.traceability'
    ]

    picking_id = fields.Many2one(
        'stock.picking',
        string='Base Stock Picking',
        required=True,
        ondelete='cascade'
    )

    compliance_verification = fields.Html('Compliance Verification')

    def _validate_picking_compliance(self):
        """Validate picking compliance based on industry type"""
        if self.industry_type in ['livestock', 'field_crop']:
            if self.temperature_control and not self.temperature_log:
                raise UserError(_("Temperature-controlled transfers require temperature log"))
        return True


class AgriMRPWorkorder(models.Model):
    """
    ISL model for Operation Phases with industry specialization
    Implements US-084-09: Operation phase ISL model implementation
    """
    _name = 'agri.isl.mrp.workorder'
    _description = 'Agri ISL Operation Phase'
    _inherits = {'mrp.workorder': 'workorder_id'}
    _inherit = [
        'agri.isl.manufacturing.mixin',
        'agri.isl.trait.livestock'
    ]

    workorder_id = fields.Many2one(
        'mrp.workorder',
        string='Base Operation Phase',
        required=True,
        ondelete='cascade'
    )

    operator_certification = fields.Html('Operator Certification')
    equipment_validation = fields.Html('Equipment Validation')
    in_process_inspection = fields.Html('In-Process Inspection')

    def _validate_workorder_compliance(self):
        """Validate work order compliance based on industry type"""
        if self.industry_type == 'livestock':
            if not self.batch_record:
                raise UserError(_("Pharmaceutical work orders require batch record"))
        elif self.industry_type in ['field_crop', 'livestock']:
            if not self.in_process_inspection:
                raise UserError(_("Food/pharmaceutical work orders require in-process inspection"))
        return True


class AgriQualityControl(models.Model):
    """
    ISL model for Quality Control Points with industry specialization
    Implements US-084-10: Quality control point ISL model implementation
    """
    _name = 'agri.isl.quality.control'
    _description = 'Agri ISL Quality Control'
    _inherits = {'quality.point': 'quality_point_id'}
    _inherit = [
        'agri.isl.quality.mixin',
        'agri.isl.trait.food_safety',
        'agri.isl.trait.livestock'
    ]

    quality_point_id = fields.Many2one(
        'quality.point',
        string='Base Quality Point',
        required=True,
        ondelete='cascade'
    )

    aql_sampling = fields.Html('AQL Sampling')  # Acceptable Quality Level
    testing_procedures = fields.Html('Testing Procedures')
    acceptance_criteria = fields.Html('Acceptance Criteria')
    deviation_handling = fields.Html('Deviation Handling')

    def _validate_quality_compliance(self):
        """Validate quality control compliance based on industry type"""
        if self.industry_type == 'field_crop':
            if not self.ccp_monitoring:
                raise UserError(_("Food processing quality control requires CCP monitoring"))
        elif self.industry_type == 'livestock':
            if not self.aql_sampling:
                raise UserError(_("Pharmaceutical quality control requires AQL sampling"))
        return True
