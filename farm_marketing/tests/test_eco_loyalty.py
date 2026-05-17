# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestEcoLoyalty(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        
        cls.ugly_apple_box = cls.env['product.product'].create({
            'name': 'Ugly Apple Blind Box',
            'type': 'product'
        })
        
        cls.normal_apple = cls.env['product.product'].create({
            'name': 'Perfect Apple',
            'type': 'product'
        })
        
        cls.customer = cls.env['res.partner'].create({'name': 'Eco Consumer Alice'})

    def test_01_ugly_produce_gamification(self):
        """
        Scenario 46: Gamified Ugly Produce & Eco-Loyalty
        1. Consumer buys an 'Ugly Produce' box.
        2. System confirms the order.
        3. System automatically calculates carbon savings (preventing landfill).
        4. System awards Eco-Points to the user's loyalty card.
        5. (If ESG installed) System records the carbon sink in the ledger.
        """
        order = self.env['sale.order'].create({
            'partner_id': self.customer.id
        })
        
        # Buy 5 kg of ugly apples
        self.env['sale.order.line'].create({
            'order_id': order.id,
            'product_id': self.ugly_apple_box.id,
            'product_uom_qty': 5.0,
            'price_unit': 5.0
        })
        
        # Buy 2 kg of normal apples
        self.env['sale.order.line'].create({
            'order_id': order.id,
            'product_id': self.normal_apple.id,
            'product_uom_qty': 2.0,
            'price_unit': 15.0
        })
        
        order.action_confirm()
        
        # Only the 5kg of ugly apples should trigger the eco logic
        # 5kg * 2.5 CO2e/kg = 12.5 kg CO2e saved
        # 5kg * 10 points/kg = 50 points
        
        self.assertEqual(order.eco_points_awarded, 50, "Should award 50 points for 5kg of ugly produce.")
        self.assertEqual(order.carbon_savings_co2e, 12.5, "Should calculate 12.5 kg CO2e saved.")
        
        # Check loyalty card
        program = self.env['loyalty.program'].search([('name', '=', 'Eco-Warrior Rewards')], limit=1)
        card = self.env['loyalty.card'].search([
            ('partner_id', '=', self.customer.id),
            ('program_id', '=', program.id)
        ])
        
        self.assertTrue(card, "A loyalty card should be automatically created.")
        self.assertEqual(card.points, 50, "Card should have 50 points balance.")
        
        # Check ESG Integration (Soft Dependency)
        if 'agri.carbon.ledger' in self.env:
            ledger = self.env['agri.carbon.ledger'].search([('origin', '=', order.name)])
            self.assertTrue(ledger, "Carbon ledger entry should be recorded for the consumer's action.")
            self.assertEqual(ledger.impact_type, 'sequestration', "Should be recorded as a sink/saving.")
            self.assertEqual(ledger.co2e_amount, 12.5, "Ledger amount must match the calculation.")

