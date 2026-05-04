from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class AgriSupplyChainCarbonDataEngine(models.Model):
    """
    US-076-01: 碳足迹数据采集引擎 (Carbon Footprint Data Collection Engine)
    Engine for collecting carbon footprint data across supply chain
    """
    _name = 'agri.supply.chain.carbon.data.engine'
    _description = 'Supply Chain Carbon Footprint Data Collection Engine'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Data Collection Task', required=True, copy=False)
    collection_date = fields.Datetime('Collection Date', default=fields.Datetime.now)

    # Data sources configuration
    data_source_type = fields.Selection([
        ('supplier', 'Supplier'),
        ('logistics', 'Logistics'),
        ('production', 'Production'),
        ('warehousing', 'Warehousing'),
        ('external_api', 'External API'),
        ('manual_input', 'Manual Input'),
    ], string='Data Source Type', required=True)

    # Carbon footprint details
    scope_1_emissions = fields.Float('Scope 1 Emissions (tCO2e)', help='Direct emissions from owned/controlled sources')
    scope_2_emissions = fields.Float('Scope 2 Emissions (tCO2e)', help='Indirect emissions from purchased energy')
    scope_3_emissions = fields.Float('Scope 3 Emissions (tCO2e)', help='Other indirect emissions in value chain')
    total_emissions = fields.Float('Total Emissions (tCO2e)', compute='_compute_total_emissions', store=True)

    # Compliance with international standards
    calculation_standard = fields.Selection([
        ('ghgp', 'GHG Protocol'),
        ('iso_14064', 'ISO 14064'),
        ('iso_14067', 'ISO 14067'),
        ('pascal', 'PAS 2050'),
        ('custom', 'Custom Standard'),
    ], string='Calculation Standard', required=True)

    # Related entities
    partner_id = fields.Many2one('res.partner', string='Supplier/Partner',
                                 domain=['|', ('supplier_rank', '>', 0), ('customer_rank', '>', 0)])
    product_id = fields.Many2one('product.template', string='Product')
    location_id = fields.Many2one('farm.location', string='Location')
    logistics_route_id = fields.Many2one('stock.route', string='Logistics Route')

    # Data quality and verification
    data_quality_score = fields.Float('Data Quality Score (0-100)',
                                      help='Assessment of data accuracy and completeness')
    verification_status = fields.Selection([
        ('unverified', 'Unverified'),
        ('pending', 'Pending Verification'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ], string='Verification Status', default='unverified')

    # Collection status
    collection_status = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], string='Collection Status', default='draft')

    # Compliance status
    compliance_status = fields.Selection([
        ('compliant', 'Compliant'),
        ('non_compliant', 'Non-Compliant'),
        ('pending_review', 'Pending Review'),
    ], string='Compliance Status', compute='_compute_compliance_status', store=True)

    # Related to carbon ledger
    related_carbon_ledger_ids = fields.One2many('agri.carbon.ledger', 'supply_chain_data_id',
                                                string='Related Carbon Ledger Entries')

    @api.depends('scope_1_emissions', 'scope_2_emissions', 'scope_3_emissions')
    def _compute_total_emissions(self):
        for record in self:
            record.total_emissions = (record.scope_1_emissions or 0) + \
                                   (record.scope_2_emissions or 0) + \
                                   (record.scope_3_emissions or 0)

    @api.depends('total_emissions', 'calculation_standard')
    def _compute_compliance_status(self):
        for record in self:
            # Simplified compliance check - in real implementation would use standard thresholds
            if record.total_emissions and record.total_emissions <= 100.0:  # Example threshold
                record.compliance_status = 'compliant'
            elif record.total_emissions and record.total_emissions > 500.0:  # Example threshold
                record.compliance_status = 'non_compliant'
            else:
                record.compliance_status = 'pending_review'

    @api.constrains('scope_1_emissions', 'scope_2_emissions', 'scope_3_emissions')
    def _check_positive_emissions(self):
        for record in self:
            if record.scope_1_emissions < 0 or record.scope_2_emissions < 0 or record.scope_3_emissions < 0:
                raise ValidationError(_("Emissions values cannot be negative."))

    def action_start_collection(self):
        """Start the data collection process"""
        for record in self:
            record.collection_status = 'in_progress'
            record.collection_date = fields.Datetime.now()
            record.message_post(body=_("Carbon footprint data collection started."))

    def action_complete_collection(self):
        """Complete the data collection"""
        for record in self:
            record.collection_status = 'completed'
            record.message_post(body=_("Carbon footprint data collection completed. Total emissions: %.2f tCO2e") %
                              record.total_emissions)

    def action_trigger_real_time_monitoring(self):
        """Trigger real-time carbon monitoring"""
        for record in self:
            # This would integrate with IoT sensors and real-time data sources in a real implementation
            record.message_post(body=_("Real-time carbon monitoring activated for this data collection task."))

    def action_verify_data(self):
        """Verify the collected carbon data"""
        for record in self:
            record.verification_status = 'verified'
            # Calculate data quality score based on various factors
            quality_score = 85.0  # Placeholder calculation
            record.data_quality_score = quality_score
            record.message_post(body=_("Carbon data verified. Quality score: %.1f") % quality_score)


