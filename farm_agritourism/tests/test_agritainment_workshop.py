# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
import json

class TestAgritainmentWorkshop(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        
        # 1. Create a Workshop Resource
        cls.workshop = cls.env['farm.resource'].create({
            'name': 'Ancient Tofu Mill',
            'resource_type': 'workshop'
        })
        
        # 2. Create School Partner
        cls.school = cls.env['res.partner'].create({'name': 'City Elementary School'})
        
        # 3. Create Cultural Product
        cls.tofu_craft = cls.env['product.product'].create({
            'name': 'Artisan Tofu Pack',
            'type': 'product',
        })
        # If the field exists (from farm_pos), set it. Since this test is in farm_agritourism, 
        # farm_pos might not be loaded yet in this specific test transaction context if not dependent.
        # But conceptually, this simulates the flow.

    def test_01_workshop_booking_and_traceability(self):
        """
        Scenario 28: Agritainment & Cultural Heritage Workshops
        1. A school books a field trip to the Tofu Mill.
        2. The group checks in.
        3. The system prepares the context for Traceability Passports.
        """
        booking = self.env['farm.booking'].create({
            'name': 'TRIP-001',
            'partner_id': self.school.id,
            'resource_id': self.workshop.id,
            'workshop_topic': 'Traditional Soy Fermentation'
        })
        
        booking.action_check_in()
        
        # Verify check-in log
        messages = booking.message_ids.mapped('body')
        has_checkin = any("Group Checked In for Workshop: Traditional Soy Fermentation" in str(msg) for msg in messages)
        self.assertTrue(has_checkin, "Checking in should log the workshop topic to build the cultural narrative.")

