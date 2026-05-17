# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestCoopBulkProcurement(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        
        # Setup Coop & Members
        cls.coop_partner = cls.env['res.partner'].create({'name': 'Village Coop', 'is_company': True})
        cls.coop = cls.env['cooperative.entity'].create({'name': 'Village Coop', 'partner_id': cls.coop_partner.id})
        
        cls.farmers = []
        for i in range(3):
            p = cls.env['res.partner'].create({'name': f'Farmer {i}'})
            m = cls.env['cooperative.member'].create({'partner_id': p.id, 'cooperative_id': cls.coop.id})
            cls.farmers.append(m)
            
        cls.fertilizer = cls.env['product.product'].create({'name': 'Urea 50kg', 'type': 'product'})
        cls.supplier = cls.env['res.partner'].create({'name': 'MegaChem Factory'})

    def test_01_aggregate_micro_demands(self):
        """
        Scenario 16: Cooperative Bulk Procurement & Micro-Inventory
        1. 3 farmers request 5 bags of Urea each via the App (Internal Marketplace Demands).
        2. Coop admin aggregates them into a single Bulk Procurement.
        3. Upon confirmation, system settles the cost and allocates the stock to virtual micro-inventories.
        """
        # Step 1: Farmers post demands
        for farmer in self.farmers:
            self.env['internal.marketplace'].create({
                'name': 'Need Urea',
                'cooperative_id': self.coop.id,
                'supplier_member_id': farmer.id,
                'listing_type': 'demand',
                'product_id': self.fertilizer.id,
                'quantity': 5.0,
                'state': 'active'
            })
            
        # Step 2: Aggregate
        bulk_order = self.env['joint.procurement'].create({
            'name': 'Spring Fertilizer Bulk Order',
            'cooperative_id': self.coop.id,
            'supplier_id': self.supplier.id,
            'procurement_type': 'fertilizer',
            'total_amount': 1500.0, # Total cost negotiated with factory
        })
        
        bulk_order.action_aggregate_demands()
        self.assertEqual(len(bulk_order.procurement_lines), 3, "Should have aggregated 3 micro-demands into 3 lines.")
        self.assertEqual(sum(bulk_order.procurement_lines.mapped('quantity')), 15.0, "Total aggregated quantity should be 15.")
        
        demands = self.env['internal.marketplace'].search([('cooperative_id', '=', self.coop.id)])
        for d in demands:
            self.assertEqual(d.state, 'completed', "Demands should be marked completed after aggregation.")
            
        # Step 3: Confirm and allocate to micro-inventory
        bulk_order.action_confirm_and_allocate()
        self.assertEqual(bulk_order.state, 'completed')
        
        # Verify Settlements
        settlements = self.env['internal.settlement'].search([('to_entity_id', '=', self.coop_partner.id)])
        self.assertEqual(len(settlements), 3, "3 settlements should be generated.")
        
        # Verify Virtual Inventory routing via log messages (simplified check for the test)
        messages = bulk_order.message_ids.mapped('body')
        has_allocation_log = any("Micro-Inventory: Virtual: Farmer" in msg for msg in messages)
        self.assertTrue(has_allocation_log, "System must log the automatic allocation to the farmer's micro-inventory.")

