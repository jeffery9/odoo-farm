# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from datetime import timedelta

class TestJITHarvestFlow(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        
        cls.carrot = cls.env['product.product'].create({'name': 'Organic Carrot Box', 'type': 'product'})
        cls.plan = cls.env['farm.csa.plan'].create({
            'name': 'Weekend Carrot Box',
            'product_id': cls.carrot.id,
            'frequency': 'weekly'
        })
        
        # Create 3 subscribers needing delivery tomorrow
        tomorrow = fields.Date.today() + timedelta(days=1)
        for i in range(3):
            partner = cls.env['res.partner'].create({'name': f'CSA Customer {i}'})
            cls.env['farm.csa.subscription'].create({
                'partner_id': partner.id,
                'plan_id': cls.plan.id,
                'sub_type': 'bag',
                'state': 'active',
                'next_delivery_date': tomorrow
            })

    def test_01_jit_harvest_aggregation(self):
        """
        Scenario:
        1. 3 customers have CSA box deliveries scheduled for tomorrow.
        2. Farm Manager clicks "Aggregate JIT Harvest" on the CSA Plan.
        3. System automatically sums up the demand (3 boxes).
        4. System automatically generates a single Harvesting Intervention for 3 boxes.
        """
        intervention = self.plan.action_aggregate_jit_harvest()
        
        self.assertTrue(intervention, "A harvesting intervention must be created.")
        self.assertEqual(intervention.intervention_type, 'harvesting', "Intervention must be of type harvesting.")
        self.assertEqual(intervention.product_id.id, self.carrot.id, "Must harvest the correct crop.")
        self.assertEqual(intervention.product_qty, 3.0, "Quantity must exactly match aggregated demand (3 boxes).")
        self.assertIn("JIT CSA Aggregation", intervention.origin, "Origin traceability must link to CSA.")

