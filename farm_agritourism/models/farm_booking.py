from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class FarmResource(models.Model):
    _name = 'farm.resource'
    _description = 'Agritourism Resource'

    name = fields.Char("Resource Name", required=True)
    resource_type = fields.Selection([
        ('fishing', 'Fishing Spot'),
        ('bbq', 'BBQ Area'),
        ('room', 'Farm Stay'),
        ('other', 'Other')
    ], string="Type", required=True)
    active = fields.Boolean(default=True)

class FarmBooking(models.Model):
    _name = 'farm.booking'
    _description = 'Farm Activity Booking'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Booking Reference", required=True)
    partner_id = fields.Many2one('res.partner', string="Customer", required=True)
    booking_date = fields.Date("Activity Date", default=fields.Date.today, required=True)
    
    # 增加起止时间以支持细粒度预约 [US-02-03]
    date_start = fields.Datetime("Start Time", required=True, default=fields.Datetime.now)
    date_stop = fields.Datetime("End Time", required=True, default=fields.Datetime.now)
    
    resource_id = fields.Many2one('farm.resource', string="Booked Resource")
    
    booking_type = fields.Selection([
        ('picking', 'Picking'),
        ('family', 'Family Event'),
        ('adoption', 'Adoption'),
        ('visit', 'Farm Visit'),
        ('resource', 'Resource Booking')
    ], string="Type", default='picking', required=True)
    
    land_parcel_id = fields.Many2one(
        'stock.location', 
        string="Land Parcel/Area", 
        domain=[('is_land_parcel', '=', True)],
    )
    
    sale_order_id = fields.Many2one('sale.order', string="Linked Sale Order")
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string="Status", default='draft', tracking=True)
    
    notes = fields.Text("Notes")

    # QR Code for Check-in [US-02-01]
    booking_qr_code = fields.Char("Booking QR Code", compute='_compute_qr_code', store=True)

    @api.depends('name')
    def _compute_qr_code(self):
        for booking in self:
            # 模拟生成 QR 码链接
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            booking.booking_qr_code = f"{base_url}/farm/checkin/{booking.name}"

    def action_checkin(self):
        """ 游客入园核销 """
        self.ensure_one()
        if self.state != 'confirmed':
            raise ValidationError(_("Check-in failed: Booking is not confirmed."))
        self.write({'state': 'done'})
        self.message_post(body=_("CHECK-IN: Visitor has arrived and booking is validated."))

    @api.constrains('resource_id', 'date_start', 'date_stop')
    def _check_booking_overlap(self):
        """ 检查同一资源的预约时间冲突 [US-02-03] """
        for booking in self:
            if not booking.resource_id:
                continue
            overlap = self.search([
                ('id', '!=', booking.id),
                ('resource_id', '=', booking.resource_id.id),
                ('state', '!=', 'cancel'),
                ('date_start', '<', booking.date_stop),
                ('date_stop', '>', booking.date_start),
            ])
            if overlap:
                raise ValidationError(_("CONFLICT: The resource %s is already booked for this period.") % booking.resource_id.name)

    def action_confirm(self):
        self.write({'state': 'confirmed'})