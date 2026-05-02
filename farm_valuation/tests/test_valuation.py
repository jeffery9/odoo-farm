from odoo.tests.common import TransactionCase

class TestFarmValuation(TransactionCase):
    def setUp(self):
        super().setUp()
        self.Product = self.env['product.template']
        self.product = self.Product.create({'name': 'Commodity Wheat', 'type': 'consu'})

    def test_01_market_price_sync(self):
        """ Test market price synchronization to product template """
        if 'farm.market.price' not in self.env:
            self.skipTest("farm.market.price model not found")
            
        self.env['farm.market.price'].create({
            'product_id': self.product.id,
            'unit_price': 2.5,
            'date': '2026-05-01'
        })
        
        # Trigger compute
        self.product._compute_market_price()
        self.assertEqual(self.product.market_price, 2.5)
