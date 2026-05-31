# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
import json

class TestGepValuation(TransactionCase):
    """
    Test the linkage between GEP (Ecological Score) and Financial Valuation.
    Fulfills the 'Anji Model' logic verification.
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # 1. Setup Location
        cls.parcel = cls.env['farm.location'].create({
            'name': 'Pristine Bamboo Forest',
            'is_land_parcel': True,
            'land_area': 10000.0, # 1 Ha
        })
        
        # 2. Setup Eco Zone (High quality)
        cls.env['agri.sustainability.ecological.zone'].create({
            'name': 'Conservation Area',
            'zone_type': 'forest',
            'area': 5000.0, # 50% coverage
            'location_id': cls.parcel.id,
        })
        
        # 3. Setup Biodiversity (High abundance)
        cls.env['agri.sustainability.biodiversity.indicator'].create({
            'indicator_type': 'bird',
            'species_name': 'Egrets',
            'count_observed': 100,
            'location_id': cls.parcel.id,
        })

        # 4. Setup Biological Asset representing the Land
        cls.land_asset = cls.env['agri.biological.asset'].create({
            'name': 'Bamboo Forest Plot 01',
            'agricultural_type': 'plant',
            'location_id': cls.parcel.id,
        })

    def test_01_gep_calculation(self):
        """ Verify GEP score calculation in ecology module """
        self.parcel._compute_gep_score()
        # Coverage: 50% -> 50 points
        # Bio: (100 * 0.5) + (1 * 10) = 60 points
        # GEP: (60 * 0.6) + (50 * 0.4) = 36 + 20 = 56
        # Wait, let's check the score
        self.assertGreater(self.parcel.gep_score, 0)
        self.assertEqual(self.parcel.gep_score, 56.0)

    def test_02_valuation_premium(self):
        """ Verify that high GEP score increases land valuation """
        # Increase bio to reach GEP > 60
        cls = self.__class__
        self.env['agri.sustainability.biodiversity.indicator'].create({
            'indicator_type': 'insect',
            'species_name': 'Honeybees',
            'count_observed': 200,
            'location_id': self.parcel.id,
        })
        self.parcel._compute_gep_score()
        # New Bio: (300 * 0.5) + (2 * 10) = 150 + 20 = 170 -> capped at 100
        # GEP: (100 * 0.6) + (50 * 0.4) = 60 + 20 = 80
        self.assertEqual(self.parcel.gep_score, 80.0)

        # Create Valuation record
        valuation = self.env['farm.financial.asset.valuation'].create({
            'name': 'Eco-Land Valuation',
            'asset_id': self.land_asset.id,
            'asset_type': 'land',
            'valuation_method': 'market_price',
            'market_price': 100000.0, # Base price $100k
        })
        
        # Trigger calculation
        valuation.action_calculate_valuation()
        
        # GEP = 80 -> Premium Factor = 1.20
        self.assertEqual(valuation.gep_premium_factor, 1.20)
        self.assertEqual(valuation.valuation_amount, 120000.0, "Valuation should include 20% ecological premium")
