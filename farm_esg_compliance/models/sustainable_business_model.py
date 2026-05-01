from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class AgriSustainableBusinessModel(models.Model):
    """
    US-101-02: Multi-scale Sustainable Business Model Design
    A model for designing multi-scale sustainable business models covering single farms, cooperatives, spatial neighborhoods, and administrative regions.
    """
    _name = 'agri.sustainable.business.model'
    _description = 'Agricultural Sustainable Business Model'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Business Model Name', required=True)
    code = fields.Char('Business Model Code', required=True, copy=False)
    description = fields.Text('Description')

    scale_level = fields.Selection([
        ('single_farm', 'Single Farm'),
        ('cooperative', 'Cooperative'),
        ('spatial_neighborhood', 'Spatial Neighborhood'),
        ('administrative_region', 'Administrative Region'),
    ], string='Scale Level', required=True)

    # Triple Bottom Line Metrics (US-101-01)
    economic_performance_score = fields.Float('Economic Performance Score (0-100)',
                                             help='Financial performance indicator')
    environmental_impact_score = fields.Float('Environmental Impact Score (0-100)',
                                              help='Environmental sustainability indicator')
    social_responsibility_score = fields.Float('Social Responsibility Score (0-100)',
                                               help='Social impact indicator')

    # Business model characteristics
    business_type = fields.Selection([
        ('traditional', 'Traditional Agriculture'),
        ('organic', 'Organic Agriculture'),
        ('biodynamic', 'Biodynamic Agriculture'),
        ('precision', 'Precision Agriculture'),
        ('regenerative', 'Regenerative Agriculture'),
        ('circular', 'Circular Agriculture'),
    ], string='Business Type', required=True)

    # Integration with financial and sustainability metrics
    expected_roi = fields.Float('Expected ROI (%)')
    payback_period_years = fields.Float('Expected Payback Period (Years)')

    # Spatial aggregation using PostGIS (US-101-02 requirement)
    has_geographic_coverage = fields.Boolean('Has Geographic Coverage')
    geographic_description = fields.Text('Geographic Coverage Description')

    # Integration with sales growth, resource conservation, circular economy
    sales_growth_target = fields.Float('Sales Growth Target (%)')
    resource_efficiency_improvement = fields.Float('Resource Efficiency Improvement (%)')
    circular_economy_integration = fields.Boolean('Circular Economy Integration')

    # Impact assessment for business decisions
    environmental_impact_assessment = fields.Text('Environmental Impact Assessment')
    social_impact_assessment = fields.Text('Social Impact Assessment')

    # Status and lifecycle
    status = fields.Selection([
        ('draft', 'Draft'),
        ('in_design', 'In Design'),
        ('pilot', 'Pilot'),
        ('implemented', 'Implemented'),
        ('optimized', 'Optimized'),
        ('deprecated', 'Deprecated'),
    ], string='Status', default='draft')

    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')

    # Related entities
    related_farm_ids = fields.Many2many('farm.location', string='Related Farms')
    related_cooperative_id = fields.Many2one('res.partner', string='Related Cooperative')
    related_region_id = fields.Many2one('res.country.state', string='Related Region')

    # Optimization suggestions
    optimization_suggestions = fields.Text('Optimization Suggestions')
    reasoning_path = fields.Text('Reasoning Path for Optimization')

    # Integration with AI decision for optimization
    ai_recommendations = fields.Text('AI Recommendations')

    _code_unique = models.Constraint(
        'UNIQUE(code)',
        'Business model code must be unique.'
    )

    @api.model
    def create(self, vals):
        if 'code' not in vals or not vals['code']:
            vals['code'] = self.env['ir.sequence'].next_by_code('agri.sustainable.business.model') or '/'
        return super().create(vals)

    def action_calculate_triple_bottom_line(self):
        """Calculate the triple bottom line metrics using PostGIS aggregation [US-101-02]"""
        for record in self:
            if record.related_farm_ids:
                algo = self.env['agri.sustainability.algorithms']
                record.environmental_impact_score = algo.perform_spatial_union_aggregation(
                    record.related_farm_ids.ids, 'environmental_impact')
                record.social_responsibility_score = algo.perform_spatial_union_aggregation(
                    record.related_farm_ids.ids, 'social_impact')
                record.economic_performance_score = algo.perform_spatial_union_aggregation(
                    record.related_farm_ids.ids, 'economic_impact')
            else:
                # Fallback to manual estimate if no farms linked
                record.economic_performance_score = min(100, max(0, (record.expected_roi / 20.0) * 100 if record.expected_roi else 50))

    def action_evaluate_impact(self):
        """Evaluate the environmental and social impact of business decisions"""
        for record in self:
            # Environmental impact evaluation
            environmental_impact = f"""
- Resource efficiency improvement: {record.resource_efficiency_improvement}%
- Circular economy integration: {'Yes' if record.circular_economy_integration else 'No'}
- Expected ROI: {record.expected_roi}%
- Payback period: {record.payback_period_years} years
            """

            # Social impact evaluation
            social_impact = f"""
- Impact on local community: {record.business_type} approach
- Cooperative involvement: {'Yes' if record.related_cooperative_id else 'No'}
- Regional development: {record.scale_level} level
            """

            record.environmental_impact_assessment = environmental_impact
            record.social_impact_assessment = social_impact

    def action_generate_optimization_suggestions(self):
        """Generate optimization suggestions based on triple bottom line"""
        for record in self:
            suggestions = []
            reasoning = []

            if record.economic_performance_score < 60:
                suggestions.append("Focus on improving economic performance through cost optimization and revenue enhancement.")
                reasoning.append("Economic score below 60 indicates need for financial improvements.")

            if record.environmental_impact_score < 60:
                suggestions.append("Implement more sustainable practices to improve environmental score.")
                reasoning.append("Environmental score below 60 indicates need for sustainability improvements.")

            if record.social_responsibility_score < 60:
                suggestions.append("Enhance community engagement and social impact initiatives.")
                reasoning.append("Social score below 60 indicates need for social responsibility improvements.")

            if record.payback_period_years > 5:
                suggestions.append("Consider investments with shorter payback periods.")
                reasoning.append("Payback period exceeds 5 years, suggesting longer-term risk.")

            record.optimization_suggestions = '\n'.join(suggestions) if suggestions else "No specific optimization suggestions at this time."
            record.reasoning_path = '\n'.join(reasoning) if reasoning else "No specific reasoning path identified."

    def action_implement_model(self):
        """Change status to implemented"""
        self.write({'status': 'implemented'})

    def action_optimize_model(self):
        """Change status to optimized"""
        self.write({'status': 'optimized'})

    def action_generate_ai_recommendations(self):
        """Generate AI-based recommendations for business model optimization"""
        for record in self:
            # This would typically call an AI service, but for now we'll simulate
            recommendations = []

            if record.business_type == 'traditional':
                recommendations.append("Consider transitioning to regenerative agriculture practices for better environmental impact.")

            if record.resource_efficiency_improvement < 20:
                recommendations.append("Implement precision agriculture technologies to improve resource efficiency.")

            if record.circular_economy_integration == False:
                recommendations.append("Explore circular economy opportunities such as composting, biogas production, or input recycling.")

            if record.payback_period_years > 3:
                recommendations.append("Consider phased implementation to reduce financial risk and improve payback period.")

            record.ai_recommendations = '\n'.join(recommendations) if recommendations else "No specific AI recommendations at this time."