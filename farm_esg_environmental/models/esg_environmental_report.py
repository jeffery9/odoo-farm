from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ESGEnvironmentalReport(models.Model):
    """
    US-30-XX: ESG Environmental Report
    ESG Environmental reporting that extends base ESG functionality with environmental data
    """
    _name = 'esg.environmental.report'
    _description = 'ESG Environmental Report'
    _inherit = ['esg.performance.report']  # Inherit from base ESG performance report

    # Environmental-specific fields
    carbon_footprint_tco2e = fields.Float('Carbon Footprint (tCO2e)', help='Total carbon footprint in tons CO2 equivalent')
    water_stress_score = fields.Float('Water Stress Score (0-100)', help='Water stress score for the area')
    biodiversity_risk_score = fields.Float('Biodiversity Risk Score (0-100)', help='Risk score for biodiversity impact')

    # Environmental assessment references (extending the base assessment_ids field)
    environmental_assessment_ids = fields.Many2many(
        'farm.ecology.environment.impact.assessment',
        string='Related Environmental Assessments',
        help='Environmental assessments from ecological module'
    )
    biodiversity_tracking_ids = fields.Many2many(
        'farm.ecology.biodiversity.tracking',
        string='Related Biodiversity Tracking',
        help='Biodiversity tracking records from ecological module'
    )
    water_efficiency_ids = fields.Many2many(
        'farm.ecology.water.efficiency.monitoring',
        string='Related Water Efficiency Records',
        help='Water efficiency records from ecological module'
    )

    # Environmental-specific metrics that extend base functionality
    total_environmental_assessments = fields.Integer('Total Environmental Assessments', compute='_compute_environmental_metrics')
    avg_overall_impact = fields.Float('Average Overall Impact Score', compute='_compute_environmental_metrics')
    avg_shannon_diversity = fields.Float('Average Shannon Diversity Index', compute='_compute_biodiversity_metrics')
    avg_water_use_efficiency = fields.Float('Average Water Use Efficiency', compute='_compute_water_metrics')

    @api.depends('environmental_assessment_ids')
    def _compute_environmental_metrics(self):
        """Compute aggregated environmental impact metrics"""
        for record in self:
            if record.environmental_assessment_ids:
                record.total_environmental_assessments = len(record.environmental_assessment_ids)
                # Calculate average overall impact from related assessments
                avg_impact = sum(record.environmental_assessment_ids.mapped('overall_environmental_impact_score')) / len(record.environmental_assessment_ids)
                record.avg_overall_impact = avg_impact
            else:
                # If no specific assessments, find them by date/period
                assessments = self.env['farm.ecology.environment.impact.assessment'].search([
                    ('assessment_date', '>=', fields.Date.start_of(record.report_date, 'year' if record.report_period == 'annually' else 'quarter')),
                    ('assessment_date', '<=', fields.Date.end_of(record.report_date, 'year' if record.report_period == 'annually' else 'quarter')),
                ])
                record.total_environmental_assessments = len(assessments)
                if assessments:
                    avg_impact = sum(assessments.mapped('overall_environmental_impact_score')) / len(assessments)
                    record.avg_overall_impact = avg_impact
                else:
                    record.avg_overall_impact = 0.0

            # Update the base environmental score based on computed metrics
            # Lower impact scores are better (normalized to 0-100 scale where higher is better)
            impact_score = max(0, 100 - (record.avg_overall_impact or 0))
            # Higher diversity scores are better
            diversity_score = min(100, (record.avg_shannon_diversity or 0) * 10)
            # Higher efficiency scores are better
            efficiency_score = min(100, (record.avg_water_use_efficiency or 0) * 20)
            # Weighted average for environmental score
            record.environmental_score = (impact_score * 0.4 + diversity_score * 0.3 + efficiency_score * 0.3)

    @api.depends('biodiversity_tracking_ids')
    def _compute_biodiversity_metrics(self):
        """Compute aggregated biodiversity metrics"""
        for record in self:
            if record.biodiversity_tracking_ids:
                avg_diversity = sum(record.biodiversity_tracking_ids.mapped('shannon_diversity_index')) / len(record.biodiversity_tracking_ids) if len(record.biodiversity_tracking_ids) > 0 else 0.0
                record.avg_shannon_diversity = avg_diversity
            else:
                # If no specific records, find them by date/period
                biodiversity_records = self.env['farm.ecology.biodiversity.tracking'].search([
                    ('tracking_date', '>=', fields.Date.start_of(record.report_date, 'year' if record.report_period == 'annually' else 'quarter')),
                    ('tracking_date', '<=', fields.Date.end_of(record.report_date, 'year' if record.report_period == 'annually' else 'quarter')),
                ])
                if biodiversity_records:
                    avg_diversity = sum(biodiversity_records.mapped('shannon_diversity_index')) / len(biodiversity_records)
                    record.avg_shannon_diversity = avg_diversity
                else:
                    record.avg_shannon_diversity = 0.0

    @api.depends('water_efficiency_ids')
    def _compute_water_metrics(self):
        """Compute aggregated water efficiency metrics"""
        for record in self:
            if record.water_efficiency_ids:
                avg_efficiency = sum(record.water_efficiency_ids.mapped('water_use_efficiency')) / len(record.water_efficiency_ids) if len(record.water_efficiency_ids) > 0 else 0.0
                record.avg_water_use_efficiency = avg_efficiency
            else:
                # If no specific records, find them by date/period
                water_records = self.env['farm.ecology.water.efficiency.monitoring'].search([
                    ('monitoring_date', '>=', fields.Date.start_of(record.report_date, 'year' if record.report_period == 'annually' else 'quarter')),
                    ('monitoring_date', '<=', fields.Date.end_of(record.report_date, 'year' if record.report_period == 'annually' else 'quarter')),
                ])
                if water_records:
                    avg_efficiency = sum(water_records.mapped('water_use_efficiency')) / len(water_records)
                    record.avg_water_use_efficiency = avg_efficiency
                else:
                    record.avg_water_use_efficiency = 0.0

    def action_generate_report(self):
        """Generate ESG environmental report based on ecological and base ESG data"""
        # Call the parent method first to handle base functionality
        super().action_generate_report()

        for record in self:
            # Link related environmental ecological records
            start_date = fields.Date.start_of(record.report_date, 'year' if record.report_period == 'annually' else 'quarter')
            end_date = fields.Date.end_of(record.report_date, 'year' if record.report_period == 'annually' else 'quarter')

            # Find related environmental assessments
            assessments = self.env['farm.ecology.environment.impact.assessment'].search([
                ('assessment_date', '>=', start_date),
                ('assessment_date', '<=', end_date),
            ])
            record.environmental_assessment_ids = [(6, 0, assessments.ids)]

            # Find related biodiversity records
            biodiversity_records = self.env['farm.ecology.biodiversity.tracking'].search([
                ('tracking_date', '>=', start_date),
                ('tracking_date', '<=', end_date),
            ])
            record.biodiversity_tracking_ids = [(6, 0, biodiversity_records.ids)]

            # Find related water efficiency records
            water_records = self.env['farm.ecology.water.efficiency.monitoring'].search([
                ('monitoring_date', '>=', start_date),
                ('monitoring_date', '<=', end_date),
            ])
            record.water_efficiency_ids = [(6, 0, water_records.ids)]

