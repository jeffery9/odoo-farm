from odoo import models, fields, api, _
import json
from datetime import datetime

class FarmSubsidyProgram(models.Model):
    _name = 'farm.subsidy.program'
    _description = 'Agricultural Subsidy Program'

    name = fields.Char("Program Name", required=True) # e.g. "2026 Organic Conversion Support"
    code = fields.Char("Policy Code")
    authority = fields.Char("Issuing Authority")

    subsidy_type = fields.Selection([
        ('area', 'Per Area'),
        ('head', 'Per Head'),
        ('project', 'Project Based'),
        ('output', 'Per Output')
    ], required=True, default='area')

    amount_per_unit = fields.Monetary("Amount per Unit")
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)

    requirements = fields.Text("Compliance Requirements")

class FarmSubsidyApplication(models.Model):
    """
    US-65-04: 补贴申请业务模型
    职责：处理补贴申请的业务流程，包括证据自动化收集、合规性验证和报告生成
    业务逻辑：通过farm_evidence基础设施实现补贴证据自动化功能
    """
    _name = 'farm.subsidy.application'
    _description = 'Subsidy Application'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Application Ref", default=lambda self: _('New'))
    program_id = fields.Many2one('farm.subsidy.program', string="Program", required=True)
    fiscal_year = fields.Integer("Fiscal Year", default=lambda self: fields.Date.today().year)

    # 申报对象
    land_parcel_ids = fields.Many2many('farm.location', string="Declared Parcels", domain=[('is_land_parcel', '=', True)])

    declared_quantity = fields.Float("Declared Qty (Area/Head)")
    estimated_amount = fields.Monetary("Estimated Amount", compute='_compute_estimated_amount')
    currency_id = fields.Many2one('res.currency', related='program_id.currency_id')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('paid', 'Paid')
    ], default='draft', tracking=True)

    # US-65-04: Subsidy Evidence Automation - Compliance Evidence Fields
    compliance_status = fields.Selection([
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('compliant', 'Compliant'),
        ('non_compliant', 'Non-Compliant')
    ], string="Compliance Status", default='pending', tracking=True)

    evidence_collected = fields.Integer("Evidence Collected", compute='_compute_evidence_collected', store=True)
    evidence_records = fields.One2many('farm.evidence', 'subsidy_application_id', string="Compliance Evidence")

    # Fields for compliance handbook generation
    compliance_handbook_data = fields.Text("Compliance Handbook Data", readonly=True)
    handbook_generated_date = fields.Datetime("Handbook Generated Date", readonly=True)

    @api.depends('declared_quantity', 'program_id.amount_per_unit')
    def _compute_estimated_amount(self):
        for app in self:
            app.estimated_amount = app.declared_quantity * app.program_id.amount_per_unit

    @api.depends('land_parcel_ids', 'fiscal_year')
    def _compute_evidence_collected(self):
        """Compute the number of evidence records associated with this application"""
        FarmEvidence = self.env['farm.evidence']
        for app in self:
            if app.land_parcel_ids:
                # Find evidence records associated with the declared parcels
                # Include evidence linked to tasks/activities that are on these parcels
                # Filter by time period (fiscal year)
                start_date = f"{app.fiscal_year}-01-01"
                end_date = f"{app.fiscal_year}-12-31"

                # Build domain for evidence search
                evidence_domain = [
                    '|',
                    ('res_model', '=', 'farm.location'),
                    ('res_id', 'in', app.land_parcel_ids.ids),
                ]

                # Add tasks related to these parcels
                tasks_on_parcels = self.env['project.task'].search([('land_parcel_id', 'in', app.land_parcel_ids.ids)])
                if tasks_on_parcels:
                    evidence_domain.append('|')
                    evidence_domain.append(('res_model', '=', 'project.task'))
                    evidence_domain.append(('res_id', 'in', tasks_on_parcels.ids))

                # Add interventions related to these parcels
                interventions_on_parcels = self.env['agri.intervention'].search([('land_parcel_id', 'in', app.land_parcel_ids.ids)])
                if interventions_on_parcels:
                    evidence_domain.append('|')
                    evidence_domain.append(('res_model', '=', 'agri.intervention'))
                    evidence_domain.append(('res_id', 'in', interventions_on_parcels.ids))

                # Filter by time period (fiscal year)
                evidence_domain.append(('taken_at', '>=', start_date))
                evidence_domain.append(('taken_at', '<=', end_date))

                evidence_count = FarmEvidence.search_count(evidence_domain)
                app.evidence_collected = evidence_count
            else:
                app.evidence_collected = 0

    @api.onchange('land_parcel_ids')
    def _onchange_parcels(self):
        if self.program_id.subsidy_type == 'area':
            self.declared_quantity = sum(self.land_parcel_ids.mapped('land_area'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.subsidy.application') or _('SUB')
        return super().create(vals_list)

    def action_collect_compliance_evidence(self):
        """
        US-65-04: Automatically collect GPS + time + photo evidence for subsidy compliance
        This method searches for related evidence records based on land parcels and time period
        """
        self.ensure_one()
        FarmEvidence = self.env['farm.evidence']

        # Build domain to find evidence records related to this application
        evidence_domain = []

        # Add conditions for land parcels
        if self.land_parcel_ids:
            evidence_domain.append('|')
            evidence_domain.append(('res_model', '=', 'farm.location'))
            evidence_domain.append(('res_id', 'in', self.land_parcel_ids.ids))

            # Also include evidence from tasks on these parcels
            tasks_on_parcels = self.env['project.task'].search([('land_parcel_id', 'in', self.land_parcel_ids.ids)])
            if tasks_on_parcels:
                evidence_domain.append('|')
                evidence_domain.append(('res_model', '=', 'project.task'))
                evidence_domain.append(('res_id', 'in', tasks_on_parcels.ids))

        # Add conditions for interventions on these parcels
        interventions_on_parcels = self.env['agri.intervention'].search([('land_parcel_id', 'in', self.land_parcel_ids.ids)])
        if interventions_on_parcels:
            evidence_domain.append('|')
            evidence_domain.append(('res_model', '=', 'agri.intervention'))
            evidence_domain.append(('res_id', 'in', interventions_on_parcels.ids))

        # Filter by time period (fiscal year)
        start_date = f"{self.fiscal_year}-01-01"
        end_date = f"{self.fiscal_year}-12-31"
        evidence_domain.append(('taken_at', '>=', start_date))
        evidence_domain.append(('taken_at', '<=', end_date))

        # Search for evidence records
        evidence_records = FarmEvidence.search(evidence_domain)

        # Update the compliance status based on evidence collected
        if evidence_records:
            # Check if we have sufficient evidence (for now, just check if we have any)
            self.compliance_status = 'verified' if len(evidence_records) > 0 else 'pending'

            # Update the message log
            self.message_post(
                body=_("Compliance evidence collection completed. Found %d evidence records for this application.") % len(evidence_records)
            )
        else:
            self.compliance_status = 'pending'
            self.message_post(
                body=_("No compliance evidence found for this application during fiscal year %s.") % self.fiscal_year
            )

        return {
            'type': 'ir.actions.act_window',
            'name': _('Compliance Evidence'),
            'res_model': 'farm.evidence',
            'view_mode': 'list,form',
            'domain': [('id', 'in', evidence_records.ids)],
            'context': self.env.context,
        }

    def action_generate_compliance_handbook(self):
        """
        US-65-04: Generate "Compliance Handbook" with aggregated evidence
        This creates audit-ready documentation with GPS + timestamp + photo evidence
        """
        self.ensure_one()
        FarmEvidence = self.env['farm.evidence']

        # Collect all relevant evidence for this application
        evidence_domain = []

        if self.land_parcel_ids:
            evidence_domain.append('|')
            evidence_domain.append(('res_model', '=', 'farm.location'))
            evidence_domain.append(('res_id', 'in', self.land_parcel_ids.ids))

            # Include evidence from tasks on these parcels
            tasks_on_parcels = self.env['project.task'].search([('land_parcel_id', 'in', self.land_parcel_ids.ids)])
            if tasks_on_parcels:
                evidence_domain.append('|')
                evidence_domain.append(('res_model', '=', 'project.task'))
                evidence_domain.append(('res_id', 'in', tasks_on_parcels.ids))

        # Include evidence from interventions on these parcels
        interventions_on_parcels = self.env['agri.intervention'].search([('land_parcel_id', 'in', self.land_parcel_ids.ids)])
        if interventions_on_parcels:
            evidence_domain.append('|')
            evidence_domain.append(('res_model', '=', 'agri.intervention'))
            evidence_domain.append(('res_id', 'in', interventions_on_parcels.ids))

        # Filter by time period (fiscal year)
        start_date = f"{self.fiscal_year}-01-01"
        end_date = f"{self.fiscal_year}-12-31"
        evidence_domain.append(('taken_at', '>=', start_date))
        evidence_domain.append(('taken_at', '<=', end_date))

        evidence_records = FarmEvidence.search(evidence_domain)

        # Create structured data for the compliance handbook
        handbook_data = {
            'application_ref': self.name,
            'fiscal_year': self.fiscal_year,
            'program_name': self.program_id.name,
            'declared_parcels': [{
                'name': parcel.name,
                'area': parcel.land_area,
                'area_unit': parcel.land_area_unit,
            } for parcel in self.land_parcel_ids],
            'total_evidence_count': len(evidence_records),
            'evidence_records': [],
            'generated_at': datetime.now().isoformat(),
            'compliance_status': self.compliance_status,
        }

        # Add evidence records to handbook
        for evidence in evidence_records:
            handbook_data['evidence_records'].append({
                'name': evidence.name,
                'taken_at': evidence.taken_at.isoformat() if evidence.taken_at else None,
                'gps_lat': evidence.gps_lat,
                'gps_lng': evidence.gps_lng,
                'is_on_site': evidence.is_on_site,
                'note': evidence.note,
                'taken_by': evidence.worker_id.name if evidence.worker_id else None,
            })

        # Store the handbook data
        self.compliance_handbook_data = json.dumps(handbook_data, ensure_ascii=False, indent=2)
        self.handbook_generated_date = fields.Datetime.now()

        # Update compliance status to compliant if we have evidence
        if evidence_records:
            self.compliance_status = 'compliant'

        self.message_post(
            body=_("Compliance Handbook generated with %d evidence records. Ready for audit submission.") % len(evidence_records)
        )

        return {
            'type': 'ir.actions.act_window',
            'name': _('Compliance Handbook'),
            'res_model': 'farm.evidence',
            'view_mode': 'list,form',
            'domain': [('id', 'in', evidence_records.ids)],
            'context': self.env.context,
        }
