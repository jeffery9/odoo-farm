from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class MachineryRental(models.Model):
    """
    机具租赁记录 [US-042-08]
    """
    _name = 'machinery.rental'
    _description = 'Machinery Rental'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Rental Reference', required=True, default=lambda self: _('New'))
    machinery_id = fields.Many2one('shared.machinery.pool', string='Machinery', required=True)
    renter_member_id = fields.Many2one('cooperative.member', string='Renter Member', required=True)
    
    # Linked to Agricultural Interventions
    intervention_id = fields.Many2one('mrp.production', string="Target Agricultural Intervention")

    start_date = fields.Datetime('Start Date', required=True)
    end_date = fields.Datetime('End Date', required=True)
    actual_end_date = fields.Datetime('Actual End Date')
    rental_type = fields.Selection([
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('area_based', 'Area-based'),
        ('task_based', 'Task-based'),
    ], string='Rental Type', default='hourly', required=True)
    expected_cost = fields.Float('Expected Cost', compute='_compute_expected_cost', store=True, precompute=True)
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
            
            # Simple duration calculation
            duration = (record.end_date - record.start_date).total_seconds() / 3600.0
            record.expected_cost = duration * record.machinery_id.hourly_rate

    def action_confirm(self):
        for rental in self:
            rental.state = 'confirmed'
            rental.machinery_id.availability_status = 'in_use'

    def action_complete_rental(self):
        """完成租赁, 并触发 Uber 模式自动跨主体结算 [US-UBER-02]"""
        for rental in self:
            rental.state = 'completed'
            rental.actual_end_date = fields.Datetime.now()
            rental.machinery_id.availability_status = 'available'

            # Uber-style automatic internal settlement 
            # Billed from Renter (Farm B) to Owner (Farm A)
            settlement = self.env['internal.settlement'].create({
                'from_entity_id': rental.renter_member_id.partner_id.id,
                'to_entity_id': rental.machinery_id.owner_member_id.partner_id.id,
                'settlement_type': 'resource_rental',
                'amount': rental.actual_cost or rental.expected_cost,
                'description': f'Machinery rental for {rental.machinery_id.name}',
            })
            
            # Auto-confirm settlement to generate the accounting invoice
            settlement.action_confirm()
            rental.settlement_id = settlement.id
            rental.message_post(body=_("Uber-style sharing completed. Auto-generated settlement %s for $%s.") % (settlement.name, settlement.amount))