# Environmental Compliance - extends base ESG functionality properly
class ESGEnvironmentalCompliance(models.Model):
    """
    US-30-XX: ESG Environmental Compliance
    Environmental compliance tracking that extends base ESG compliance functionality
    """
    _name = 'esg.environmental.compliance'
    _description = 'ESG Environmental Compliance'
    _inherit = ['esg.assessment']  # Inherit from base ESG assessment

    # Override and specialize for environmental compliance
    assessment_type = fields.Selection(
        selection_add=[('environmental', 'Environmental')],
        default='environmental'
    )

    compliance_type = fields.Selection([
        ('iso_14001', 'ISO 14001 Environmental Management'),
        ('emission_standards', 'Emission Standards Compliance'),
        ('waste_management', 'Waste Management Compliance'),
        ('water_usage', 'Water Usage Compliance'),
        ('biodiversity_protection', 'Biodiversity Protection Compliance'),
        ('carbon_footprint', 'Carbon Footprint Compliance'),
        ('other', 'Other')
    ], string='Compliance Type', required=True)

    # Environmental-specific compliance data
    environmental_indicator_ids = fields.Many2many(
        'esg.indicator',
        domain=[('category', '=', 'environmental')],
        string='Environmental Indicators',
        help='Environmental indicators being measured for this compliance check'
    )

    carbon_emissions_tco2e = fields.Float('Carbon Emissions (tCO2e)', help='Total carbon emissions in tons CO2 equivalent')
    energy_consumption_kwh = fields.Float('Energy Consumption (kWh)', help='Total energy consumption in kilowatt-hours')
    waste_generation_kg = fields.Float('Waste Generation (kg)', help='Total waste generation in kilograms')

    environmental_risk_level = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ], string='Environmental Risk Level', compute='_compute_environmental_risk', store=True)

    # Compliance-specific fields that complement base assessment model
    certification_body = fields.Char('Certification Body')
    certification_number = fields.Char('Certification Number')
    scope_statement = fields.Text('Scope Statement', help='Description of what is within and outside the audit scope')
    non_compliance_issues = fields.Text('Non-Compliance Issues', help='Details of any non-compliance issues found')
    corrective_actions = fields.Text('Corrective Actions Required', help='Actions required to address non-compliance')

    @api.depends('carbon_emissions_tco2e', 'environmental_indicator_ids')
    def _compute_environmental_risk(self):
        """Compute environmental risk level based on various factors"""
        for record in self:
            risk_score = 0

            # Factor in carbon emissions (higher emissions = higher risk)
            if record.carbon_emissions_tco2e:
                if record.carbon_emissions_tco2e > 1000:  # Very high emissions
                    risk_score += 4
                elif record.carbon_emissions_tco2e > 500:  # High emissions
                    risk_score += 3
                elif record.carbon_emissions_tco2e > 100:  # Medium emissions
                    risk_score += 2
                else:  # Low emissions
                    risk_score += 1

            # Factor in compliance score from base class
            if record.overall_esg_score:
                if record.overall_esg_score < 40:
                    risk_score += 3
                elif record.overall_esg_score < 60:
                    risk_score += 2
                elif record.overall_esg_score < 80:
                    risk_score += 1

            # Map risk score to risk level
            if risk_score >= 6:
                record.environmental_risk_level = 'critical'
            elif risk_score >= 4:
                record.environmental_risk_level = 'high'
            elif risk_score >= 2:
                record.environmental_risk_level = 'medium'
            else:
                record.environmental_risk_level = 'low'

    def action_schedule_audit(self):
        """Schedule next ESG audit (specialized for environmental compliance)"""
        for record in self:
            if record.assessment_period == 'annually':
                next_audit = fields.Date.add(fields.Date.context_today(self), years=1)
            elif record.assessment_period == 'semi_annually':
                next_audit = fields.Date.add(fields.Date.context_today(self), months=6)
            elif record.assessment_period == 'quarterly':
                next_audit = fields.Date.add(fields.Date.context_today(self), months=3)
            else:  # monthly
                next_audit = fields.Date.add(fields.Date.context_today(self), months=1)

            record.assessment_date = next_audit  # Update the assessment date which is the base field