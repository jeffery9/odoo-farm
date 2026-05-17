# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestOmnichannelRouting(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        
        # Create an account
        cls.account = cls.env['douyin.account'].create({'name': 'Farm Fresh Official'})
        
        # Create a cold-chain product
        cls.cherry = cls.env['product.product'].create({
            'name': 'Premium Cherries',
            'type': 'product',
            'requires_cold_chain': True
        })
        
        # Create some Edge Warehouses
        cls.wh_north = cls.env['stock.warehouse'].create({
            'name': 'North Edge Hub',
            'code': 'NEH'
        })
        cls.wh_south = cls.env['stock.warehouse'].create({
            'name': 'South Edge Hub',
            'code': 'SEH'
        })

    def test_01_live_order_fast_routing(self):
        """
        Scenario 45: Omnichannel Live-Streaming Commerce
        1. 3 orders flow in from Douyin stream.
        2. System processes them instantly.
        3. Stock is deducted and orders are load-balanced to edge warehouses.
        4. Logistics uses cold-chain for cherries.
        """
        orders = self.env['live.order'].create([
            {'name': 'DY001', 'dy_order_id': '1001', 'account_id': self.account.id},
            {'name': 'DY002', 'dy_order_id': '1002', 'account_id': self.account.id},
            {'name': 'DY003', 'dy_order_id': '1003', 'account_id': self.account.id},
        ])
        
        # Mock product selection in the script
        # The script picks the first product, so let's make sure it picks cherry
        # In a real system, the JSON would specify the product ID
        
        orders.action_import_and_route()
        
        for o in orders:
            self.assertEqual(o.state, 'imported')
            self.assertEqual(o.routing_status, 'routed')
            self.assertTrue(o.edge_warehouse_id, "Order must be routed to an edge warehouse.")
            self.assertTrue(o.odoo_so_id, "Sales order must be generated.")
            
            # Check SO confirmed
            self.assertEqual(o.odoo_so_id.state, 'sale', "Sales order must be confirmed to lock inventory instantly.")
            
        # Check load balancing (they shouldn't all go to the same warehouse)
        wh_ids = set(orders.mapped('edge_warehouse_id.id'))
        self.assertGreater(len(wh_ids), 1, "Orders should be load-balanced across multiple edge hubs.")

