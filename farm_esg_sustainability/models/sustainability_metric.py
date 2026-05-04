# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class AgriSustainabilityMetric(models.Model):
    """
    Agri Domain Level: Sustainability Metric. [US-101-01, US-014-2026]
    Universal sustainability standards for the Agri domain.
    Refactored from farm.sustainability.metric with 100% logic and English i18n.
    """
    _name = 'agri.sustainability.metric'
    _description = 'Agricultural Sustainability Metric'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'category, sequence'

    name = fields.Char('Metric Name', required=True, translate=True)
    code = fields.Char('Metric Code', required=True, copy=False)
    category = fields.Selection([
        ('economic', 'Economic'),
        ('environmental', 'Environmental'),
        ('social', 'Social'),
        ('governance', 'Governance'),
    ], string='Category', required=True, default='economic')
    
    unit = fields.Char('Unit of Measure', help='Unit of the metric, e.g., Tons, USD, Percentage')
    description = fields.Text('Description', translate=True)
    sequence = fields.Integer('Sequence', default=10)
    target_value = fields.Float('Target Value')
    current_value = fields.Float('Current Value', compute='_compute_current_value', store=True)
    progress_rate = fields.Float('Progress Rate (%)', compute='_compute_progress_rate', store=True, digits=(6, 2))
    is_active = fields.Boolean('Active', default=True)
    
    calculation_method = fields.Selection([
        ('manual', 'Manual Entry'),
        ('automatic', 'Automatic Calculation'),
        ('formula', 'Formula-based')
    ], string='Calculation Method', required=True, default='manual')
    
    formula = fields.Text('Calculation Formula', help='Python formula used when method is set to Formula-based')
    last_updated = fields.Datetime('Last Updated', readonly=True)

    # Metric Value History
    value_history_ids = fields.One2many('agri.sustainability.metric.value', 'metric_id', string='Value History')

    @api.depends('value_history_ids.value')
    def _compute_current_value(self):
        """Calculate the latest metric value based on history."""
        for metric in self:
            if metric.value_history_ids:
                latest_value = metric.value_history_ids.sorted('date', reverse=True)[:1]
                metric.current_value = latest_value.value if latest_value else 0.0
            else:
                metric.current_value = 0.0

    @api.depends('current_value', 'target_value')
    def _compute_progress_rate(self):
        """Calculate the achievement rate towards the target."""
        for metric in self:
            if metric.target_value != 0:
                metric.progress_rate = (metric.current_value / metric.target_value) * 100
            else:
                metric.progress_rate = 0.0

    @api.constrains('code')
    def _check_code_unique(self):
        """Ensure uniqueness of the metric code."""
        for record in self:
            count = self.search_count([('code', '=', record.code)])
            if count > 1:
                raise ValidationError(_('The Metric Code must be unique: %s') % record.code)

    def action_update_value(self):
        """Action to launch the update value wizard."""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Update Metric Value'),
            'res_model': 'agri.sustainability.metric.value.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_metric_id': self.id,
                'default_value': self.current_value
            }
        }

    @api.model
    def create(self, vals):
        """Automatically create an initial value record upon creation."""
        record = super(AgriSustainabilityMetric, self).create(vals)
        if 'current_value' in vals:
            self.env['agri.sustainability.metric.value'].create({
                'metric_id': record.id,
                'value': vals['current_value'],
                'date': fields.Datetime.now(),
                'note': _('Initial value setup')
            })
        return record


class AgriSustainabilityMetricValue(models.Model):
    """
    History of sustainability metric values (Domain Level).
    """
    _name = 'agri.sustainability.metric.value'
    _description = 'Agri Sustainability Metric Value'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    metric_id = fields.Many2one('agri.sustainability.metric', string='Metric', required=True, ondelete='cascade')
    value = fields.Float('Value', required=True)
    date = fields.Datetime('Record Date', required=True, default=fields.Datetime.now)
    note = fields.Text('Note')
    recorded_by = fields.Many2one('res.users', string='Recorded By', default=lambda self: self.env.user)

    @api.model
    def create(self, vals):
        """Update the last_updated timestamp of the parent metric."""
        record = super(AgriSustainabilityMetricValue, self).create(vals)
        if record.metric_id:
            record.metric_id.last_updated = fields.Datetime.now()
        return record


class AgriSustainabilityMetricValueWizard(models.TransientModel):
    """
    Wizard to record new metric values.
    """
    _name = 'agri.sustainability.metric.value.wizard'
    _description = 'Agri Sustainability Metric Value Update Wizard'

    metric_id = fields.Many2one('agri.sustainability.metric', string='Metric', readonly=True)
    value = fields.Float('New Value', required=True)
    date = fields.Datetime('Date', default=fields.Datetime.now, required=True)
    note = fields.Text('Note')

    def action_update_value(self):
        """Execute the value update and return to the list view."""
        if self.metric_id:
            self.env['agri.sustainability.metric.value'].create({
                'metric_id': self.metric_id.id,
                'value': self.value,
                'date': self.date,
                'note': self.note,
                'recorded_by': self.env.user.id
            })
            return {
                'type': 'ir.actions.act_window',
                'name': _('Sustainability Metrics'),
                'res_model': 'agri.sustainability.metric',
                'view_mode': 'list,form',
                'target': 'current',
            }
        return {'type': 'ir.actions.act_window_close'}