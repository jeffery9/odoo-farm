from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class AgriCarbonNeutralGoal(models.Model):
    """
    US-083-01: 碳中和目标管理 (Carbon Neutral Goal Management)
    Management of carbon neutral goals and targets across the organization
    """
    _name = 'agri.carbon.neutral.goal'
    _description = 'Carbon Neutral Goal Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Goal Name', required=True)
    goal_code = fields.Char('Goal Code', required=True, copy=False, default=lambda self: self._generate_goal_code())
    description = fields.Text('Description')

    # Goal scope
    goal_scope = fields.Selection([
        ('organization', 'Organization Wide'),
        ('location', 'Specific Location'),
        ('product', 'Product Line'),
        ('process', 'Specific Process'),
        ('supply_chain', 'Supply Chain'),
    ], string='Goal Scope', required=True, default='organization')

    location_id = fields.Many2one('farm.location', string='Specific Location',
                                  domain=[('is_active', '=', True)],
                                  help='Applicable when scope is "location"')
    product_category_id = fields.Many2one('product.category', string='Product Category',
                                          help='Applicable when scope is "product"')
    process_type = fields.Char('Process Type',
                               help='Applicable when scope is "process"')

    # Time boundaries
    start_date = fields.Date('Start Date', required=True)
    target_completion_date = fields.Date('Target Completion Date', required=True)
    actual_completion_date = fields.Date('Actual Completion Date')

    # Carbon metrics
    baseline_emissions = fields.Float('Baseline Emissions (tCO2e)', required=True,
                                     help='Emissions at the start of the goal period')
    target_emissions = fields.Float('Target Emissions (tCO2e)', required=True,
                                   help='Emissions target at goal completion')
    current_emissions = fields.Float('Current Emissions (tCO2e)',
                                    help='Current emissions level toward the goal')
    emissions_reduction_target = fields.Float('Emissions Reduction Target (tCO2e)',
                                             compute='_compute_emissions_reduction', store=True, precompute=True)

    # Progress tracking
    progress_percentage = fields.Float('Progress Percentage (%)', compute='_compute_progress', store=True, precompute=True)
    status = fields.Selection([
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('on_track', 'On Track'),
        ('at_risk', 'At Risk'),
        ('delayed', 'Delayed'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], string='Status', compute='_compute_status', store=True, precompute=True)

    # Carbon offset strategy
    offset_strategy = fields.Selection([
        ('renewable_energy', 'Renewable Energy'),
        ('forestation', 'Reforestation/Revegetation'),
        ('energy_efficiency', 'Energy Efficiency'),
        ('carbon_capture', 'Carbon Capture and Storage'),
        ('agroforestry', 'Agroforestry'),
        ('soil_carbon', 'Soil Carbon Sequestration'),
        ('other', 'Other'),
    ], string='Offset Strategy')
    offset_projects_description = fields.Text('Offset Projects Description')

    # Financial aspects
    budget_allocated = fields.Float('Budget Allocated')
    budget_spent = fields.Float('Budget Spent')
    cost_per_ton_co2 = fields.Float('Cost per Ton CO2', help='Estimated cost per ton of CO2 reduced/offset')

    # Related activities
    implementation_activities = fields.Text('Implementation Activities')
    monitoring_plan = fields.Text('Monitoring Plan')
    verification_method = fields.Selection([
        ('internal_audit', 'Internal Audit'),
        ('third_party', 'Third Party Verification'),
        ('blockchain', 'Blockchain Verification'),
        ('hybrid', 'Hybrid Verification'),
    ], string='Verification Method', default='internal_audit')

    # Stakeholder involvement
    responsible_user_id = fields.Many2one('res.users', string='Responsible Person')
    stakeholders = fields.Many2many('res.partner', string='Stakeholders')

    # Documentation
    supporting_documents = fields.Binary('Supporting Documents', attachment=True)
    document_name = fields.Char('Document Name')

    @api.model
    def _generate_goal_code(self):
        """Generate a unique goal code"""
        return self.env['ir.sequence'].next_by_code('agri.carbon.neutral.goal') or 'CG-NEW'

    @api.constrains('start_date', 'target_completion_date', 'baseline_emissions', 'target_emissions')
    def _check_dates_and_values(self):
        for record in self:
            if record.start_date and record.target_completion_date:
                if record.start_date >= record.target_completion_date:
                    raise ValidationError(_("Start date must be before target completion date."))
            if record.baseline_emissions < 0 or record.target_emissions < 0:
                raise ValidationError(_("Emissions values cannot be negative."))
            if record.target_emissions > record.baseline_emissions:
                raise ValidationError(_("Target emissions should be less than or equal to baseline emissions for reduction goals."))

    @api.depends('baseline_emissions', 'target_emissions')
    def _compute_emissions_reduction(self):
        for record in self:
            record.emissions_reduction_target = record.baseline_emissions - record.target_emissions

    @api.depends('current_emissions', 'baseline_emissions', 'target_emissions')
    def _compute_progress(self):
        for record in self:
            if record.baseline_emissions != record.target_emissions:  # Avoid division by zero for no-reduction goals
                # Calculate progress based on emissions reduction achieved
                reduction_achieved = (record.baseline_emissions or 0) - (record.current_emissions or 0)
                total_reduction_target = (record.baseline_emissions or 0) - (record.target_emissions or 0)

                if total_reduction_target != 0:
                    record.progress_percentage = min(100, max(0, (reduction_achieved / total_reduction_target) * 100))
                else:
                    record.progress_percentage = 100 if reduction_achieved >= 0 else 0
            else:
                record.progress_percentage = 0

    @api.depends('progress_percentage', 'target_completion_date')
    def _compute_status(self):
        for record in self:
            current_date = fields.Date.context_today(self)

            if record.actual_completion_date:
                # Check if completed on time
                if record.actual_completion_date <= record.target_completion_date:
                    record.status = 'completed'
                else:
                    record.status = 'completed'  # Still completed, but late
            elif current_date > record.target_completion_date:
                # Goal is overdue
                record.status = 'failed'
            else:
                # Calculate if on track based on timeline and progress
                if record.target_completion_date and record.start_date:
                    total_days = (record.target_completion_date - record.start_date).days
                    elapsed_days = (current_date - record.start_date).days
                    expected_progress = (elapsed_days / total_days) * 100 if total_days > 0 else 0

                    if record.progress_percentage >= expected_progress * 0.9:  # 90% of expected progress
                        record.status = 'on_track'
                    elif record.progress_percentage >= expected_progress * 0.7:  # 70% of expected progress
                        record.status = 'at_risk'
                    elif record.progress_percentage < expected_progress * 0.5:  # Less than 50% of expected progress
                        record.status = 'delayed'
                    else:
                        record.status = 'in_progress'
                else:
                    record.status = 'in_progress' if record.progress_percentage > 0 else 'in_progress'

    def action_update_current_emissions(self):
        """Update current emissions based on latest data"""
        for record in self:
            # In real implementation, this would aggregate data from carbon ledger, supply chain data, etc.
            # For now, we'll keep the current emissions as is or update from some data source
            record.message_post(body=_("Current emissions should be updated from carbon tracking systems."))

    def action_generate_progress_report(self):
        """Generate a progress report for the carbon neutral goal"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Carbon Neutral Goal Progress Report'),
            'res_model': 'agri.carbon.neutral.goal',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'context': self.env.context,
        }

    def action_mark_completed(self):
        """Mark the goal as completed"""
        for record in self:
            record.actual_completion_date = fields.Date.context_today(record)
            record.status = 'completed'
            record.message_post(body=_("Carbon neutral goal marked as completed."))


class AgriCarbonCredit(models.Model):
    """
    US-083-02: 碳信用管理 (Carbon Credit Management)
    Management of carbon credits for trading and offsetting
    """
    _name = 'agri.carbon.credit'
    _description = 'Carbon Credit Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Credit Name', required=True)
    credit_code = fields.Char('Credit Code', required=True, copy=False, default=lambda self: self._generate_credit_code())
    description = fields.Text('Description')

    # Credit details
    credit_quantity = fields.Float('Credit Quantity (tCO2e)', required=True)
    unit_price = fields.Float('Unit Price ($/tCO2e)')
    total_value = fields.Float('Total Value ($)', compute='_compute_total_value', store=True, precompute=True)
    vintage_year = fields.Integer('Vintage Year', required=True,
                                 help='Year when the carbon reduction was achieved')

    # Verification and standards
    verification_standard = fields.Selection([
        ('vcs', 'Verified Carbon Standard (VCS)'),
        ('gold', 'Gold Standard'),
        ('climate_action', 'Climate Action Reserve'),
        ('ccp', 'China Carbon Pool'),
        ('acr', 'American Carbon Registry'),
        ('other', 'Other'),
    ], string='Verification Standard', required=True)

    verification_body = fields.Char('Verification Body')
    verification_date = fields.Date('Verification Date')
    certification_number = fields.Char('Certification Number')

    # Credit status
    status = fields.Selection([
        ('issued', 'Issued'),
        ('transferred', 'Transferred'),
        ('retired', 'Retired'),
        ('available', 'Available for Sale'),
        ('contracted', 'Contracted'),
    ], string='Status', required=True, default='available')

    # Ownership and transfer
    owner_partner_id = fields.Many2one('res.partner', string='Owner', required=True)
    project_location_id = fields.Many2one('farm.location', string='Project Location')
    project_description = fields.Text('Project Description')

    # Compliance and use
    compliance_scope = fields.Selection([
        ('voluntary', 'Voluntary Market'),
        ('compliance', 'Compliance Market'),
        ('internal', 'Internal Use'),
    ], string='Compliance Scope', default='voluntary')

    eligible_for_compliance = fields.Boolean('Eligible for Compliance Use',
                                           help='Can be used for regulatory compliance purposes')

    # Trading information
    purchase_date = fields.Date('Purchase Date')
    purchase_price = fields.Float('Purchase Price ($/tCO2e)')
    seller_partner_id = fields.Many2one('res.partner', string='Seller')
    contract_reference = fields.Char('Contract Reference')

    # Retirement information
    retirement_date = fields.Date('Retirement Date')
    retirement_reason = fields.Selection([
        ('compliance', 'Regulatory Compliance'),
        ('voluntary', 'Voluntary Offset'),
        ('internal', 'Internal Carbon Neutral Goal'),
        ('other', 'Other'),
    ], string='Retirement Reason')
    retiree_partner_id = fields.Many2one('res.partner', string='Retired By')

    @api.model
    def _generate_credit_code(self):
        """Generate a unique credit code"""
        return self.env['ir.sequence'].next_by_code('agri.carbon.credit') or 'CC-NEW'

    @api.constrains('credit_quantity', 'unit_price', 'vintage_year')
    def _check_credit_values(self):
        for record in self:
            if record.credit_quantity <= 0:
                raise ValidationError(_("Credit quantity must be positive."))
            if record.unit_price < 0:
                raise ValidationError(_("Unit price cannot be negative."))
            if record.vintage_year > fields.Date.context_today(self).year + 1:
                raise ValidationError(_("Vintage year cannot be in the future."))

    @api.depends('credit_quantity', 'unit_price')
    def _compute_total_value(self):
        for record in self:
            record.total_value = (record.credit_quantity or 0) * (record.unit_price or 0)

    def action_transfer_credits(self):
        """Transfer credits to another party"""
        # This would typically open a wizard in real implementation
        for record in self:
            record.status = 'transferred'
            record.message_post(body=_("Carbon credits transferred."))

    def action_retire_credits(self):
        """Retire credits for compliance or offset purposes"""
        for record in self:
            record.status = 'retired'
            record.retirement_date = fields.Date.context_today(record)
            record.retiree_partner_id = self.env.user.partner_id
            record.message_post(body=_("Carbon credits retired for use."))

    def action_verify_credits(self):
        """Verify the carbon credits with verification body"""
        for record in self:
            record.verification_date = fields.Date.context_today(record)
            record.message_post(body=_("Carbon credits verified by %s on %s") %
                              (record.verification_body or 'Unknown Body', record.verification_date))


class AgriBioEnergyProduct(models.Model):
    """
    US-097-01: 生物能源产品管理 (Bio-energy Product Management)
    Management of bio-energy products for external ESG marketplace
    """
    _name = 'agri.bio.energy.product'
    _description = 'Bio-energy Product for ESG Marketplace'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Bio-energy Product Name', required=True)
    product_code = fields.Char('Product Code', required=True, copy=False, default=lambda self: self._generate_product_code())
    description = fields.Text('Description')

    # Product type
    product_type = fields.Selection([
        ('biogas', 'Biogas'),
        ('biofuel', 'Biofuel'),
        ('biodiesel', 'Biodiesel'),
        ('bioethanol', 'Bioethanol'),
        ('biomass', 'Biomass'),
        ('pellets', 'Pellets'),
        ('biogasoline', 'Biogasoline'),
        ('other', 'Other'),
    ], string='Product Type', required=True)

    # Production details
    raw_material_source = fields.Selection([
        ('agricultural_waste', 'Agricultural Waste'),
        ('forestry_residue', 'Forestry Residue'),
        ('energy_crops', 'Energy Crops'),
        ('algae', 'Algae'),
        ('other', 'Other'),
    ], string='Raw Material Source')

    energy_content = fields.Float('Energy Content (MJ/kg or MJ/m3)', help='Energy content per unit')
    co2_reduction_percentage = fields.Float('CO2 Reduction Percentage (%)',
                                           help='Percentage of CO2 reduction compared to fossil fuels')

    # Sustainability metrics
    sustainability_score = fields.Float('Sustainability Score (0-100)', compute='_compute_sustainability_score', store=True, precompute=True)
    lifecycle_assessment = fields.Text('Lifecycle Assessment Details')

    # Production location
    production_location_id = fields.Many2one('farm.location', string='Production Location', required=True)
    production_capacity = fields.Float('Production Capacity', help='Annual production capacity in specified units')
    production_unit = fields.Many2one('uom.uom', string='Production Unit')

    # ESG compliance
    #esg_certifications removed
    sustainability_standards = fields.Char('Sustainability Standards', help='Standards the product meets (e.g., RSB, ISCC)')

    # Marketplace information
    is_listed_in_marketplace = fields.Boolean('Listed in ESG Marketplace', default=False)
    marketplace_listing_date = fields.Date('Marketplace Listing Date')
    marketplace_category = fields.Selection([
        ('renewable_energy', 'Renewable Energy'),
        ('carbon_offset', 'Carbon Offset'),
        ('sustainable_fuel', 'Sustainable Fuel'),
        ('bio_material', 'Bio-based Material'),
    ], string='Marketplace Category')

    # Pricing and trading
    marketplace_price = fields.Float('Marketplace Price ($/unit)')
    available_quantity = fields.Float('Available Quantity')
    min_order_quantity = fields.Float('Minimum Order Quantity')

    # Quality certifications
    quality_grade = fields.Selection([
        ('premium', 'Premium'),
        ('standard', 'Standard'),
        ('basic', 'Basic'),
    ], string='Quality Grade', default='standard')

    #quality_certifications removed

    # Documentation
    technical_specifications = fields.Binary('Technical Specifications', attachment=True)
    spec_name = fields.Char('Spec Name')

    sustainability_report = fields.Binary('Sustainability Report', attachment=True)
    report_name = fields.Char('Report Name')

    @api.model
    def _generate_product_code(self):
        """Generate a unique product code"""
        return self.env['ir.sequence'].next_by_code('agri.bio.energy.product') or 'BEP-NEW'

    @api.constrains('energy_content', 'co2_reduction_percentage', 'production_capacity', 'available_quantity')
    def _check_positive_values(self):
        for record in self:
            if record.energy_content < 0:
                raise ValidationError(_("Energy content cannot be negative."))
            if record.co2_reduction_percentage < 0 or record.co2_reduction_percentage > 100:
                raise ValidationError(_("CO2 reduction percentage must be between 0 and 100."))
            if record.production_capacity < 0:
                raise ValidationError(_("Production capacity cannot be negative."))
            if record.available_quantity < 0:
                raise ValidationError(_("Available quantity cannot be negative."))

    @api.depends('co2_reduction_percentage')
    def _compute_sustainability_score(self):
        """Compute sustainability score based on various factors"""
        for record in self:
            score = 0.0
            # Base score from CO2 reduction
            score += (record.co2_reduction_percentage or 0) * 0.4  # 40% weight

            # Quality grade contributes to score
            grade_factor = {'premium': 30, 'standard': 20, 'basic': 10}
            score += grade_factor.get(record.quality_grade, 0)  # 10-30% weight

            # Certifications contribute to score
            score += len(record.esg_certifications) * 10  # Each certification adds 10 points

            record.sustainability_score = min(100, max(0, score))

    def action_list_in_marketplace(self):
        """List the product in the ESG marketplace"""
        for record in self:
            record.is_listed_in_marketplace = True
            record.marketplace_listing_date = fields.Date.context_today(record)
            record.message_post(body=_("Product listed in ESG marketplace."))

    def action_delist_from_marketplace(self):
        """Remove the product from the ESG marketplace"""
        for record in self:
            record.is_listed_in_marketplace = False
            record.message_post(body=_("Product removed from ESG marketplace."))

    def action_generate_sustainability_report(self):
        """Generate a sustainability report for the bio-energy product"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Bio-energy Product Sustainability Report'),
            'res_model': 'agri.bio.energy.product',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'context': self.env.context,
        }