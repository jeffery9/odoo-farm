from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, date, timedelta


class FarmGAPCertification(models.Model):
    _name = 'farm.gap.certification'
    _description = 'GAP (Good Agricultural Practices) Certification'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("GAP Certificate Name", required=True)
    cert_number = fields.Char("Certificate Number", required=True)
    cert_type = fields.Selection([
        ('globalgap', 'GlobalGAP'),
        ('us_gap', 'US GAP'),
        ('eu_gap', 'EU GAP'),
        ('china_gap', 'China GAP'),
        ('other', 'Other GAP Standard')
    ], string="GAP Standard Type", required=True, default='china_gap')

    partner_id = fields.Many2one('res.partner', string="Certified Entity", required=True)
    farm_location_ids = fields.Many2many('stock.location', string="Certified Locations")
    product_ids = fields.Many2many('product.product', string="Certified Products")

    issue_date = fields.Date("Issue Date", default=fields.Date.context_today, required=True)
    expiry_date = fields.Date("Expiry Date", required=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('valid', 'Valid'),
        ('expired', 'Expired'),
        ('suspended', 'Suspended'),
        ('revoked', 'Revoked')
    ], string="Status", default='valid', tracking=True)

    # GAP Specific Requirements
    water_quality_compliance = fields.Boolean("Water Quality Compliance")
    soil_health_management = fields.Boolean("Soil Health Management")
    pest_management_plan = fields.Boolean("Integrated Pest Management Plan")
    worker_health_safety = fields.Boolean("Worker Health & Safety")
    traceability_system = fields.Boolean("Traceability System")
    environmental_protection = fields.Boolean("Environmental Protection")

    # Audit Information
    last_audit_date = fields.Date("Last Audit Date")
    next_audit_date = fields.Date("Next Audit Date")
    audit_result = fields.Text("Audit Result")
    non_conformities = fields.Text("Non-Conformities")

    # Documentation
    certificate_file = fields.Binary("Certificate File", attachment=True)
    audit_report_file = fields.Binary("Audit Report", attachment=True)
    supporting_docs = fields.Binary("Supporting Documents", attachment=True)

    @api.constrains('issue_date', 'expiry_date')
    def _check_dates(self):
        for record in self:
            if record.issue_date and record.expiry_date:
                if record.issue_date > record.expiry_date:
                    raise ValidationError(_("Issue date cannot be later than expiry date."))

    @api.constrains('status', 'expiry_date')
    def _check_expiry_status(self):
        today = date.today()
        for record in self:
            if record.status == 'valid' and record.expiry_date < today:
                record.status = 'expired'

    @api.onchange('issue_date', 'expiry_date')
    def _onchange_dates(self):
        if self.issue_date and self.expiry_date:
            # Calculate next audit date as 3 months before expiry for GAP standards
            self.next_audit_date = self.expiry_date - timedelta(days=90)

    def action_renew_certificate(self):
        """Action to renew GAP certification"""
        self.ensure_one()
        renewal_wizard = self.env['farm.certification.renewal.wizard'].create({
            'certification_id': self.id,
            'certification_model': 'farm.gap.certification',
        })
        return {
            'name': _('Renew GAP Certificate'),
            'type': 'ir.actions.act_window',
            'res_model': 'farm.certification.renewal.wizard',
            'res_id': renewal_wizard.id,
            'view_mode': 'form',
            'target': 'new',
        }

    @api.model
    def cron_check_expiry(self):
        """Cron job to check for expiring certificates"""
        today = date.today()
        expiring_certs = self.search([
            ('expiry_date', '<=', today + timedelta(days=30)),
            ('status', '=', 'valid')
        ])

        for cert in expiring_certs:
            cert.message_post(
                body=_("GAP Certificate is expiring on %s. Please renew promptly.") % cert.expiry_date,
                subject=_("GAP Certificate Expiry Alert")
            )


