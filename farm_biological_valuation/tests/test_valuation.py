# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestBiologicalValuation(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Valuation = cls.env['agri.biological.asset.valuation']
        # Create a dummy asset
        cls.Asset = cls.env['agri.biological.asset'].create({
            'name': 'Test Apple Tree',
            'asset_type': 'crop',
        })
        
    def test_01_valuation_creation(self):
        """ Test basic valuation record creation """
        val = self.Valuation.create({
            'asset_id': self.Asset.id,
            'valuation_method': 'market_price',
            'current_growth_progress': 50.0,
            'target_yield': 100.0,
        })
        self.assertTrue(val.exists())
        self.assertEqual(val.current_yield_potential, 50.0)
        
    def test_02_fair_value_calculation(self):
        """ Test fair value computation """
        val = self.Valuation.create({
            'asset_id': self.Asset.id,
            'valuation_method': 'market_price',
            'current_growth_progress': 60.0,
            'target_yield': 200.0,
        })
        # Mock market price if compute doesn't do it automatically
        val.market_price = 10.0
        val._compute_fair_value()
        self.assertEqual(val.fair_value, 1200.0) # 60% * 200 * 10
