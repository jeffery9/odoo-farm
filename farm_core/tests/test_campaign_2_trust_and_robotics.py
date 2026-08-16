# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError

@tagged('post_install', '-at_install')
class TestCampaign2TrustAndRobotics(TransactionCase):

    def setUp(self):
        super(TestCampaign2TrustAndRobotics, self).setUp()
        self.carrier_a = self.env['stock.matter.tracking'].create({'name': 'CARRIER-A', 'dna_integrity_score': 100.0})
        self.carrier_b = self.env['stock.matter.tracking'].create({'name': 'CARRIER-B', 'dna_integrity_score': 90.0})
        self.carrier_c = self.env['stock.matter.tracking'].create({'name': 'CARRIER-C'})

    def test_merkle_cascade_hashing_and_ledger(self):
        """ Verify child carrier gets a unique SHA-256 Merkle cascade state hash on link creation and logs ledger """
        self.env['stock.matter.tracking.link'].create({
            'parent_id': self.carrier_a.id,
            'child_id': self.carrier_c.id,
            'link_type': 'sequential'
        })
        self.assertTrue(self.carrier_c.merkle_state_hash, "Merkle State Hash must be generated!")
        self.assertEqual(len(self.carrier_c.merkle_state_hash), 64, "Merkle State Hash must be 64 characters hexadecimal.")
        
        # Verify ledger entry was created as confirmed
        ledger = self.env['agri.clearing.ledger'].search([('description', 'like', 'SFC Merkle Traceability State Certified')])
        self.assertTrue(ledger, "Automated ledger entry must be created!")
        self.assertEqual(ledger[0].state, 'confirmed', "Audit ledger log should be auto-confirmed.")

    def test_federated_a2a_auction_clearing(self):
        """ Verify multi-agent charging auction transaction transfers credit balances atomically """
        buyer_partner = self.env['res.partner'].create({
            'name': 'UAV-01-Agent-Owner',
            'impact_credits': 150.0
        })
        seller_partner = self.env['res.partner'].create({
            'name': 'Solar-Station-Agent-Owner',
            'impact_credits': 50.0
        })
        
        # Execute clearing transaction
        self.env['agri.clearing.netting.engine'].create({'name': 'Auction-UAV-BATTERY-932'}).action_execute_a2a_auction_clearing(
            buyer_id=buyer_partner.id,
            seller_id=seller_partner.id,
            transaction_credits=30.0,
            detail_desc="Drone Battery Charge Auction Station #2"
        )
        # Re-fetch balances
        self.assertEqual(buyer_partner.impact_credits, 120.0, "Buyer credits must decrease by auction price.")
        self.assertEqual(seller_partner.impact_credits, 80.0, "Seller credits must increase by auction price.")
