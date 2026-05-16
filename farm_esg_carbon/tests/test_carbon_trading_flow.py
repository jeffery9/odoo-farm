# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
import logging

_logger = logging.getLogger(__name__)

class TestCarbonTradingFlow(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        
        # Entities
        cls.farm_a = cls.env['res.partner'].create({'name': 'Green Farm A', 'is_company': True})
        cls.factory_b = cls.env['res.partner'].create({'name': 'Heavy Processing Plant B', 'is_company': True})
        
        # Ensure company partner is set to Farm A for the test scope
        cls.env.company.partner_id = cls.farm_a

        # Carbon Factor
        cls.factor_notill = cls.env['agri.carbon.factor'].create({
            'name': 'No-Till Sequestration',
            'category': 'land',
            'emission_factor': 0.0, # Not used directly in this simplified mock
            'uom_id': cls.env.ref('uom.product_uom_acre', raise_if_not_found=False).id or cls.env.ref('uom.product_uom_unit').id,
        })
        
        # Carbon Ledger Entry (Sequestration)
        cls.ledger_sink = cls.env['agri.carbon.ledger'].create({
            'name': 'No-Till Carbon Sink 2026',
            'impact_type': 'sequestration',
            'scope': 'scope3',
            'co2e_amount': 50000.0, # 50,000 kg = 50 Tons
            'source_factor_id': cls.factor_notill.id
        })

    def test_01_tokenize_and_trade_carbon(self):
        """
        Scenario:
        1. Farm A generates 50 Tons of carbon sequestration.
        2. Farm A tokenizes this into a tradable Carbon Credit Asset.
        3. Plant B purchases the asset to offset its emissions.
        4. System automatically transfers ownership and creates an internal financial settlement.
        """
        # Step 1: Tokenize
        self.ledger_sink.action_tokenize_offset()
        self.assertTrue(self.ledger_sink.is_tokenized, "Ledger entry should be marked as tokenized.")
        
        asset = self.env['farm.exchange.asset'].search([('origin_ledger_id', '=', self.ledger_sink.id)])
        self.assertTrue(asset, "A tradable asset must be created on the exchange.")
        self.assertEqual(asset.quantity, 50.0, "50,000 kg CO2e should equal 50.0 Tons.")
        self.assertEqual(asset.state, 'available', "Asset should be available for trading.")
        self.assertEqual(asset.owner_id.id, self.farm_a.id, "Farm A should be the initial owner.")
        
        # Step 2: Trade (Plant B buys from Farm A)
        success = asset.action_purchase(self.factory_b)
        self.assertTrue(success, "Purchase action should execute successfully.")
        
        # Step 3: Verify Ownership and State
        self.assertEqual(asset.state, 'sold', "Asset should be marked as sold.")
        self.assertEqual(asset.owner_id.id, self.factory_b.id, "Ownership should transfer to Plant B.")
        
        # Step 4: Verify Financial Settlement
        settlement = self.env['internal.settlement'].search([
            ('from_entity_id', '=', self.factory_b.id),
            ('to_entity_id', '=', self.farm_a.id),
            ('amount', '=', 2500.0) # 50 tons * $50/ton = $2500
        ])
        self.assertTrue(settlement, "An internal settlement of $2500 must be auto-generated.")
        self.assertEqual(settlement.state, 'confirmed', "The settlement should be auto-confirmed.")

