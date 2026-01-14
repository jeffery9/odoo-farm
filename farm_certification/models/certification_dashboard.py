from odoo import models, fields, api
from datetime import date, timedelta


class FarmCertificationDashboard(models.TransientModel):
    _name = 'farm.certification.dashboard'
    _description = 'Certification Compliance Dashboard'

    # Overall certification counts
    total_cert_count = fields.Integer(string="Total Certifications", compute='_compute_cert_counts')
    valid_cert_count = fields.Integer(string="Valid Certifications", compute='_compute_cert_counts')
    expired_cert_count = fields.Integer(string="Expired Certifications", compute='_compute_cert_counts')

    # GAP specific metrics
    gap_cert_count = fields.Integer(string="GAP Certifications", compute='_compute_cert_counts')
    organic_cert_count = fields.Integer(string="Organic Certifications", compute='_compute_cert_counts')
    gap_compliant_count = fields.Integer(string="GAP Compliant Locations", compute='_compute_gap_metrics')
    gap_audit_score_avg = fields.Float(string="Avg GAP Audit Score", compute='_compute_gap_metrics', digits=(10, 2))

    # Expiring certifications
    expiring_cert_count = fields.Integer(string="Expiring Soon", compute='_compute_expiring_certs')
    expiring_certs = fields.Many2many('farm.gap.certification', string="Expiring Certifications",
                                     compute='_compute_expiring_certs')

    @api.model
    def action_open_gap_certifications(self):
        """Open GAP certifications view"""
        return {
            'name': 'GAP Certifications',
            'type': 'ir.actions.act_window',
            'res_model': 'farm.gap.certification',
            'view_mode': 'tree,form',
            'domain': [('status', '!=', 'expired')],
            'context': self.env.context,
        }

    @api.model
    def action_open_organic_certifications(self):
        """Open organic certifications view"""
        return {
            'name': 'Organic Certifications',
            'type': 'ir.actions.act_window',
            'res_model': 'stock.location',
            'view_mode': 'tree,form',
            'domain': [('certification_level', 'in', ['organic', 'organic_transition'])],
            'context': self.env.context,
        }

    @api.model
    def action_open_expiring_certs(self):
        """Open expiring certifications view"""
        return {
            'name': 'Expiring Certifications',
            'type': 'ir.actions.act_window',
            'res_model': 'farm.gap.certification',
            'view_mode': 'tree,form',
            'domain': [('expiry_date', '<=', fields.Date.to_string(date.today() + timedelta(days=30))),
                      ('status', '!=', 'expired')],
            'context': self.env.context,
        }

    @api.model
    def action_open_all_certifications(self):
        """Open all certifications view"""
        return {
            'name': 'All Certifications',
            'type': 'ir.actions.act_window',
            'res_model': 'farm.gap.certification',
            'view_mode': 'tree,form',
            'context': self.env.context,
        }

    def _compute_cert_counts(self):
        """Compute overall certification counts"""
        for record in self:
            # Total certifications
            all_certs = self.env['farm.gap.certification'].search([])
            record.total_cert_count = len(all_certs)

            # Valid certifications
            valid_certs = all_certs.filtered(lambda c: c.status == 'valid')
            record.valid_cert_count = len(valid_certs)

            # Expired certifications
            expired_certs = all_certs.filtered(lambda c: c.status == 'expired')
            record.expired_cert_count = len(expired_certs)

            # GAP certifications
            gap_certs = all_certs
            record.gap_cert_count = len(gap_certs)

            # Organic certifications (from location model)
            organic_locations = self.env['stock.location'].search([
                ('certification_level', 'in', ['organic', 'organic_transition'])
            ])
            record.organic_cert_count = len(organic_locations)

    def _compute_gap_metrics(self):
        """Compute GAP-specific metrics"""
        for record in self:
            # GAP compliant locations (daily checks)
            today = date.today()
            last_week = today - timedelta(days=7)

            # Get daily compliance checks from the last week
            recent_checks = self.env['farm.gap.compliance.check'].search([
                ('date', '>=', last_week),
                ('overall_compliant', '=', True)
            ])

            record.gap_compliant_count = len(recent_checks)

            # Average GAP audit score
            recent_audits = self.env['farm.gap.audit'].search([
                ('audit_date', '>=', last_week)
            ])

            if recent_audits:
                avg_score = sum(audit.total_score for audit in recent_audits) / len(recent_audits)
                record.gap_audit_score_avg = round(avg_score, 2)
            else:
                record.gap_audit_score_avg = 0.0

    def _compute_expiring_certs(self):
        """Compute expiring certifications (within 30 days)"""
        today = date.today()
        expiring_date = today + timedelta(days=30)

        expiring_certs = self.env['farm.gap.certification'].search([
            ('expiry_date', '>=', today),
            ('expiry_date', '<=', expiring_date),
            ('status', '!=', 'expired')
        ])

        for record in self:
            record.expiring_cert_count = len(expiring_certs)
            record.expiring_certs = expiring_certs