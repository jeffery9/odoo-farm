from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class FairTradeCertificate(models.Model):
    """
    US-081-01: 公平贸易认证追踪与溢价管理
    Fair Trade Certificate Management for tracking certification and premiums
    """
    _name = 'farm.esg.fair.trade.certificate'
    _description = 'Fair Trade Certificate'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Certificate Name', required=True)
    certificate_number = fields.Char('Certificate Number', required=True, copy=False)
    issuing_body = fields.Char('Issuing Body', required=True)
    issue_date = fields.Date('Issue Date', required=True)
    expiry_date = fields.Date('Expiry Date', required=True)
    is_active = fields.Boolean('Is Active', compute='_compute_is_active', store=True)
    fair_trade_premium = fields.Float('Fair Trade Premium (%)', help='Percentage premium paid to producers')
    covered_products = fields.Many2many('product.product', 'farm_esg_fair_trade_certificate_product_product_rel', 'certificate_id', 'product_id', string='Covered Products')
    covered_farms = fields.Many2many('res.partner', 'farm_esg_fair_trade_certificate_res_partner_rel', 'certificate_id', 'partner_id', string='Covered Farms')
    certificate_type = fields.Selection([('fair_trade_intl', 'Fairtrade International'), ('fair_trade_usa', 'Fair Trade USA'), ('fair_for_life', 'Fair for Life'), ('worldfairtrade', 'WFTO'), ('other', 'Other')], string='Certificate Type', default='fair_trade_intl')
    status = fields.Selection([('applied', 'Applied'), ('under_review', 'Under Review'), ('certified', 'Certified'), ('suspended', 'Suspended'), ('expired', 'Expired'), ('revoked', 'Revoked')], string='Status', default='applied', required=True)
    annual_audit_date = fields.Date('Annual Audit Date')
    next_audit_date = fields.Date('Next Audit Date')
    compliance_score = fields.Float('Compliance Score', help='Score based on audit results')
    assigned_to_user_id = fields.Many2one('res.users', 'Assigned To')

    @api.depends('expiry_date')
    def _compute_is_active(self):
        """Compute if the certificate is currently active based on expiry date"""
        today = fields.Date.context_today(self)
        for record in self:
            record.is_active = record.expiry_date and record.expiry_date >= today

    @api.constrains('issue_date', 'expiry_date')
    def _check_date_range(self):
        """Ensure expiry date is after issue date"""
        for record in self:
            if record.issue_date and record.expiry_date and record.issue_date > record.expiry_date:
                raise ValidationError(_("Expiry date must be after issue date."))

    def action_check_expiry_alerts(self):
        """Check for certificates that are about to expire and send alerts"""
        today = fields.Date.context_today(self)
        # Find certificates expiring in the next 30 days
        expiring_certs = self.search([
            ('expiry_date', '<=', fields.Date.add(today, days=30)),
            ('expiry_date', '>=', today),
            ('is_active', '=', True)
        ])

        for cert in expiring_certs:
            # Create an activity to alert responsible users
            self.env['mail.activity'].create({
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                'summary': f'Fair Trade Certificate {cert.name} is about to expire',
                'note': f'Certificate {cert.name} (#{cert.certificate_number}) expires on {cert.expiry_date}',
                'res_id': cert.id,
                'res_model_id': self.env['ir.model'].sudo().search([('model', '=', 'farm.esg.fair.trade.certificate')]).id,
                'user_id': cert.assigned_to_user_id.id or self.env.user.id,
            })

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Expiry Check Complete',
                'message': f'Found {len(expiring_certs)} certificates expiring soon.',
                'sticky': False,
            }
        }


