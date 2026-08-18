# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestLivestockValuationBridge(TransactionCase):

    def setUp(self):
        super(TestLivestockValuationBridge, self).setUp()
        
        # Seed an agri.biological.asset (since asset_id is required on farm.financial.asset.valuation)
        self.biological_asset = self.env['agri.biological.asset'].create({
            'name': 'Ginseng Plant Area A',
        })
        
        # Seed L1 livestock animal and a weight telemetry record
        self.livestock_asset = self.env['farm.livestock'].create({
            'name': 'Ginseng-fed Wagyu Cow #01',
            'breed_coefficient': 1.5
        })
        self.weight_record = self.env['livestock.weight.record'].create({
            'livestock_id': self.livestock_asset.id,
            'measured_weight': 500.0,
            'rfid_tag': 'GS1-WAGYU-01'
        })
        # Base platform valuation model instance
        self.valuation_base = self.env['farm.financial.asset.valuation'].create({
            'name': 'Valuation Transaction #1',
            'asset_id': self.biological_asset.id,
            'livestock_asset_id': self.livestock_asset.id
        })

    def test_livestock_valuation_curve(self):
        """ Verify dynamic computation of L2 livestock growth-weight curve valuation """
        algorithms = self.valuation_base._get_specialized_algorithms()
        self.assertIn('livestock', algorithms, "Livestock specialized algorithm must be registered in dynamic bridge registry")
        
        # Trigger valuation calculation
        calculated_amount = self.valuation_base.action_compute_biomass_valuation()
        # Expected: 500.0 (weight) * 1.5 (breed_coefficient) * 12.5 (rate) = 9375.0
        self.assertEqual(calculated_amount, 9375.0, "Livestock biological valuation calculations misaligned with dynamic growth curve")
