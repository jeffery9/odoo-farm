from odoo import models, fields, api
from odoo.exceptions import ValidationError


class StakeholderEngagement(models.Model):
    """
    US-082-04: 利益相关者参与度追踪
    Stakeholder Engagement tracking for ESG reporting
    """
    _name = 'farm.esg.stakeholder.engagement'
    _description = 'Stakeholder Engagement'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Engagement Activity', required=True)
    stakeholder_id = fields.Many2one('res.partner', 'Stakeholder', required=True)
    stakeholder_type = fields.Selection([
        'community', 'ngo', 'regulator', 'investor', 'customer', 'employee', 'supplier', 'other'
    ], string='Stakeholder Type', required=True)
    engagement_date = fields.Date('Engagement Date', required=True)
    engagement_type = fields.Selection([
        'meeting', 'survey', 'consultation', 'feedback_session', 'complaint', 'inquiry', 'other'
    ], string='Engagement Type', required=True)
    engagement_topic = fields.Selection([
        'environmental_impact', 'social_impact', 'governance', 'compliance', 'sustainability', 'other'
    ], string='Engagement Topic')
    communication_channel = fields.Selection([
        'in_person', 'virtual', 'written', 'survey', 'public_hearing', 'online', 'other'
    ], string='Communication Channel')
    participants_count = fields.Integer('Participants Count')
    outcome_summary = fields.Text('Outcome Summary')
    feedback_received = fields.Text('Feedback Received')
    action_items = fields.Text('Action Items')
    action_owner = fields.Many2one('res.users', 'Action Owner')
    action_deadline = fields.Date('Action Deadline')
    action_status = fields.Selection([
        'pending', 'in_progress', 'completed', 'cancelled'
    ], string='Action Status', default='pending')
    satisfaction_rating = fields.Selection([
        'very_satisfied', 'satisfied', 'neutral', 'dissatisfied', 'very_dissatisfied'
    ], string='Satisfaction Rating')
    follow_up_required = fields.Boolean('Follow Up Required')
    next_engagement_date = fields.Date('Next Engagement Date')
    report_year = fields.Integer('Report Year', default=lambda self: fields.Date.context_today(self).year)
    engagement_score = fields.Float('Engagement Score', help='Quantitative measure of engagement effectiveness')

    @api.model
    def get_engagement_summary(self, year=None):
        """Get stakeholder engagement summary for a year"""
        if year is None:
            year = fields.Date.context_today(self).year

        records = self.search([('report_year', '=', year)])

        if not records:
            return {
                'year': year,
                'total_engagements': 0,
                'total_participants': 0,
                'avg_engagement_score': 0.0,
                'stakeholder_breakdown': {},
                'engagement_by_type': {}
            }

        total_engagements = len(records)
        total_participants = sum(records.mapped('participants_count'))
        avg_engagement_score = sum(records.mapped('engagement_score')) / len(records) if records else 0.0

        # Breakdown by stakeholder type
        stakeholder_breakdown = {}
        for record in records:
            stakeholder_type = record.stakeholder_type
            if stakeholder_type not in stakeholder_breakdown:
                stakeholder_breakdown[stakeholder_type] = {
                    'count': 0,
                    'total_participants': 0,
                    'avg_score': 0.0
                }
            stakeholder_breakdown[stakeholder_type]['count'] += 1
            stakeholder_breakdown[stakeholder_type]['total_participants'] += record.participants_count or 0

        # Calculate avg scores per type
        for st_type, data in stakeholder_breakdown.items():
            type_records = records.filtered(lambda r: r.stakeholder_type == st_type)
            data['avg_score'] = sum(type_records.mapped('engagement_score')) / len(type_records) if type_records else 0.0

        # Breakdown by engagement type
        engagement_by_type = {}
        for record in records:
            eng_type = record.engagement_type
            if eng_type not in engagement_by_type:
                engagement_by_type[eng_type] = 0
            engagement_by_type[eng_type] += 1

        return {
            'year': year,
            'total_engagements': total_engagements,
            'total_participants': total_participants,
            'avg_engagement_score': avg_engagement_score,
            'stakeholder_breakdown': stakeholder_breakdown,
            'engagement_by_type': engagement_by_type,
            'detailed_records': records
        }

    def action_follow_up_required(self):
        """Mark engagement as requiring follow up"""
        for record in self:
            if record.satisfaction_rating in ['dissatisfied', 'very_dissatisfied']:
                record.follow_up_required = True
                record.next_engagement_date = fields.Date.add(fields.Date.context_today(self), days=30)