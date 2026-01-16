from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class CircularAssetTracking(models.Model):
    """
    高价值包材/托盘循环追踪 [US-09-13]
    """
    _name = 'circular.asset.tracking'
    _description = 'Circular Asset Tracking for High-value Packaging'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Asset Reference', required=True, default=lambda self: _('New'))
    asset_type = fields.Selection([
        ('insulated_box', 'Insulated Box'),
        ('standard_pallet', 'Standard Pallet'),
        ('custom_container', 'Custom Container'),
        ('other', 'Other'),
    ], string='Asset Type', required=True)
    asset_serial = fields.Char('Serial Number', required=True)
    description = fields.Text('Description')
    purchase_date = fields.Date('Purchase Date')
    purchase_price = fields.Float('Purchase Price')
    current_status = fields.Selection([
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('in_transit', 'In Transit'),
        ('in_repair', 'In Repair'),
        ('decommissioned', 'Decommissioned'),
    ], string='Current Status', default='available', required=True)
    current_location = fields.Many2one('stock.location', string='Current Location')
    assigned_to_partner = fields.Many2one('res.partner', string='Assigned To Partner (Customer)')
    assigned_date = fields.Date('Assigned Date')
    due_return_date = fields.Date('Due Return Date')
    actual_return_date = fields.Date('Actual Return Date')
    rental_cost_per_day = fields.Float('Rental Cost Per Day')
    total_rental_income = fields.Float('Total Rental Income', compute='_compute_rental_income', store=True)
    overdue_days = fields.Integer('Overdue Days', compute='_compute_overdue_days', store=True)
    rental_agreements = fields.One2many('asset.rental.agreement', 'asset_id', string='Rental Agreements')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('circular.asset.tracking') or '/'
        return super().create(vals)

    @api.depends('rental_agreements.total_income')
    def _compute_rental_income(self):
        for record in self:
            record.total_rental_income = sum(record.rental_agreements.mapped('total_income'))

    @api.depends('due_return_date')
    def _compute_overdue_days(self):
        for record in self:
            if record.due_return_date and record.due_return_date < fields.Date.context_today(self):
                record.overdue_days = (fields.Date.context_today(self) - record.due_return_date).days
            else:
                record.overdue_days = 0

    def action_assign_asset(self, partner_id, due_date):
        """Assign asset to a partner with due date"""
        self.write({
            'current_status': 'in_use',
            'assigned_to_partner': partner_id,
            'assigned_date': fields.Date.context_today(self),
            'due_return_date': due_date,
        })

    def action_receive_asset(self):
        """Receive asset back from partner"""
        self.write({
            'current_status': 'available',
            'actual_return_date': fields.Date.context_today(self),
            'assigned_to_partner': False,
            'assigned_date': False,
            'due_return_date': False,
        })
        # Create activity if asset was overdue
        if self.overdue_days > 0:
            self.env['mail.activity'].create({
                'res_model_id': self.env.ref('farm_supply.model_circular_asset_tracking').id,
                'res_id': self.id,
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                'summary': _('Overdue Asset Return Follow-up'),
                'note': _('Asset %s was returned %d days overdue. Please follow up with customer %s.') % (
                    self.name, self.overdue_days, self.assigned_to_partner.name if self.assigned_to_partner else 'N/A'
                ),
                'user_id': self.env.user.id,
                'date_deadline': fields.Date.context_today(self),
            })


class AssetRentalAgreement(models.Model):
    """
    资产租赁协议 [US-09-13]
    """
    _name = 'asset.rental.agreement'
    _description = 'Asset Rental Agreement'

    asset_id = fields.Many2one('circular.asset.tracking', string='Asset', required=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    agreement_date = fields.Date('Agreement Date', required=True, default=fields.Date.context_today)
    rental_start_date = fields.Date('Rental Start Date', required=True)
    rental_end_date = fields.Date('Rental End Date', required=True)
    daily_rate = fields.Float('Daily Rate', required=True)
    total_income = fields.Float('Total Income', compute='_compute_total_income', store=True)
    status = fields.Selection([
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='active', required=True)

    @api.depends('rental_start_date', 'rental_end_date', 'daily_rate')
    def _compute_total_income(self):
        for record in self:
            if record.rental_start_date and record.rental_end_date:
                days = (record.rental_end_date - record.rental_start_date).days + 1
                record.total_income = days * record.daily_rate
            else:
                record.total_income = 0.0


