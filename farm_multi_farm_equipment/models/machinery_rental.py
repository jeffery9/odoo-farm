from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class MachineryRental(models.Model):
    """
    机具租赁记录 [US-19-08]
    """
    _name = 'machinery.rental'
    _description = 'Machinery Rental'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Rental Reference', required=True, default=lambda self: _('New'))
    machinery_id = fields.Many2one('shared.machinery.pool', string='Machinery', required=True)
    renter_member_id = fields.Many2one('cooperative.member', string='Renter Member', required=True)
    start_date = fields.Datetime('Start Date', required=True)
    end_date = fields.Datetime('End Date', required=True)
    actual_end_date = fields.Datetime('Actual End Date')
    rental_type = fields.Selection([
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('area_based', 'Area-based'),
        ('task_based', 'Task-based'),
    ], string='Rental Type', default='hourly', required=True)
    expected_cost = fields.Float('Expected Cost', compute='_compute_expected_cost', store=True)
    actual_cost = fields.Float('Actual Cost', default=0.0)
    settlement_id = fields.Many2one('internal.settlement', string='Settlement')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', required=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('machinery.rental') or '/'
        return super().create(vals)

    @api.depends('start_date', 'end_date', 'rental_type', 'machinery_id')
    def _compute_expected_cost(self):
        for record in self:
            if not record.start_date or not record.end_date:
                record.expected_cost = 0.0
                continue
            # Calculate expected cost based on rental type and duration
            # This is a simplified calculation - real implementation would consider more factors
            if record.machinery_id and record.machinery_id.hourly_rate:
                duration_hours = (record.end_date - record.start_date).total_seconds() / 3600
                if record.rental_type == 'hourly':
                    record.expected_cost = duration_hours * record.machinery_id.hourly_rate
                elif record.rental_type == 'daily':
                    duration_days = max(1, int(duration_hours / 24))
                    record.expected_cost = duration_days * record.machinery_id.daily_rate
                else:
                    record.expected_cost = 0.0  # Would need additional logic for area/task based
            else:
                record.expected_cost = 0.0