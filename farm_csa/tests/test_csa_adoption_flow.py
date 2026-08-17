# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestCSAAdoptionFlow(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        
        # 1. Create Customer
        cls.customer = cls.env['res.partner'].create({'name': 'John Doe'})
        
        # 2. Create Asset (Pig)
        cls.pig_product = cls.env['product.product'].create({
            'name': 'Organic Pig',
            'type': 'consu',
            'tracking': 'lot'
        })
        cls.pig_lot = cls.env['stock.lot'].create({
            'name': 'PIG-001',
            'product_id': cls.pig_product.id,
            'company_id': cls.env.company.id
        })
        
        # 3. Create Plan
        cls.plan = cls.env['farm.csa.plan'].create({
            'name': 'Pig Adoption Plan',
            'product_id': cls.pig_product.id,
            'frequency': 'monthly'
        })

    def test_01_adoption_triggers_feeding_and_twin(self):
        """
        Scenario:
        1. A customer subscribes to an 'adoption' type CSA plan.
        2. Activating the subscription automatically:
           - Triggers a 'feeding' intervention task.
           - Sets up a public stream URL for the adopted lot/twin.
        """
        sub = self.env['farm.csa.subscription'].create({
            'partner_id': self.customer.id,
            'plan_id': self.plan.id,
            'sub_type': 'adoption',
            'adopted_lot_id': self.pig_lot.id
        })
        
        sub.action_activate()
        self.assertEqual(sub.state, 'active')
        
        # Verify Feeding task created
        domain = [('intervention_type', '=', 'feeding')]
        if 'lot_producing_id' in self.env['mrp.production']._fields:
            domain.append(('lot_producing_id', '=', self.pig_lot.id))
        else:
            domain.append(('lot_producing_ids', 'in', [self.pig_lot.id]))
        interventions = self.env['mrp.production'].search(domain)
        self.assertTrue(interventions, "Activating adoption should trigger an initial feeding/care intervention.")
        
        # Verify Stream URL created
        self.assertTrue(self.pig_lot.csa_stream_url, "Activating adoption should provision a video stream URL.")
        self.assertIn("stream.farm", self.pig_lot.csa_stream_url)

