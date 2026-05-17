from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AgriESGComplianceMonitoring(models.Model):
    """
    ESG Compliance Monitoring for tracking compliance status and generating alerts
    """
    _name = 'agri.esg.compliance.monitoring'
    _description = 'Agricultural ESG Compliance Monitoring'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Compliance Check Name', required=True)
    compliance_type = fields.Selection([('environmental', 'Environmental'), ('social', 'Social'), ('governance', 'Governance'), ('industry_standard', 'Industry Standard')], string='Compliance Type', required=True)
    regulation_reference = fields.Char('Regulation Reference', help='Standard or regulation being monitored')
    threshold_value = fields.Float('Threshold Value', help='Threshold that triggers alert')
    current_value = fields.Float('Current Value', help='Current measured value')
    compliance_status = fields.Selection([('compliant', 'Compliant'), ('warning', 'Warning'), ('non_compliant', 'Non Compliant'), ('critical', 'Critical')], string='Compliance Status', compute='_compute_compliance_status', store=True, precompute=True)
    last_check_date = fields.Date('Last Check Date', default=fields.Date.context_today)
    next_check_date = fields.Date('Next Check Date')
    compliance_owner = fields.Many2one('res.users', 'Compliance Owner')
    alert_issued = fields.Boolean('Alert Issued', default=False)
    last_alert_date = fields.Date('Last Alert Date')
    corrective_actions = fields.Text('Corrective Actions Required')
    implementation_status = fields.Selection([('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('na', 'N/A')], string='Implementation Status', default='pending')
    notes = fields.Text('Notes')

    @api.depends('current_value', 'threshold_value')
    def _compute_compliance_status(self):
        """Compute compliance status based on current vs threshold values"""
        for record in self:
            if record.threshold_value:
                # For most environmental metrics, higher values might be worse (e.g., emissions)
                # But for some metrics (e.g., biodiversity), higher values might be better
                # This logic assumes higher values are worse; adjust based on specific use case
                if record.current_value <= record.threshold_value:
                    record.compliance_status = 'compliant'
                elif record.current_value <= record.threshold_value * 1.1:  # 10% buffer
                    record.compliance_status = 'warning'
                elif record.current_value <= record.threshold_value * 1.3:  # 30% buffer
                    record.compliance_status = 'non_compliant'
                else:
                    record.compliance_status = 'critical'
            else:
                record.compliance_status = 'compliant'  # If no threshold, assume compliant

    def action_issue_alert(self):
        """Action to issue alert when compliance is at risk"""
        for record in self:
            if record.compliance_status in ['warning', 'non_compliant', 'critical']:
                record.alert_issued = True
                record.last_alert_date = fields.Date.context_today(self)

                # Create an activity to alert responsible users
                self.env['mail.activity'].create({
                    'activity_type_id': self.env.ref('mail.mail_activity_data_alert').id,
                    'summary': f'ESG Compliance Alert: {record.name}',
                    'note': f'Compliance check {record.name} is at {record.compliance_status} level. Current value: {record.current_value}, Threshold: {record.threshold_value}',
                    'res_id': record.id,
                    'res_model_id': self.env['ir.model'].sudo().search([('model', '=', 'agri.esg.compliance.monitoring')]).id,
                    'user_id': record.compliance_owner.id or self.env.user.id,
                })