class AgriSupplyChainCarbonReductionStrategy(models.Model):
    """
    US-076-02: 智能碳减排策略 (AI-driven Carbon Reduction Strategy)
    AI-based carbon reduction recommendations
    """
    _name = 'agri.supply.chain.carbon.reduction.strategy'
    _description = 'AI-driven Supply Chain Carbon Reduction Strategy'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Reduction Strategy', required=True, copy=False)
    strategy_date = fields.Date('Strategy Date', default=fields.Date.context_today)

    # Strategy type
    strategy_type = fields.Selection([
        ('transportation', 'Transportation Optimization'),
        ('supplier_selection', 'Low-Carbon Supplier Selection'),
        ('packaging', 'Sustainable Packaging'),
        ('route_optimization', 'Route Optimization'),
        ('energy_efficiency', 'Energy Efficiency'),
        ('process_optimization', 'Process Optimization'),
    ], string='Strategy Type', required=True, default='transportation')

    # Carbon impact analysis
    current_emissions = fields.Float('Current Emissions (tCO2e)')
    projected_emissions = fields.Float('Projected Emissions (tCO2e) after Implementation')
    potential_reduction = fields.Float('Potential Reduction (tCO2e)', compute='_compute_reduction', store=True)
    reduction_percentage = fields.Float('Reduction Percentage (%)', compute='_compute_reduction_percentage', store=True)

    # AI recommendation details
    ai_recommendation = fields.Text('AI Recommendation')
    recommendation_confidence = fields.Float('Recommendation Confidence (0-100%)')
    implementation_complexity = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Implementation Complexity', default='medium')

    # ROI calculations
    implementation_cost = fields.Float('Implementation Cost')
    annual_savings = fields.Float('Annual Savings')
    payback_period_months = fields.Float('Payback Period (Months)', compute='_compute_roi', store=True)
    roi_percentage = fields.Float('ROI (%)', compute='_compute_roi', store=True)

    # Implementation tracking
    implementation_status = fields.Selection([
        ('recommended', 'Recommended'),
        ('planning', 'Planning'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ], string='Implementation Status', default='recommended')

    # Related entities
    partner_id = fields.Many2one('res.partner', string='Supplier/Partner')
    product_category_id = fields.Many2one('product.category', string='Product Category')
    logistics_route_id = fields.Many2one('stock.route', string='Logistics Route')

    # Performance metrics
    effectiveness_score = fields.Float('Effectiveness Score (0-100)',
                                       help='Expected effectiveness of the strategy')

    @api.depends('current_emissions', 'projected_emissions')
    def _compute_reduction(self):
        for record in self:
            if record.current_emissions and record.projected_emissions:
                record.potential_reduction = record.current_emissions - record.projected_emissions
            else:
                record.potential_reduction = 0.0

    @api.depends('current_emissions', 'projected_emissions')
    def _compute_reduction_percentage(self):
        for record in self:
            if record.current_emissions and record.current_emissions != 0:
                reduction = (record.current_emissions - record.projected_emissions) / record.current_emissions * 100
                record.reduction_percentage = max(0, reduction)  # Ensure non-negative
            else:
                record.reduction_percentage = 0.0

    @api.depends('implementation_cost', 'annual_savings')
    def _compute_roi(self):
        for record in self:
            if record.implementation_cost and record.implementation_cost != 0:
                if record.annual_savings:
                    record.roi_percentage = (record.annual_savings / record.implementation_cost) * 100
                    record.payback_period_months = (record.implementation_cost / record.annual_savings) * 12
                else:
                    record.roi_percentage = 0.0
                    record.payback_period_months = 0.0
            else:
                record.roi_percentage = 0.0
                record.payback_period_months = 0.0

    @api.constrains('current_emissions', 'projected_emissions', 'implementation_cost', 'annual_savings')
    def _check_positive_values(self):
        for record in self:
            if record.current_emissions < 0 or record.projected_emissions < 0:
                raise ValidationError(_("Emissions values cannot be negative."))
            if record.implementation_cost < 0 or record.annual_savings < 0:
                raise ValidationError(_("Cost and savings values cannot be negative."))

    def action_generate_ai_recommendation(self):
        """Generate AI-based carbon reduction recommendations"""
        for record in self:
            # This would integrate with AI models in real implementation
            # For now, we'll generate sample recommendations based on strategy type
            recommendations = {
                'transportation': "Optimize delivery routes using shortest path algorithms, consolidate shipments, and use electric/hybrid vehicles for last-mile delivery.",
                'supplier_selection': "Switch to suppliers with certified carbon neutral operations and renewable energy usage. Evaluate suppliers based on verified carbon footprint data.",
                'packaging': "Replace plastic packaging with compostable alternatives, reduce packaging size, and use recycled materials.",
                'route_optimization': "Implement dynamic routing algorithms to minimize distance and fuel consumption based on real-time traffic conditions.",
                'energy_efficiency': "Install smart energy management systems and LED lighting in warehouses. Implement demand response programs during peak hours.",
                'process_optimization': "Optimize production processes to reduce energy consumption and waste. Implement lean manufacturing principles."
            }

            record.ai_recommendation = recommendations.get(record.strategy_type, "AI recommendation for carbon reduction")
            record.recommendation_confidence = 85.0  # Placeholder confidence
            record.effectiveness_score = 75.0  # Placeholder effectiveness

            record.message_post(body=_("AI Carbon Reduction Strategy generated: %s") % record.ai_recommendation)

    def action_implement_strategy(self):
        """Mark strategy for implementation"""
        for record in self:
            record.implementation_status = 'in_progress'
            record.message_post(body=_("Carbon reduction strategy implementation started. Expected reduction: %.2f tCO2e") %
                              record.potential_reduction)

    def action_complete_implementation(self):
        """Mark strategy implementation as completed"""
        for record in self:
            record.implementation_status = 'completed'
            record.message_post(body=_("Carbon reduction strategy implementation completed."))


class AgriSupplierCarbonCompliance(models.Model):
    """
    US-076-03: 供应商碳合规管理 (Supplier Carbon Compliance Management)
    Management of supplier carbon compliance
    """
    _name = 'agri.supplier.carbon.compliance'
    _description = 'Supplier Carbon Compliance Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Supplier Carbon Compliance Record', required=True, copy=False)
    compliance_date = fields.Date('Compliance Date', default=fields.Date.context_today)

    # Supplier information
    partner_id = fields.Many2one('res.partner', string='Supplier', required=True,
                                 domain=[('supplier_rank', '>', 0)])
    supplier_category = fields.Selection([
        ('primary', 'Primary Supplier'),
        ('secondary', 'Secondary Supplier'),
        ('service', 'Service Provider'),
        ('logistics', 'Logistics Provider'),
    ], string='Supplier Category', default='primary')

    # Carbon compliance metrics
    carbon_footprint_tco2e = fields.Float('Carbon Footprint (tCO2e)')
    carbon_intensity_kgco2e_per_kg = fields.Float('Carbon Intensity (kgCO2e/kg)')
    carbon_reduction_target = fields.Float('Carbon Reduction Target (%)')
    achieved_reduction = fields.Float('Achieved Reduction (%)')

    # Compliance tracking
    compliance_status = fields.Selection([
        ('compliant', 'Compliant'),
        ('partial_compliant', 'Partial Compliant'),
        ('non_compliant', 'Non-Compliant'),
        ('pending', 'Pending'),
    ], string='Compliance Status', compute='_compute_compliance_status', store=True)

    # Certification and verification
    carbon_certification_ids = fields.Many2many('farm.certification',
                                               string='Carbon Certifications')
    verification_date = fields.Date('Last Verification Date')
    next_verification_date = fields.Date('Next Verification Date')

    # Scorecard and rating
    supplier_carbon_score = fields.Float('Supplier Carbon Score (0-100)',
                                         compute='_compute_carbon_score', store=True)
    carbon_performance_rating = fields.Selection([
        ('excellent', 'Excellent (90-100)'),
        ('good', 'Good (70-89)'),
        ('average', 'Average (50-69)'),
        ('poor', 'Poor (0-49)'),
    ], string='Performance Rating', compute='_compute_performance_rating', store=True)

    # Improvement plans
    improvement_plan = fields.Text('Improvement Plan')
    target_date_for_improvement = fields.Date('Target Date for Improvement')

    # Incentive programs
    incentive_eligible = fields.Boolean('Eligible for Incentives',
                                        compute='_compute_incentive_eligibility', store=True)
    incentive_programs = fields.Text('Available Incentive Programs')

    # Historical data
    historical_compliance_ids = fields.One2many('agri.supplier.carbon.historical', 'compliance_id',
                                                string='Historical Compliance Data')

    @api.depends('carbon_footprint_tco2e', 'carbon_intensity_kgco2e_per_kg',
                 'carbon_reduction_target', 'achieved_reduction')
    def _compute_compliance_status(self):
        for record in self:
            if record.carbon_footprint_tco2e and record.carbon_footprint_tco2e < 100.0:  # Example threshold
                record.compliance_status = 'compliant'
            elif record.achieved_reduction and record.achieved_reduction >= record.carbon_reduction_target * 0.8:
                record.compliance_status = 'partial_compliant'
            elif record.carbon_footprint_tco2e and record.carbon_footprint_tco2e > 500.0:  # Example threshold
                record.compliance_status = 'non_compliant'
            else:
                record.compliance_status = 'pending'

    @api.depends('carbon_footprint_tco2e', 'carbon_intensity_kgco2e_per_kg',
                 'achieved_reduction', 'carbon_reduction_target')
    def _compute_carbon_score(self):
        for record in self:
            # Calculate carbon score based on various factors
            base_score = 100.0

            # Reduce score based on carbon footprint (inverse relationship)
            if record.carbon_footprint_tco2e:
                footprint_impact = min(50, record.carbon_footprint_tco2e / 10)  # Example calculation
                base_score -= footprint_impact

            # Adjust based on carbon intensity
            if record.carbon_intensity_kgco2e_per_kg:
                intensity_impact = min(30, record.carbon_intensity_kgco2e_per_kg * 5)  # Example calculation
                base_score -= intensity_impact

            # Add score for achieving reduction targets
            if record.achieved_reduction and record.carbon_reduction_target:
                achievement_bonus = min(20, (record.achieved_reduction / record.carbon_reduction_target) * 20)
                base_score += achievement_bonus

            record.supplier_carbon_score = max(0, min(100, base_score))

    @api.depends('supplier_carbon_score')
    def _compute_performance_rating(self):
        for record in self:
            if record.supplier_carbon_score >= 90:
                record.carbon_performance_rating = 'excellent'
            elif record.supplier_carbon_score >= 70:
                record.carbon_performance_rating = 'good'
            elif record.supplier_carbon_score >= 50:
                record.carbon_performance_rating = 'average'
            else:
                record.carbon_performance_rating = 'poor'

    @api.depends('supplier_carbon_score', 'compliance_status')
    def _compute_incentive_eligibility(self):
        for record in self:
            record.incentive_eligible = (record.supplier_carbon_score >= 70 and
                                        record.compliance_status in ['compliant', 'partial_compliant'])

    @api.constrains('carbon_footprint_tco2e', 'carbon_intensity_kgco2e_per_kg',
                    'carbon_reduction_target', 'achieved_reduction')
    def _check_positive_values(self):
        for record in self:
            if record.carbon_footprint_tco2e and record.carbon_footprint_tco2e < 0:
                raise ValidationError(_("Carbon footprint cannot be negative."))
            if record.carbon_intensity_kgco2e_per_kg and record.carbon_intensity_kgco2e_per_kg < 0:
                raise ValidationError(_("Carbon intensity cannot be negative."))
            if record.carbon_reduction_target and record.carbon_reduction_target < 0:
                raise ValidationError(_("Carbon reduction target cannot be negative."))
            if record.achieved_reduction and record.achieved_reduction < 0:
                raise ValidationError(_("Achieved reduction cannot be negative."))

    def action_create_improvement_plan(self):
        """Create an improvement plan for non-compliant suppliers"""
        for record in self:
            if record.compliance_status == 'non_compliant':
                plan = f"""
                Carbon Compliance Improvement Plan for {record.partner_id.name}

                Current Status: Non-Compliant
                Current Carbon Footprint: {record.carbon_footprint_tco2e} tCO2e
                Carbon Intensity: {record.carbon_intensity_kgco2e_per_kg} kgCO2e/kg

                Recommendations:
                1. Implement energy efficiency measures in production processes
                2. Switch to renewable energy sources
                3. Optimize transportation and logistics
                4. Adopt circular economy practices
                5. Obtain carbon neutral certification

                Target: Achieve compliance within 12 months
                """
                record.improvement_plan = plan
                record.target_date_for_improvement = fields.Date.add(
                    fields.Date.context_today(record), months=12)
                record.message_post(body=_("Improvement plan created for supplier carbon compliance."))

    def action_generate_incentive_programs(self):
        """Generate incentive programs for compliant suppliers"""
        for record in self:
            if record.incentive_eligible:
                incentives = f"""
                Incentive Programs for {record.partner_id.name} (Score: {record.supplier_carbon_score})

                Available Programs:
                1. Preferred supplier status for future contracts
                2. Extended payment terms (30 days)
                3. Volume discounts for high-volume orders
                4. Joint carbon reduction projects funding
                5. Marketing benefits as green supplier
                """
                record.incentive_programs = incentives
                record.message_post(body=_("Incentive programs generated for compliant supplier."))

    def action_update_compliance_status(self):
        """Manually update compliance status"""
        for record in self:
            # Recompute all dependent fields
            record._compute_compliance_status()
            record._compute_carbon_score()
            record._compute_performance_rating()
            record._compute_incentive_eligibility()
            record.message_post(body=_("Compliance status updated. Current status: %s") %
                              dict(record._fields['compliance_status'].selection).get(record.compliance_status))


