from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class AgriTripleBottomLineMetrics(models.Model):
    """
    US-101-01: Triple Bottom Line Metrics Management
    Model for managing the three key sustainability metrics: economic, environmental, and social.
    """
    _name = 'agri.triple.bottom.line.metrics'
    _description = 'Agricultural Triple Bottom Line Metrics'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Metric Set Name', required=True)
    date = fields.Date('Date', required=True, default=fields.Date.context_today)

    # Economic metrics
    revenue = fields.Float('Revenue')
    profit = fields.Float('Profit')
    profit_margin = fields.Float('Profit Margin (%)', compute='_compute_profit_margin', store=True, precompute=True)
    roi = fields.Float('Return on Investment (%)')

    # Environmental metrics
    carbon_footprint_tco2e = fields.Float('Carbon Footprint (tCO2e)')
    water_usage_m3 = fields.Float('Water Usage (m3)')
    land_use_efficiency = fields.Float('Land Use Efficiency')
    resource_efficiency = fields.Float('Resource Efficiency (%)')

    # Social metrics
    jobs_created = fields.Integer('Jobs Created')
    community_investment = fields.Float('Community Investment')
    safety_incidents = fields.Integer('Safety Incidents')
    employee_satisfaction = fields.Float('Employee Satisfaction (0-10)')

    # Composite scores
    economic_score = fields.Float('Economic Score (0-100)', compute='_compute_economic_score', store=True, precompute=True)
    environmental_score = fields.Float('Environmental Score (0-100)', compute='_compute_environmental_score', store=True, precompute=True)
    social_score = fields.Float('Social Score (0-100)', compute='_compute_social_score', store=True, precompute=True)
    overall_sustainability_score = fields.Float('Overall Sustainability Score (0-100)', compute='_compute_overall_score', store=True, precompute=True)

    # Related entities
    farm_id = fields.Many2one('farm.location', string='Farm Location')
    period_type = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually'),
    ], string='Period Type', required=True, default='annually')

    # Integration with sustainability mixin
    _inherit = ['agri.sustainability.mixin']

    @api.depends('profit', 'revenue')
    def _compute_profit_margin(self):
        for record in self:
            if record.revenue and record.revenue != 0:
                record.profit_margin = (record.profit / record.revenue) * 100
            else:
                record.profit_margin = 0.0

    @api.depends('profit', 'revenue', 'roi')
    def _compute_economic_score(self):
        for record in self:
            # Calculate economic score based on revenue, profit, and ROI
            revenue_score = min(100, (record.revenue or 0) / 10000) if record.revenue else 0  # Normalize for comparison
            profit_score = min(100, (record.profit or 0) / 5000) if record.profit else 0
            roi_score = min(100, (record.roi or 0) * 2) if record.roi else 0  # ROI up to 50% would be 100 points

            record.economic_score = min(100, (revenue_score + profit_score + roi_score) / 3)

    @api.depends('carbon_footprint_tco2e', 'water_usage_m3', 'resource_efficiency')
    def _compute_environmental_score(self):
        for record in self:
            # Calculate environmental score based on environmental metrics
            # Lower carbon/water usage gets higher score, higher efficiency gets higher score
            carbon_score = max(0, 100 - ((record.carbon_footprint_tco2e or 0) * 10))  # Assume 0.1 tCO2e = 10 points
            water_score = max(0, 100 - ((record.water_usage_m3 or 0) / 100))  # Assume 100m3 = 10 points
            efficiency_score = min(100, (record.resource_efficiency or 0) * 2)  # Max efficiency of 50% = 100 points

            record.environmental_score = min(100, (carbon_score + water_score + efficiency_score) / 3)

    @api.depends('jobs_created', 'community_investment', 'safety_incidents', 'employee_satisfaction')
    def _compute_social_score(self):
        for record in self:
            # Calculate social score based on social metrics
            jobs_score = min(50, (record.jobs_created or 0) * 5)  # Max 50 points for jobs
            investment_score = min(30, (record.community_investment or 0) / 1000)  # Max 30 points for investment
            safety_score = 20 if (record.safety_incidents or 0) == 0 else max(0, 20 - (record.safety_incidents or 0) * 5)
            satisfaction_score = min(100, (record.employee_satisfaction or 0) * 10)  # Max 100 for perfect satisfaction

            record.social_score = min(100, (jobs_score + investment_score + safety_score + satisfaction_score) / 2)

    @api.depends('economic_score', 'environmental_score', 'social_score')
    def _compute_overall_score(self):
        for record in self:
            record.overall_sustainability_score = (record.economic_score + record.environmental_score + record.social_score) / 3

    @api.model
    def create(self, vals):
        record = super().create(vals)
        # Generate a report or notification when metrics are created
        record.message_post(body=_("Triple Bottom Line metrics recorded for %s") % record.date)
        return record

    def action_generate_comprehensive_report(self):
        """Generate a comprehensive sustainability report based on all three metrics"""
        self.ensure_one()
        report_content = f"""
        Triple Bottom Line Report for {self.name}
        ========================================

        Economic Performance:
        - Revenue: {self.revenue}
        - Profit: {self.profit}
        - ROI: {self.roi}%
        - Economic Score: {self.economic_score}/100

        Environmental Impact:
        - Carbon Footprint: {self.carbon_footprint_tco2e} tCO2e
        - Water Usage: {self.water_usage_m3} m³
        - Resource Efficiency: {self.resource_efficiency}%
        - Environmental Score: {self.environmental_score}/100

        Social Responsibility:
        - Jobs Created: {self.jobs_created}
        - Community Investment: {self.community_investment}
        - Safety Incidents: {self.safety_incidents}
        - Social Score: {self.social_score}/100

        Overall Sustainability Score: {self.overall_sustainability_score}/100
        """
        return {
            'type': 'ir.actions.act_window',
            'name': _('Triple Bottom Line Report'),
            'res_model': 'agri.triple.bottom.line.metrics',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'context': {'default_report_content': report_content}
        }