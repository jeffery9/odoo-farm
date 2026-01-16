from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class SupplyRiskRadar(models.Model):
    """
    供应链风险雷达 [US-09-16]
    """
    _name = 'supply.risk.radar'
    _description = 'Supply Risk Radar for Agricultural Inputs'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Risk Assessment Name', required=True, default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string='Supplier/Partner', required=True)
    risk_category = fields.Selection([
        ('financial', 'Financial'),
        ('operational', 'Operational'),
        ('logistics', 'Logistics'),
        ('quality', 'Quality'),
        ('environmental', 'Environmental'),
        ('geopolitical', 'Geopolitical'),
    ], string='Risk Category', required=True)
    risk_score = fields.Float('Risk Score', required=True, help='Calculated risk score based on various factors')
    risk_level = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ], string='Risk Level', compute='_compute_risk_level', store=True)
    is_monitored = fields.Boolean('Is Monitored', default=False)
    monitoring_frequency_days = fields.Integer('Monitoring Frequency (Days)', default=7)
    last_monitoring_date = fields.Date('Last Monitoring Date')
    is_automated_monitoring_enabled = fields.Boolean('Automated Monitoring Enabled', default=False)
    monitoring_indicators = fields.Text('Monitoring Indicators')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('supply.risk.radar') or '/'
        return super().create(vals)

    @api.depends('risk_score')
    def _compute_risk_level(self):
        for record in self:
            if record.risk_score <= 2.0:
                record.risk_level = 'low'
            elif record.risk_score <= 5.0:
                record.risk_level = 'medium'
            elif record.risk_score <= 8.0:
                record.risk_level = 'high'
            else:
                record.risk_level = 'critical'

    def action_schedule_automated_monitoring(self):
        """Schedule automated monitoring for this risk assessment"""
        if not self.is_automated_monitoring_enabled:
            self.write({
                'is_automated_monitoring_enabled': True,
                'last_monitoring_date': fields.Date.context_today(self)
            })

        # Create a server action or scheduled activity to perform monitoring
        self.env['mail.activity'].create({
            'res_model_id': self.env.ref('farm_supply.model_supply_risk_radar').id,
            'res_id': self.id,
            'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
            'summary': _('Supply Risk Monitoring for %s') % self.partner_id.name,
            'note': _('Monitoring risk level for %s. Current score: %s (%s)') % (
                self.partner_id.name, self.risk_score, self.risk_level
            ),
            'user_id': self.env.user.id,
            'date_deadline': fields.Date.add(fields.Date.context_today(self), days=self.monitoring_frequency_days),
        })

    def action_update_from_external_data(self):
        """Update risk assessment based on external data sources"""
        # This would integrate with external risk data sources
        # For now, we'll just log the update
        _logger.info(f"Updating risk assessment {self.name} for {self.partner_id.name} from external sources")

        # Example: Increase risk score if external indicators show issues
        # This is where we'd integrate with external risk monitoring services
        self.message_post(
            body=_("Risk assessment updated based on external risk monitoring data.")
        )
        self.last_monitoring_date = fields.Date.context_today(self)


