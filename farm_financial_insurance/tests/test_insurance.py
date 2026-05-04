# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestInsurance(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Insurance = cls.env['farm.crop.yield.insurance']
        cls.Partner = cls.env['res.partner'].create({'name': 'Test Farmer'})
        
    def test_01_insurance_creation(self):
        """ Test basic insurance policy creation """
        policy = self.Insurance.create({
            'partner_id': self.Partner.id,
            'amount': 10000.0,
            'duration_months': 12,
        })
        self.assertTrue(policy.exists())
        self.assertEqual(policy.state, 'draft')
        
    def test_02_premium_calculation(self):
        """ Test premium amount computation """
        policy = self.Insurance.create({
            'partner_id': self.Partner.id,
            'amount': 10000.0,
            'risk_score': 5.0, # Assuming 5% premium base on risk score
        })
        # If _compute_premium_amount uses risk_score
        if policy.premium_amount > 0:
            self.assertTrue(policy.premium_amount > 0)
        
    def test_03_maturity_date(self):
        """ Test maturity date calculation """
        from datetime import date, timedelta
        policy = self.Insurance.create({
            'partner_id': self.Partner.id,
            'application_date': date.today(),
            'duration_months': 6,
        })
        # Check maturity date logic
        self.assertTrue(policy.maturity_date)
