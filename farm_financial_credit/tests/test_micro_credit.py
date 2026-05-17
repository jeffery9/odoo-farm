# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestMicroCredit(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        
        cls.good_farmer = cls.env['res.users'].create({'name': 'Honest Zhang', 'login': 'zhang'})
        cls.bad_farmer = cls.env['res.users'].create({'name': 'Lazy Wang', 'login': 'wang'})
        
        # Create history for Good Farmer (Trust Score 95)
        for i in range(3):
            cls.env['project.task'].create({
                'name': f'Harvest Task {i}',
                'user_ids': [(4, cls.good_farmer.id)],
                'trust_verification_status': 'verified',
                'trust_score': 95.0
            })
            
        # Create history for Bad Farmer (Trust Score 50)
        for i in range(3):
            cls.env['project.task'].create({
                'name': f'Spraying Task {i}',
                'user_ids': [(4, cls.bad_farmer.id)],
                'trust_verification_status': 'verified',
                'trust_score': 50.0
            })

    def test_01_data_backed_loan_approval(self):
        """
        Scenario 18: Data-Backed Cooperative Micro-Credit
        1. Honest Zhang applies for $500. System checks his past task trust scores.
        2. Average score is 95.0. System auto-approves and generates disbursement settlement.
        3. Lazy Wang applies for $500. Average score is 50.0. System rejects.
        """
        good_loan = self.env['farm.micro.loan'].create({
            'farmer_id': self.good_farmer.id,
            'amount_requested': 500.0
        })
        good_loan.action_evaluate_and_approve()
        
        self.assertEqual(good_loan.digital_trust_score, 95.0)
        self.assertEqual(good_loan.state, 'disbursed', "Good farmer should be approved and disbursed.")
        self.assertTrue(good_loan.settlement_id, "Disbursement settlement must be generated.")
        self.assertEqual(good_loan.settlement_id.amount, 500.0)
        
        bad_loan = self.env['farm.micro.loan'].create({
            'farmer_id': self.bad_farmer.id,
            'amount_requested': 500.0
        })
        bad_loan.action_evaluate_and_approve()
        
        self.assertEqual(bad_loan.digital_trust_score, 50.0)
        self.assertEqual(bad_loan.state, 'rejected', "Bad farmer should be rejected.")

