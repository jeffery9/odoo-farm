from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AgriESGKPI(models.Model):
    """
    US-082-05: ESG KPI仪表盘与对标分析
    ESG KPIs for dashboard and benchmarking
    """
    _name = 'agri.esg.kpi'
    _description = 'Agricultural ESG KPI'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('KPI Name', required=True)
    kpi_category = fields.Selection([
        'environmental', 'social', 'governance', 'financial'
    ], string='KPI Category', required=True)
    kpi_type = fields.Selection([
        'carbon_emissions', 'water_usage', 'waste_generation', 'biodiversity',
        'employee_safety', 'diversity', 'community_investment', 'governance_score',
        'compliance_rate', 'training_hours', 'local_procurement', 'other'
    ], string='KPI Type', required=True)
    reporting_period = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semi_annually', 'Semi-Annually'),
        ('annually', 'Annually')
    ], string='Reporting Period', required=True, default='annually')
    target_value = fields.Float('Target Value')
    current_value = fields.Float('Current Value')
    unit_of_measurement = fields.Char('Unit of Measurement', required=True)
    baseline_value = fields.Float('Baseline Value')
    achievement_percentage = fields.Float('Achievement %', compute='_compute_achievement_percentage', store=True, precompute=True)
    trend_indicator = fields.Selection([
        'increasing', 'decreasing', 'stable'
    ], string='Trend Indicator', compute='_compute_trend_indicator', store=True, precompute=True)
    year = fields.Integer('Year', default=lambda self: fields.Date.context_today(self).year)
    responsible_department = fields.Many2one('hr.department', 'Responsible Department')
    data_source = fields.Char('Data Source')
    calculation_method = fields.Text('Calculation Method')
    benchmark_value = fields.Float('Benchmark Value', help='Industry or regional benchmark')
    benchmark_source = fields.Char('Benchmark Source')
    variance_from_target = fields.Float('Variance from Target', compute='_compute_variance', store=True, precompute=True)
    performance_status = fields.Selection([
        'exceeding', 'on_track', 'at_risk', 'off_track'
    ], string='Performance Status', compute='_compute_performance_status', store=True, precompute=True)
    notes = fields.Text('Notes')

    @api.depends('current_value', 'target_value')
    def _compute_achievement_percentage(self):
        """Compute achievement percentage relative to target"""
        for record in self:
            if record.target_value and record.target_value != 0:
                record.achievement_percentage = (record.current_value / record.target_value) * 100
            else:
                record.achievement_percentage = 0.0

    @api.depends('current_value', 'baseline_value')
    def _compute_trend_indicator(self):
        """Compute trend indicator based on current vs baseline"""
        for record in self:
            if record.baseline_value is not None and record.current_value is not None:
                if record.current_value > record.baseline_value * 1.05:  # More than 5% increase
                    record.trend_indicator = 'increasing'
                elif record.current_value < record.baseline_value * 0.95:  # More than 5% decrease
                    record.trend_indicator = 'decreasing'
                else:
                    record.trend_indicator = 'stable'
            else:
                record.trend_indicator = 'stable'

    @api.depends('current_value', 'target_value')
    def _compute_variance(self):
        """Compute variance from target"""
        for record in self:
            record.variance_from_target = (record.current_value or 0) - (record.target_value or 0)

    @api.depends('achievement_percentage')
    def _compute_performance_status(self):
        """Compute performance status based on achievement percentage"""
        for record in self:
            if record.achievement_percentage >= 100:
                record.performance_status = 'exceeding'
            elif record.achievement_percentage >= 80:
                record.performance_status = 'on_track'
            elif record.achievement_percentage >= 60:
                record.performance_status = 'at_risk'
            else:
                record.performance_status = 'off_track'

    @api.model
    def get_kpi_dashboard_data(self, year=None, category=None):
        """Get KPI data for dashboard display"""
        if year is None:
            year = fields.Date.context_today(self).year

        domain = [('year', '=', year)]
        if category:
            domain.append(('kpi_category', '=', category))

        kpis = self.search(domain)

        if not kpis:
            return {
                'year': year,
                'category': category,
                'total_kpis': 0,
                'avg_achievement': 0.0,
                'on_track_count': 0,
                'at_risk_count': 0,
                'off_track_count': 0
            }

        total_kpis = len(kpis)
        avg_achievement = sum(kpis.mapped('achievement_percentage')) / len(kpis) if kpis else 0.0
        on_track_count = len(kpis.filtered(lambda k: k.performance_status == 'on_track' or k.performance_status == 'exceeding'))
        at_risk_count = len(kpis.filtered(lambda k: k.performance_status == 'at_risk'))
        off_track_count = len(kpis.filtered(lambda k: k.performance_status == 'off_track'))

        return {
            'year': year,
            'category': category,
            'total_kpis': total_kpis,
            'avg_achievement': avg_achievement,
            'on_track_count': on_track_count,
            'at_risk_count': at_risk_count,
            'off_track_count': off_track_count,
            'detailed_kpis': kpis
        }

    def action_reset_kpi_target(self):
        """Reset KPI to track against new target"""
        for record in self:
            record.baseline_value = record.current_value
            record.baseline_year = record.year