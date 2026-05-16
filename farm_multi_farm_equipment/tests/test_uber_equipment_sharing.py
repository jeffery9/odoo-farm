# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from datetime import datetime, timedelta

class TestUberEquipmentSharing(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        
        # 1. Setup Farm Entities (Tenants)
        cls.coop = cls.env['cooperative.entity'].create({
            'name': 'Global Agri Coop'
        })
        
        cls.farm_a_partner = cls.env['res.partner'].create({'name': 'Farm A (Provider)', 'is_company': True})
        cls.farm_b_partner = cls.env['res.partner'].create({'name': 'Farm B (Requester)', 'is_company': True})
        
        cls.member_a = cls.env['cooperative.member'].create({
            'partner_id': cls.farm_a_partner.id,
            'cooperative_id': cls.coop.id,
        })
        cls.member_b = cls.env['cooperative.member'].create({
            'partner_id': cls.farm_b_partner.id,
            'cooperative_id': cls.coop.id,
        })
        
        # 2. Farm A registers a Harvester into the Shared Pool
        cls.equipment = cls.env['fleet.vehicle'].create({
            'model_id': cls.env['fleet.vehicle.model'].search([], limit=1).id,
            'license_plate': 'HARV-A-001'
        })
        
        cls.shared_harvester = cls.env['shared.machinery.pool'].create({
            'name': 'Farm A Harvester',
            'code': 'SH-A01',
            'cooperative_id': cls.coop.id,
            'owner_member_id': cls.member_a.id,
            'equipment_id': cls.equipment.id,
            'hourly_rate': 100.0, # $100 per hour
        })

    def test_01_cross_farm_uber_dispatch(self):
        """
        Scenario: Uber-style Equipment Dispatch
        1. Farm B creates an intervention needing a Harvester.
        2. Farm B initiates a rental request to the shared pool.
        3. Rental is confirmed (Harvester status changes).
        4. Mission completes, generating an internal settlement.
        5. Settlement generates twin invoices (AP for B, AR for A).
        """
        # Step 1: Farm B requests rental
        start_dt = datetime.now()
        end_dt = start_dt + timedelta(hours=4) # 4 hour mission
        
        rental = self.env['machinery.rental'].create({
            'machinery_id': self.shared_harvester.id,
            'renter_member_id': self.member_b.id,
            'start_date': start_dt,
            'end_date': end_dt,
            'rental_type': 'hourly'
        })
        
        # Check expected cost calculation (4 hours * $100 = $400)
        self.assertEqual(rental.expected_cost, 400.0)
        
        # Step 2: Confirm rental
        rental.action_confirm()
        self.assertEqual(self.shared_harvester.availability_status, 'in_use', "Harvester must be marked as in_use.")
        
        # Step 3: Complete mission
        rental.actual_cost = 450.0 # Actual was 4.5 hours
        rental.action_complete_rental()
        
        self.assertEqual(rental.state, 'completed')
        self.assertEqual(self.shared_harvester.availability_status, 'available', "Harvester must be released back to the pool.")
        
        # Step 4: Verify Settlement & Accounting
        self.assertTrue(rental.settlement_id, "An internal settlement must be generated.")
        settlement = rental.settlement_id
        
        self.assertEqual(settlement.amount, 450.0, "Settlement amount must match actual cost.")
        self.assertEqual(settlement.from_entity_id.id, self.farm_b_partner.id, "Farm B should be the debtor.")
        self.assertEqual(settlement.to_entity_id.id, self.farm_a_partner.id, "Farm A should be the creditor.")
        
        self.assertTrue(settlement.invoice_id, "Settlement must have automatically generated an accounting invoice.")
        invoice = settlement.invoice_id
        self.assertEqual(invoice.move_type, 'in_invoice', "Should be a Vendor Bill for Farm B.")
        self.assertEqual(invoice.partner_id.id, self.farm_a_partner.id, "Bill should be payable to Farm A.")
        self.assertEqual(invoice.amount_total, 450.0, "Invoice amount must match the settlement.")