class FairTradePremiumAllocation(models.Model):
    """
    Fair Trade Premium Allocation for tracking how premiums are distributed
    """
    _name = 'farm.esg.fair.trade.premium.allocation'
    _description = 'Fair Trade Premium Allocation'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    certificate_id = fields.Many2one('farm.esg.fair.trade.certificate', 'Certificate', required=True)
    allocation_date = fields.Date('Allocation Date', required=True)
    amount = fields.Float('Amount', required=True)
    allocation_type = fields.Selection([('community_investment', 'Community Investment'), ('producer_bonus', 'Producer Bonus'), ('infrastructure', 'Infrastructure'), ('education', 'Education'), ('healthcare', 'Healthcare'), ('other', 'Other')], string='Allocation Type', required=True)
    description = fields.Text('Description')
    beneficiaries = fields.Text('Beneficiaries')
    impact_measure = fields.Text('Impact Measure')
    allocated_by = fields.Many2one('res.users', 'Allocated By')
    approved_by = fields.Many2one('res.users', 'Approved By')
    approval_date = fields.Date('Approval Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('allocated', 'Allocated'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='State', default='draft', required=True)
    allocation_reference = fields.Char('Allocation Reference', copy=False, readonly=True)

    @api.model
    def create(self, vals):
        """Auto-generate allocation reference on creation"""
        if not vals.get('allocation_reference'):
            vals['allocation_reference'] = self.env['ir.sequence'].next_by_code('fair.trade.premium.allocation') or '/'
        return super().create(vals)

    def action_approve(self):
        """Approve the premium allocation"""
        for record in self:
            record.write({
                'state': 'approved',
                'approved_by': self.env.user.id,
                'approval_date': fields.Date.context_today(self)
            })

            # Send notification about approval
            record.message_post(
                body=f"Fair Trade Premium Allocation {record.allocation_reference} has been approved by {self.env.user.name}.",
                subtype_id=self.env.ref('mail.mt_comment').id
            )

    def action_reject(self):
        """Reject the premium allocation"""
        for record in self:
            record.write({
                'state': 'rejected'
            })

            # Send notification about rejection
            record.message_post(
                body=f"Fair Trade Premium Allocation {record.allocation_reference} has been rejected.",
                subtype_id=self.env.ref('mail.mt_comment').id
            )

    def action_allocate(self):
        """Mark the allocation as allocated"""
        for record in self:
            if not record.approved_by:
                record.approved_by = self.env.user.id
                record.approval_date = fields.Date.context_today(self)
            record.state = 'allocated'

            # Send notification about allocation
            record.message_post(
                body=f"Fair Trade Premium Allocation {record.allocation_reference} has been allocated.",
                subtype_id=self.env.ref('mail.mt_comment').id
            )


class CommunityInvestment(models.Model):
    """
    US-081-03: 社区投资与乡村振兴贡献量化
    Community Investment tracking for rural revitalization contribution
    """
    _name = 'farm.esg.community.investment'
    _description = 'Community Investment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Investment Name', required=True)
    investment_type = fields.Selection([('employment', 'Employment'), ('infrastructure', 'Infrastructure'), ('education', 'Education'), ('healthcare', 'Healthcare'), ('environmental', 'Environmental'), ('social_welfare', 'Social Welfare'), ('other', 'Other')], string='Investment Type', required=True)
    amount = fields.Float('Amount')
    beneficiaries_count = fields.Integer('Number of Beneficiaries')
    location = fields.Char('Location')
    investment_date = fields.Date('Investment Date')
    description = fields.Text('Description')
    impact_assessment = fields.Text('Impact Assessment')
    evidence_attachments = fields.Binary('Evidence Attachments', attachment=True)
    reported_by = fields.Many2one('res.users', 'Reported By')
    project_status = fields.Selection([('planned', 'Planned'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], string='Project Status', default='planned')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    annual_recurring = fields.Boolean('Annual Recurring')

    @api.constrains('investment_date', 'start_date', 'end_date')
    def _check_investment_dates(self):
        """Ensure dates are logical"""
        for record in self:
            if record.start_date and record.end_date and record.start_date > record.end_date:
                raise ValidationError(_("End date must be after start date."))

    @api.model
    def get_annual_community_investments(self, year=None):
        """Get community investments for a specific year"""
        if year is None:
            year = fields.Date.context_today(self).year
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"

        investments = self.search([
            ('investment_date', '>=', start_date),
            ('investment_date', '<=', end_date)
        ])

        total_amount = sum(investments.mapped('amount'))
        total_beneficiaries = sum(investments.mapped('beneficiaries_count'))

        return {
            'investments': investments,
            'total_amount': total_amount,
            'total_beneficiaries': total_beneficiaries,
            'count': len(investments)
        }


class LaborCondition(models.Model):
    """
    US-081-02: 农工权益保护与安全合规
    US-081-04: 劳动条件透明度与供应链可追溯
    Labor conditions and worker protection tracking
    """
    _name = 'farm.esg.labor.condition'
    _description = 'Labor Condition'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Condition Name', required=True)
    employee_id = fields.Many2one('hr.employee', 'Employee', required=True)
    condition_type = fields.Selection([('safety_training', 'Safety Training'), ('health_cert', 'Health Cert'), ('insurance_coverage', 'Insurance Coverage'), ('working_hours', 'Working Hours'), ('wage_compliance', 'Wage Compliance'), ('other', 'Other')], string='Condition Type', required=True)
    issue_date = fields.Date('Issue Date')
    expiry_date = fields.Date('Expiry Date')
    is_valid = fields.Boolean('Is Valid', compute='_compute_is_valid', store=True)
    compliance_status = fields.Selection([('compliant', 'Compliant'), ('non_compliant', 'Non Compliant'), ('pending_review', 'Pending Review'), ('expired', 'Expired')], string='Compliance Status', default='compliant')
    training_record = fields.Many2one('farm.agri.skill', 'Training Record')
    certification = fields.Char('Certification Number')
    issuing_body = fields.Char('Issuing Body')
    notes = fields.Text('Notes')
    last_inspection_date = fields.Date('Last Inspection Date')
    next_inspection_date = fields.Date('Next Inspection Date')
    safety_score = fields.Float('Safety Score')

    @api.depends('expiry_date')
    def _compute_is_valid(self):
        """Compute if the condition is currently valid"""
        today = fields.Date.context_today(self)
        for record in self:
            if record.expiry_date:
                record.is_valid = record.expiry_date >= today
            else:
                record.is_valid = True  # No expiry date means always valid

    @api.model
    def check_worker_compliance(self, employee_id=None):
        """Check compliance status for workers, optionally for a specific employee"""
        domain = [('compliance_status', '!=', 'compliant')]
        if employee_id:
            domain.append(('employee_id', '=', employee_id))

        non_compliant_conditions = self.search(domain)

        # Group by employee
        employee_compliance = {}
        for condition in non_compliant_conditions:
            emp_id = condition.employee_id.id
            if emp_id not in employee_compliance:
                employee_compliance[emp_id] = {
                    'employee': condition.employee_id.name,
                    'conditions': []
                }
            employee_compliance[emp_id]['conditions'].append({
                'condition': condition.name,
                'type': condition.condition_type,
                'status': condition.compliance_status,
                'expiry_date': condition.expiry_date
            })

        return employee_compliance

    def action_schedule_inspection(self):
        """Schedule next inspection for labor conditions"""
        today = fields.Date.context_today(self)
        for record in self:
            if not record.next_inspection_date:
                # Default to 6 months from today if not set
                record.next_inspection_date = fields.Date.add(today, months=6)