from odoo.tests import TransactionCase, tagged
from odoo.exceptions import ValidationError


@tagged('post_install', '-at_install')
class TestFairTrade(TransactionCase):
    """Test Fair Trade related models and functions"""

    def setUp(self):
        super().setUp()

        # Create test data
        self.fair_trade_certificate = self.env['farm.esg.fair.trade.certificate'].create({
            'name': 'Test Fair Trade Certificate',
            'certificate_number': 'FT123456',
            'issuing_body': 'Fair Trade International',
            'issue_date': '2023-01-01',
            'expiry_date': '2025-01-01',
            'certificate_type': 'fair_trade_intl',
            'status': 'certified',
            'fair_trade_premium': 10.0,
        })

    def test_create_fair_trade_certificate(self):
        """Test creating a fair trade certificate"""
        self.assertEqual(self.fair_trade_certificate.name, 'Test Fair Trade Certificate')
        self.assertEqual(self.fair_trade_certificate.certificate_number, 'FT123456')
        self.assertTrue(self.fair_trade_certificate.is_active)

    def test_certificate_expiry_check(self):
        """Test that certificate expiry status is computed correctly"""
        # Create an expired certificate
        expired_cert = self.env['farm.esg.fair.trade.certificate'].create({
            'name': 'Expired Certificate',
            'certificate_number': 'FT987654',
            'issuing_body': 'Fair Trade International',
            'issue_date': '2020-01-01',
            'expiry_date': '2021-01-01',  # Expired date
            'certificate_type': 'fair_trade_intl',
            'status': 'expired',
        })

        self.assertFalse(expired_cert.is_active)
        self.assertTrue(self.fair_trade_certificate.is_active)

    def test_date_validation(self):
        """Test that expiry date cannot be before issue date"""
        with self.assertRaises(ValidationError):
            self.env['farm.esg.fair.trade.certificate'].create({
                'name': 'Invalid Date Certificate',
                'certificate_number': 'FT000000',
                'issuing_body': 'Fair Trade International',
                'issue_date': '2025-01-01',  # Later date
                'expiry_date': '2023-01-01',  # Earlier date
                'certificate_type': 'fair_trade_intl',
                'status': 'applied',
            })

    def test_premium_allocation_workflow(self):
        """Test the premium allocation workflow"""
        # Create a premium allocation
        premium_allocation = self.env['farm.esg.fair.trade.premium.allocation'].create({
            'certificate_id': self.fair_trade_certificate.id,
            'allocation_date': '2023-06-01',
            'amount': 1000.0,
            'allocation_type': 'community_investment',
            'description': 'Community school project',
            'state': 'draft'
        })

        # Test the allocation workflow
        self.assertEqual(premium_allocation.state, 'draft')

        # Test allocation action
        premium_allocation.action_allocate()
        self.assertIn(premium_allocation.state, ['allocated', 'approved'])

        # Test approve action
        premium_allocation.action_approve()
        self.assertEqual(premium_allocation.state, 'approved')

    def test_premium_allocation_without_approval(self):
        """Test that premium allocation can be allocated without explicit approval"""
        premium_allocation = self.env['farm.esg.fair.trade.premium.allocation'].create({
            'certificate_id': self.fair_trade_certificate.id,
            'allocation_date': '2023-06-01',
            'amount': 500.0,
            'allocation_type': 'producer_bonus',
            'description': 'Producer bonus allocation',
            'state': 'draft'
        })

        # Simulate allocation without approval
        premium_allocation.action_allocate()
        # The state should be allocated and approval_date should be set
        self.assertIsNotNone(premium_allocation.approval_date)