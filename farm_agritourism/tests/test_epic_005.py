# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo import fields

class TestEpic005(TransactionCase):
    """ BDD Test for Epic 005 Agritourism & Experience """

    def setUp(self):
        super(TestEpic005, self).setUp()
        self.Partner = self.env['res.partner'].create({'name': 'Tourist A'})
        self.Resource = self.env['farm.resource'].create({
            'name': 'Fishing Spot 01',
            'resource_type': 'fishing',
            'capacity': 1,
        })

    def test_01_picking_garden_activity_booking_and_check_in(self):
        """ Scenario: Picking garden activity booking and check-in """
        booking = self.env['farm.booking'].create({
            'partner_id': self.Partner.id,
            'resource_id': self.Resource.id,
            'date_from': fields.Datetime.now(),
            'date_to': fields.Datetime.now(),
        })
        self.assertTrue(booking.id)
        
        # Simulate check-in
        booking.action_checkin()
        self.assertEqual(booking.state, 'checked_in')

    def test_02_pick_to_sale_integration(self):
        """ Scenario: "Pick-to-Sale" integration """
        # Test sales order link to picking garden activity
        pass

    def test_03_resource_capacity_and_conflict_management(self):
        """ Scenario: Resource capacity and conflict management """
        # Create first booking
        self.env['farm.booking'].create({
            'partner_id': self.Partner.id,
            'resource_id': self.Resource.id,
            'date_from': fields.Datetime.now(),
            'date_to': fields.Datetime.now(),
        })
        
        # Try to create second booking for same resource (capacity is 1)
        with self.assertRaises(UserError, msg="Should block due to capacity"):
            self.env['farm.booking'].create({
                'partner_id': self.Partner.id,
                'resource_id': self.Resource.id,
                'date_from': fields.Datetime.now(),
                'date_to': fields.Datetime.now(),
            })

    def test_05_integrated_multi_farm_community_tour_booking(self):
        """ Scenario: Integrated multi-farm community tour booking """
        # Test cross-company resource confirmation
        pass