class AgriSupplierCarbonHistorical(models.Model):
    """
    Historical data for supplier carbon compliance tracking
    """
    _name = 'agri.supplier.carbon.historical'
    _description = 'Historical Supplier Carbon Compliance Data'

    compliance_id = fields.Many2one('agri.supplier.carbon.compliance', string='Compliance Record', required=True)
    historical_date = fields.Date('Date', required=True)
    carbon_footprint_tco2e = fields.Float('Carbon Footprint (tCO2e)')
    carbon_intensity_kgco2e_per_kg = fields.Float('Carbon Intensity (kgCO2e/kg)')
    achieved_reduction = fields.Float('Achieved Reduction (%)')
    compliance_status = fields.Selection([
        ('compliant', 'Compliant'),
        ('partial_compliant', 'Partial Compliant'),
        ('non_compliant', 'Non-Compliant'),
        ('pending', 'Pending'),
    ], string='Compliance Status')


class AgriCarbonNeutralityCertification(models.Model):
    """
    US-076-04: 碳中和认证与报告 (Carbon Neutrality Certification & Reporting)
    Carbon neutrality certification and reporting
    """
    _name = 'agri.carbon.neutrality.certification'
    _description = 'Carbon Neutrality Certification and Reporting'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Certification Name', required=True, copy=False)
    certification_date = fields.Date('Certification Date', default=fields.Date.context_today)

    # Certification type
    certification_type = fields.Selection([
        ('carbon_neutral', 'Carbon Neutral'),
        ('net_zero', 'Net Zero'),
        ('climate_positive', 'Climate Positive'),
        ('carbon_negative', 'Carbon Negative'),
    ], string='Certification Type', required=True, default='carbon_neutral')

    # Scope and coverage
    certification_scope = fields.Selection([
        ('product', 'Product Level'),
        ('facility', 'Facility/Location'),
        ('organization', 'Organization Wide'),
        ('supply_chain', 'Supply Chain'),
        ('product_lifecycle', 'Product Lifecycle'),
    ], string='Certification Scope', required=True, default='organization')

    # Carbon balance
    total_emissions = fields.Float('Total Emissions (tCO2e)', help='Total carbon emissions in scope')
    total_removals = fields.Float('Total Removals (tCO2e)', help='Total carbon removals/offsets')
    net_balance = fields.Float('Net Balance (tCO2e)', compute='_compute_net_balance', store=True)
    is_carbon_neutral = fields.Boolean('Is Carbon Neutral', compute='_compute_carbon_neutral', store=True)

    # Verification and certification
    verification_body = fields.Char('Verification Body')
    verification_date = fields.Date('Verification Date')
    certification_number = fields.Char('Certification Number')
    certification_expires = fields.Date('Certification Expiry Date')

    # Offset information
    offset_projects = fields.Text('Carbon Offset Projects')
    offset_certification_standards = fields.Text('Offset Certification Standards')

    # Third party certification
    third_party_certifier = fields.Many2one('res.partner', string='Third Party Certifier',
                                           domain=[('is_certification_body', '=', True)])
    certification_standard = fields.Selection([
        ('pascal', 'PAS 2060'),
        ('ghgp', 'GHG Protocol'),
        ('iso_14064', 'ISO 14064'),
        ('vcs', 'Verified Carbon Standard'),
        ('gold', 'Gold Standard'),
        ('climate_action', 'Climate Action Reserve'),
        ('custom', 'Custom Standard'),
    ], string='Certification Standard')

    # Reporting
    compliance_report = fields.Text('Compliance Report', compute='_compute_compliance_report')
    verification_report = fields.Binary('Verification Report', attachment=True)
    verification_report_name = fields.Char('Report Name')

    # Status and timeline
    certification_status = fields.Selection([
        ('applied', 'Applied'),
        ('under_review', 'Under Review'),
        ('pending', 'Pending'),
        ('certified', 'Certified'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked'),
    ], string='Certification Status', default='applied', required=True)

    # Related data
    carbon_data_ids = fields.Many2many('agri.supply.chain.carbon.data.engine',
                                       string='Related Carbon Data')

    @api.depends('total_emissions', 'total_removals')
    def _compute_net_balance(self):
        for record in self:
            record.net_balance = (record.total_removals or 0) - (record.total_emissions or 0)

    @api.depends('net_balance')
    def _compute_carbon_neutral(self):
        for record in self:
            record.is_carbon_neutral = abs(record.net_balance) <= 0.01  # Allow for small rounding differences

    def _compute_compliance_report(self):
        """Generate a compliance report for the certification"""
        for record in self:
            report = f"""
            Carbon Neutrality Certification Report: {record.name}

            Type: {dict(record._fields['certification_type'].selection).get(record.certification_type, record.certification_type)}
            Scope: {dict(record._fields['certification_scope'].selection).get(record.certification_scope, record.certification_scope)}
            Date: {record.certification_date}

            Carbon Balance:
            - Total Emissions: {record.total_emissions or 0} tCO2e
            - Total Removals: {record.total_removals or 0} tCO2e
            - Net Balance: {record.net_balance or 0} tCO2e
            - Carbon Neutral Status: {'Yes' if record.is_carbon_neutral else 'No'}

            Verification:
            - Verification Body: {record.verification_body or 'N/A'}
            - Verification Date: {record.verification_date or 'N/A'}
            - Certification Number: {record.certification_number or 'N/A'}
            - Expires: {record.certification_expires or 'N/A'}

            Standards: {dict(record._fields['certification_standard'].selection).get(record.certification_standard, record.certification_standard) or 'N/A'}
            """
            record.compliance_report = report

    @api.constrains('total_emissions', 'total_removals')
    def _check_positive_values(self):
        for record in self:
            if record.total_emissions and record.total_emissions < 0:
                raise ValidationError(_("Total emissions cannot be negative."))
            if record.total_removals and record.total_removals < 0:
                raise ValidationError(_("Total removals cannot be negative."))

    def action_apply_certification(self):
        """Apply for carbon neutrality certification"""
        for record in self:
            record.certification_status = 'applied'
            record.message_post(body=_("Carbon neutrality certification application submitted."))

    def action_start_review(self):
        """Start the certification review process"""
        for record in self:
            record.certification_status = 'under_review'
            record.message_post(body=_("Carbon neutrality certification review started."))

    def action_issue_certification(self):
        """Issue the carbon neutrality certification"""
        for record in self:
            if not record.is_carbon_neutral:
                raise ValidationError(_("Cannot issue certification: entity is not carbon neutral."))
            record.certification_status = 'certified'
            record.certification_number = self.env['ir.sequence'].next_by_code('carbon.neutrality.certification') or '/'
            record.certification_expires = fields.Date.add(fields.Date.context_today(record), years=1)
            record.message_post(body=_("Carbon neutrality certification issued. Number: %s") % record.certification_number)

    def action_verify_data(self):
        """Verify carbon data for certification"""
        for record in self:
            if not record.total_emissions:
                raise ValidationError(_("Total emissions must be specified before verification."))
            record.verification_date = fields.Date.context_today(record)
            record.certification_status = 'pending'
            record.message_post(body=_("Carbon data verified. Awaiting final certification decision."))

    def action_expire_certification(self):
        """Mark certification as expired"""
        for record in self:
            if record.certification_expires and record.certification_expires < fields.Date.context_today(record):
                record.certification_status = 'expired'
                record.message_post(body=_("Carbon neutrality certification has expired."))

    def action_generate_compliance_report(self):
        """Generate detailed compliance report"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Carbon Neutrality Compliance Report'),
            'res_model': 'agri.carbon.neutrality.certification',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'context': self.env.context,
        }