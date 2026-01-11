from odoo import models, fields, api

class FarmBooking(models.Model):
    _name = 'farm.booking'
    _description = 'Farm Activity Booking'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Booking Reference", required=True)
    partner_id = fields.Many2one('res.partner', string="Customer", required=True)
    booking_date = fields.Date("Activity Date", default=fields.Date.today, required=True)
    
    booking_type = fields.Selection([
        ('picking', 'Picking (采摘)'),
        ('family', 'Family Event (亲子活动)'),
        ('adoption', 'Adoption (认养/租赁)'),
        ('visit', 'Farm Visit (参观)')
    ], string="Type", default='picking', required=True)
    
    land_parcel_id = fields.Many2one(
        'stock.location', 
        string="Land Parcel/Area", 
        domain=[('is_land_parcel', '=', True)],
        help="The specific area where the activity will take place."
    )
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string="Status", default='draft', tracking=True)
    
    notes = fields.Text("Notes")

    def action_confirm(self):
        self.write({'state': 'confirmed'})
