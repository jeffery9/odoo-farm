from odoo.tests.common import TransactionCase
from odoo import fields

class TestAgritourismBooking(TransactionCase):

    def setUp(self):
        super(TestAgritourismBooking, self).setUp()
        self.Booking = self.env['farm.booking']
        self.Location = self.env['stock.location']
        self.Partner = self.env['res.partner'].create({'name': 'Tourist A'})
        
        self.plot = self.Location.create({
            'name': 'Picking Orchard 01',
            'is_land_parcel': True,
        })

    def test_01_create_picking_booking(self):
        """ 测试创建采摘预约 [US-51] """
        booking = self.Booking.create({
            'name': 'Weekend Picking Activity',
            'partner_id': self.Partner.id,
            'land_parcel_id': self.plot.id,
            'booking_date': fields.Date.today(),
            'booking_type': 'picking'
        })
        self.assertEqual(booking.state, 'draft')
        self.assertEqual(booking.land_parcel_id.id, self.plot.id)
