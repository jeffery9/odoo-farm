# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestCentralizedSales(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        
        cls.tomato = cls.env['product.product'].create({'name': 'Village Brand Tomato', 'type': 'product', 'tracking': 'lot'})
        
        cls.coop = cls.env.company
        
        # Two farmers
        cls.farmer_a = cls.env['res.users'].create({'name': 'Farmer A', 'login': 'farmer_a'})
        cls.farmer_b = cls.env['res.users'].create({'name': 'Farmer B', 'login': 'farmer_b'})
        
        cls.mega_lot = cls.env['stock.lot'].create({
            'name': 'MEGA-TOMATO-001',
            'product_id': cls.tomato.id,
            'company_id': cls.coop.id,
        })
        
        # Register contributions
        cls.env['stock.lot.contribution'].create({
            'lot_id': cls.mega_lot.id,
            'farmer_id': cls.farmer_a.id,
            'contributed_qty': 100.0 # 100kg
        })
        cls.env['stock.lot.contribution'].create({
            'lot_id': cls.mega_lot.id,
            'farmer_id': cls.farmer_b.id,
            'contributed_qty': 200.0 # 200kg
        })

    def test_01_centralized_sales_revenue_split(self):
        """
        Scenario 17: Distributed Grow, Centralized Brand Sales
        1. Farmers pool 300kg of tomatoes into a Mega-Lot.
        2. Coop sells the 300kg at a premium price ($10/kg = $3000 total).
        3. System automatically calculates the 90% payout.
        4. Farmer A receives $900 (100kg * $10 * 0.9).
        5. Farmer B receives $1800 (200kg * $10 * 0.9).
        """
        so = self.env['sale.order'].create({
            'partner_id': self.env['res.partner'].create({'name': 'High-end Supermarket'}).id
        })
        
        self.env['sale.order.line'].create({
            'order_id': so.id,
            'product_id': self.tomato.id,
            'product_uom_qty': 300.0,
            'price_unit': 10.0,
            'lot_id': self.mega_lot.id
        })
        
        # Trigger the engine
        self.env['internal.settlement'].action_centralized_sales_revenue_split(so)
        
        settlements = self.env['internal.settlement'].search([('description', 'ilike', 'Centralized Sale')])
        self.assertEqual(len(settlements), 2, "Should generate exactly 2 payouts.")
        
        payout_a = settlements.filtered(lambda s: s.to_entity_id.id == self.farmer_a.partner_id.id)
        self.assertEqual(payout_a.amount, 900.0)
        
        payout_b = settlements.filtered(lambda s: s.to_entity_id.id == self.farmer_b.partner_id.id)
        self.assertEqual(payout_b.amount, 1800.0)
