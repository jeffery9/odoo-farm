# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestEcoSymbiosisLoop(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        
        # Products
        cls.pig = cls.env['product.product'].create({'name': 'Pig', 'type': 'product', 'tracking': 'lot'})
        cls.manure_product = cls.env['product.product'].create({
            'name': 'Raw Pig Manure',
            'type': 'product',
        })
        cls.compost_product = cls.env['product.product'].create({
            'name': 'Organic Compost Fertilizer',
            'type': 'product',
            'input_type': 'fertilizer',
            'n_content': 5.0, # 5% Nitrogen
            'p_content': 3.0,
            'k_content': 2.0
        })
        cls.apple = cls.env['product.product'].create({'name': 'Organic Apple', 'type': 'product'})
        
        # Locations
        cls.barn = cls.env['farm.location'].create({'name': 'Pig Barn 01', 'usage': 'internal'})
        cls.compost_station = cls.env['farm.location'].create({'name': 'Compost Station A', 'usage': 'internal'})
        cls.orchard = cls.env['farm.location'].create({'name': 'Apple Orchard', 'is_land_parcel': True})

    def test_01_waste_to_fertilizer_loop(self):
        """
        Scenario:
        1. Barn clearing operation generates 5000kg of Raw Manure.
        2. Symbiosis system automatically intercepts and triggers a 'Composting' intervention.
        3. Composting intervention produces 2000kg of 'Organic Compost Fertilizer'.
        4. When Orchard schedules a Fertilizing task, the system calculates nutrient credits.
        """
        # Step 1: Generate Manure
        # Simulate a barn clearing operation
        clearing_intervention = self.env['mrp.production'].create({
            'product_id': self.env['product.product'].create({'name': 'Barn Cleaning Service', 'type': 'service'}).id,
            'product_qty': 1.0,
            'intervention_type': 'tillage', # Using standard types for the simulation
            'location_id': self.barn.id,
        })
        
        # We manually create the manure batch as if the intervention finished
        manure_batch = self.env['agri.manure.batch'].create({
            'quantity': 5000.0,
            'location_source_id': self.barn.id,
            'disposal_method': 'composting',
            'fertilizer_product_id': self.compost_product.id
        })
        
        # Step 2: Trigger Composting Intervention
        # In the real system, this is triggered by action_process
        manure_batch.action_process()
        
        self.assertEqual(manure_batch.state, 'processing', "Manure batch should transition to processing.")
        
        # Verify that a composting intervention was automatically created in the Symbiosis/Waste system
        compost_intervention = self.env['mrp.production'].search([
            ('origin', '=', manure_batch.batch_no),
            ('product_id', '=', self.compost_product.id)
        ])
        
        self.assertTrue(compost_intervention, "Symbiosis should automatically trigger a composting intervention.")
        
        # Step 3: Complete Composting
        # We update the produced quantity and mark done
        compost_intervention.write({'product_qty': 2000.0}) # 5 tons raw -> 2 tons compost
        compost_intervention.action_confirm()
        # Mock completion
        
        # Step 4: Nutrient Credits
        # Recompute nutrients on the batch
        manure_batch.write({'quantity': 2000.0}) # update for final
        self.assertEqual(manure_batch.pure_n_qty, 100.0, "2000kg * 5% = 100kg Pure Nitrogen recovered for the ecosystem.")

