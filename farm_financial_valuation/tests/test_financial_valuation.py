# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestFinancialValuation(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Valuation = cls.env['farm.financial.asset.valuation']
        # Create a dummy asset
        cls.Asset = cls.env['agri.biological.asset'].create({
            'name': 'Test Tractor',
            'asset_type': 'machinery',
        })
        
    def test_01_valuation_creation(self):
        """ Test basic financial valuation record creation """
        val = self.Valuation.create({
            'asset_id': self.Asset.id,
            'asset_type': 'machinery',
            'valuation_method': 'cost_model',
            'acquisition_cost': 50000.0,
            'depreciation_accumulated': 10000.0,
        })
        self.assertTrue(val.exists())
        self.assertEqual(val.book_value, 40000.0)
        
    def test_02_fair_value_calculation(self):
        """ Test fair value computation with market adjustment """
        val = self.Valuation.create({
            'asset_id': self.Asset.id,
            'asset_type': 'machinery',
            'valuation_method': 'market_price',
            'market_price': 45000.0,
            'market_adjustment_factor': 0.9, # 10% discount for used condition
        })
        self.assertEqual(val.fair_value, 40500.0)