class FarmGAPAudit(models.Model):
    _name = 'farm.gap.audit'
    _description = 'GAP Audit Records'
    _order = 'audit_date desc'

    certification_id = fields.Many2one('farm.gap.certification', string="GAP Certification", required=True)
    partner_id = fields.Many2one(related='certification_id.partner_id', string="Entity", store=True)
    audit_date = fields.Date("Audit Date", default=fields.Date.context_today, required=True)
    auditor = fields.Char("Auditor Name")
    audit_type = fields.Selection([
        ('internal', 'Internal Audit'),
        ('external', 'External Audit'),
        ('annual', 'Annual Audit'),
        ('renewal', 'Renewal Audit'),
        ('complaint', 'Complaint-based Audit')
    ], string="Audit Type", default='external')

    # GAP Audit Criteria
    water_quality_score = fields.Float("Water Quality Score", help="Score out of 100", digits=(10, 2))
    soil_management_score = fields.Float("Soil Management Score", digits=(10, 2))
    pest_management_score = fields.Float("Pest Management Score", digits=(10, 2))
    worker_safety_score = fields.Float("Worker Safety Score", digits=(10, 2))
    traceability_score = fields.Float("Traceability Score", digits=(10, 2))
    environmental_score = fields.Float("Environmental Score", digits=(10, 2))
    total_score = fields.Float("Total Score", compute='_compute_total_score', store=True)

    # Compliance Status
    compliant = fields.Boolean("Overall Compliant", compute='_compute_compliance', store=True)
    audit_result = fields.Selection([
        ('pass', 'Pass'),
        ('conditional', 'Conditional Pass'),
        ('fail', 'Fail')
    ], string="Audit Result", compute='_compute_audit_result', store=True)

    non_conformities = fields.Text("Non-Conformities")
    corrective_actions = fields.Text("Corrective Actions Required")
    follow_up_required = fields.Boolean("Follow-up Required")

    @api.depends('water_quality_score', 'soil_management_score', 'pest_management_score',
                 'worker_safety_score', 'traceability_score', 'environmental_score')
    def _compute_total_score(self):
        for record in self:
            record.total_score = sum([
                record.water_quality_score or 0,
                record.soil_management_score or 0,
                record.pest_management_score or 0,
                record.worker_safety_score or 0,
                record.traceability_score or 0,
                record.environmental_score or 0
            ]) / 6  # Average of all criteria

    @api.depends('total_score', 'non_conformities')
    def _compute_compliance(self):
        for record in self:
            if record.non_conformities:
                record.compliant = False
            else:
                record.compliant = record.total_score >= 85.0  # 85% threshold for compliance

    @api.depends('compliant', 'total_score', 'non_conformities')
    def _compute_audit_result(self):
        for record in self:
            if record.total_score < 70.0:
                record.audit_result = 'fail'
            elif record.total_score >= 85.0 and not record.non_conformities:
                record.audit_result = 'pass'
            else:
                record.audit_result = 'conditional'


class FarmGAPRequirement(models.Model):
    _name = 'farm.gap.requirement'
    _description = 'GAP Compliance Requirements'

    name = fields.Char("Requirement Name", required=True)
    code = fields.Char("Requirement Code", required=True, help="e.g., WQ-001 for Water Quality")
    category = fields.Selection([
        ('water', 'Water Quality & Usage'),
        ('soil', 'Soil Health & Management'),
        ('pest', 'Pest Management'),
        ('worker', 'Worker Health & Safety'),
        ('traceability', 'Traceability & Record Keeping'),
        ('environment', 'Environmental Protection'),
        ('food_safety', 'Food Safety')
    ], string="Category", required=True)

    description = fields.Text("Description")
    mandatory = fields.Boolean("Mandatory", default=True)
    frequency = fields.Selection([
        ('continuously', 'Continuously'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually')
    ], string="Compliance Frequency", default='daily')

    # Implementation Guide
    implementation_guide = fields.Html("Implementation Guide")
    evidence_required = fields.Html("Evidence Required")

    active = fields.Boolean("Active", default=True)

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Requirement code must be unique.')
    ]


class FarmGAPComplianceCheck(models.Model):
    _name = 'farm.gap.compliance.check'
    _description = 'GAP Daily Compliance Check'

    name = fields.Char("Check Reference", compute='_compute_name', store=True)
    location_id = fields.Many2one('stock.location', string="Location", required=True)
    date = fields.Date("Check Date", default=fields.Date.context_today, required=True)
    checker_id = fields.Many2one('res.users', string="Checked By", default=lambda self: self.env.user)

    # Compliance Status for each requirement
    water_quality_compliant = fields.Boolean("Water Quality Compliant")
    soil_management_compliant = fields.Boolean("Soil Management Compliant")
    pest_management_compliant = fields.Boolean("Pest Management Compliant")
    worker_safety_compliant = fields.Boolean("Worker Safety Compliant")
    traceability_compliant = fields.Boolean("Traceability Compliant")
    environmental_compliant = fields.Boolean("Environmental Compliant")

    overall_compliant = fields.Boolean("Overall Compliant", compute='_compute_overall_compliance', store=True)
    notes = fields.Text("Notes")
    corrective_actions = fields.Text("Corrective Actions")

    @api.depends('location_id', 'date')
    def _compute_name(self):
        for record in self:
            record.name = f"GAP Check - {record.location_id.name} - {record.date}"

    @api.depends(
        'water_quality_compliant', 'soil_management_compliant', 'pest_management_compliant',
        'worker_safety_compliant', 'traceability_compliant', 'environmental_compliant'
    )
    def _compute_overall_compliance(self):
        for record in self:
            compliant_checks = [
                record.water_quality_compliant,
                record.soil_management_compliant,
                record.pest_management_compliant,
                record.worker_safety_compliant,
                record.traceability_compliant,
                record.environmental_compliant
            ]
            # All checks must be True for overall compliance
            record.overall_compliant = all(check for check in compliant_checks if check is not None)

    @api.constrains('date')
    def _check_future_date(self):
        for record in self:
            if record.date and record.date > date.today():
                raise ValidationError(_("Check date cannot be in the future."))