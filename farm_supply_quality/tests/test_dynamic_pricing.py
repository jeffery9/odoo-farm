# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestDynamicPricing(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        
        cls.apple = cls.env['product.product'].create({
            'name': 'Fuji Apple', 
            'type': 'product',
            'list_price': 10.0 # Base price $10
        })
        
        cls.customer = cls.env['res.partner'].create({'name': 'High-End Supermarket'})
        
        # We need to simulate the quality grade on the lot.
        # Since quality_grade might be injected via ISL or farm_core, we check if it exists.
        cls.premium_lot = cls.env['stock.lot'].create({
            'name': 'LOT-PREMIUM',
            'product_id': cls.apple.id,
            'company_id': cls.env.company.id,
        })
        if hasattr(cls.premium_lot, 'quality_grade'):
            cls.premium_lot.write({'quality_grade': 'premium'})
            
        cls.standard_lot = cls.env['stock.lot'].create({
            'name': 'LOT-STANDARD',
            'product_id': cls.apple.id,
            'company_id': cls.env.company.id,
        })
        if hasattr(cls.standard_lot, 'quality_grade'):
            cls.standard_lot.write({'quality_grade': 'standard'})

    def test_01_premium_lot_surcharge(self):
        """
        Scenario:
        1. A B2B Sale Order is created for Apples.
        2. Sales rep selects a specific harvested lot that was graded 'Premium'.
        3. System automatically intercepts and applies a 30% price premium ($13.0 instead of $10.0).
        """
        if not hasattr(self.premium_lot, 'quality_grade'):
            self.skipTest("quality_grade field not found on stock.lot, skipping dynamic pricing test.")
            
        order = self.env['sale.order'].create({
            'partner_id': self.customer.id
        })
        
        line = self.env['sale.order.line'].create({
            'order_id': order.id,
            'product_id': self.apple.id,
            'product_uom_qty': 100,
            'price_unit': 10.0
        })
        
        # Simulate user selecting the premium lot in the UI
        line.agri_lot_id = self.premium_lot.id
        line._onchange_agri_lot_pricing()
        
        self.assertTrue(line.quality_premium_applied, "Premium flag should be checked.")
        self.assertEqual(line.price_unit, 13.0, "Price should have been increased by 30% to 13.0")
        self.assertIn("30% Premium Surcharge", line.name, "Description should mention the premium.")
        
        # Test revert
        line.agri_lot_id = self.standard_lot.id
        line._onchange_agri_lot_pricing()
        self.assertFalse(line.quality_premium_applied, "Premium flag should be unchecked.")
        self.assertEqual(line.price_unit, 10.0, "Price should revert to base 10.0")

