from odoo.tests.common import TransactionCase

class TestFarmInsurance(TransactionCase):
    def setUp(self):
        super().setUp()
        self.agri_loc = self.env['agri.location'].create({
            'name': 'Insured Field',
            'location_type': 'field'
        })

    def test_01_policy_creation(self):
        """ Test creating an insurance policy """
        if 'farm.insurance.policy' not in self.env:
            self.skipTest("farm.insurance.policy model not found")
        policy = self.env['farm.insurance.policy'].create({
            'name': 'POLICY-2026-001',
            'policy_number': 'INS-999',
            'location_id': self.agri_loc.id,
            'insured_amount': 100000.0,
            'premium_amount': 2000.0
        })
        self.assertEqual(policy.insured_amount, 100000.0)
