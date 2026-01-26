from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class SocialDiversityMetric(models.Model):
    """
    US-51-07: 工作场所多样性与包容性指标
    US-51-09: 社会责任指标跟踪
    Social and diversity metrics tracking
    """
    _name = 'farm.esg.social.diversity.metric'
    _description = 'Social and Diversity Metrics'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Metric Name', required=True)
    reporting_period = fields.Date('Reporting Period', required=True)
    gender_male_count = fields.Integer('Male Count')
    gender_female_count = fields.Integer('Female Count')
    gender_other_count = fields.Integer('Other Gender Count')
    age_under_30 = fields.Integer('Under 30 Years')
    age_30_to_50 = fields.Integer('30-50 Years')
    age_over_50 = fields.Integer('Over 50 Years')
    disability_employment = fields.Integer('Disability Employment Count')
    local_community_employment = fields.Integer('Local Community Employment')
    temporary_contract_count = fields.Integer('Temporary Contract Count')
    full_time_count = fields.Integer('Full Time Count')
    total_employees = fields.Integer('Total Employees', compute='_compute_total_employees', store=True)
    gender_balance_ratio = fields.Float('Gender Balance Ratio', compute='_compute_gender_balance_ratio', store=True)
    local_employment_ratio = fields.Float('Local Employment Ratio', compute='_compute_local_employment_ratio', store=True)

    @api.depends('gender_male_count', 'gender_female_count', 'gender_other_count')
    def _compute_total_employees(self):
        """Compute total employees"""
        for record in self:
            record.total_employees = record.gender_male_count + record.gender_female_count + record.gender_other_count

    @api.depends('gender_male_count', 'gender_female_count', 'total_employees')
    def _compute_gender_balance_ratio(self):
        """Compute gender balance ratio"""
        for record in self:
            if record.total_employees > 0:
                record.gender_balance_ratio = min(record.gender_male_count, record.gender_female_count) / max(record.gender_male_count, record.gender_female_count) if max(record.gender_male_count, record.gender_female_count) > 0 else 0.0
            else:
                record.gender_balance_ratio = 0.0

    @api.depends('local_community_employment', 'total_employees')
    def _compute_local_employment_ratio(self):
        """Compute local employment ratio"""
        for record in self:
            if record.total_employees > 0:
                record.local_employment_ratio = record.local_community_employment / record.total_employees
            else:
                record.local_employment_ratio = 0.0

    @api.model
    def get_diversity_report(self, year=None):
        """Generate diversity report for a specific year"""
        if year is None:
            year = fields.Date.context_today(self).year

        # Get all metrics for the year
        metrics = self.search([('reporting_period', 'like', f'{year}%')])

        if not metrics:
            return {
                'year': year,
                'total_reports': 0,
                'avg_gender_balance_ratio': 0.0,
                'avg_local_employment_ratio': 0.0,
                'total_employees': 0
            }

        total_employees = sum(metrics.mapped('total_employees'))
        avg_gender_balance = sum(metrics.mapped('gender_balance_ratio')) / len(metrics)
        avg_local_employment = sum(metrics.mapped('local_employment_ratio')) / len(metrics)

        return {
            'year': year,
            'total_reports': len(metrics),
            'avg_gender_balance_ratio': avg_gender_balance,
            'avg_local_employment_ratio': avg_local_employment,
            'total_employees': total_employees,
            'detailed_metrics': metrics
        }