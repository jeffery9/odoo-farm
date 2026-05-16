# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
import logging

_logger = logging.getLogger(__name__)

class TestDynamicBiologicalValuation(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        
        # 1. Create a biological asset (e.g., a herd of Pigs)
        cls.biological_asset = cls.env['agri.biological.asset'].create({
            'name': 'Herd of Yorkshire Pigs - Batch 01',
            'agricultural_type': 'animal',
            'base_weight_kg': 1000.0, # Total herd weight
        })

        # 2. Setup the valuation template & market price
        # Assuming current market price for live pig is $3.5 per kg
        cls.valuation_record = cls.env['farm.financial.asset.valuation'].create({
            'asset_id': cls.biological_asset.id,
            'valuation_method': 'market_price',
            'market_price': 3.5,
            'original_cost': 3500.0, # 1000kg * 3.5
            'valuation_amount': 3500.0,
            'asset_type': 'livestock'
        })
        
        # We need a feed product
        cls.feed_product = cls.env['product.product'].create({
            'name': 'High-Energy Pig Feed',
            'type': 'consu'
        })

    def test_01_feed_consumption_increases_valuation(self):
        """
        Scenario:
        1. A feeding intervention consumes 500kg of feed.
        2. Farm Agri Science logic calculates weight gain based on a Feed Conversion Ratio (e.g., FCR = 2.5, meaning 500kg feed = 200kg meat).
        3. Biological asset weight increases to 1200kg.
        4. Financial Valuation module catches this, generates a new valuation at $3.5/kg ($4200),
           and creates a journal entry for the $700 unrealized gain.
        """
        # Step 1: Execute Feeding Intervention
        intervention = self.env['mrp.production'].create({
            'product_id': self.env['product.product'].create({'name': 'Feeding Service', 'type': 'service'}).id,
            'product_qty': 1.0,
            'intervention_type': 'feeding',
            'asset_id': self.biological_asset.id,
        })
        
        self.env['stock.move'].create({
            'name': 'Consume Feed',
            'product_id': self.feed_product.id,
            'product_uom_qty': 500.0,
            'product_uom': self.feed_product.uom_id.id,
            'location_id': self.env.ref('stock.stock_location_stock').id,
            'location_dest_id': self.env.ref('stock.stock_location_stock').id,
            'raw_material_production_id': intervention.id,
        })
        
        # Mark intervention as done to trigger the weight gain & valuation pipeline
        intervention.action_confirm()
        # simplified mock:
        intervention._trigger_post_intervention_growth()
        
        # Step 2: Assert biological growth
        self.biological_asset.invalidate_recordset(['base_weight_kg'])
        self.assertEqual(self.biological_asset.base_weight_kg, 1200.0, "Weight should increase by 200kg (500kg feed / 2.5 FCR).")
        
        # Step 3: Assert financial valuation update
        new_valuation = self.env['farm.financial.asset.valuation'].search([
            ('asset_id', '=', self.biological_asset.id)
        ], order='id desc', limit=1)
        
        self.assertEqual(new_valuation.valuation_amount, 4200.0, "New valuation should be 1200kg * 3.5 = $4200.")
        self.assertEqual(new_valuation.valuation_variance, 20.0, "Variance should be 20% (($4200-$3500)/$3500).")
        
        # Step 4: Verify accounting journal entry
        # The new valuation should have triggered action_create_accounting_entries
        self.assertTrue(new_valuation.message_ids, "Valuation message should be posted containing journal entry info.")
        has_journal_entry = any("Journal entry" in msg.body for msg in new_valuation.asset_id.message_ids)
        self.assertTrue(has_journal_entry, "An accounting journal entry must be created for the unrealized gain.")

