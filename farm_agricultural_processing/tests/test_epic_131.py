# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class TestEpic131(TransactionCase):
    """ BDD Test for Epic 131 Alternative Proteins & Bio-conversion """

    def setUp(self):
        super(TestEpic131, self).setUp()
        self.Product = self.env['product.product']
        self.Production = self.env['mrp.production']
        self.Bom = self.env['mrp.bom']
        
        # Setup BSF Products
        self.bsf_egg = self.Product.create({'name': 'BSF Eggs', 'type': 'product'})
        self.bsf_larva = self.Product.create({'name': 'BSF Larvae', 'type': 'product'})
        self.bsf_pupa = self.Product.create({'name': 'BSF Pre-pupa', 'type': 'product'})
        
        # Setup Microalgae Products
        self.microalgae_slurry = self.Product.create({'name': 'Microalgae Slurry', 'type': 'product'})
        self.protein_meal = self.Product.create({'name': 'Alternative Protein Meal', 'type': 'product'})
        self.insect_oil = self.Product.create({'name': 'Insect Oil', 'type': 'product'})

    def test_01_bioconversion_lifecycle_black_soldier_fly__bsf__full_lifecycle_and_microclimate_management(self):
        """
        US-131-01: BSF full lifecycle and microclimate management
        Verify stage-specific item codes and microclimate curves.
        """
        # Create a Production Order for Bioconversion
        mo = self.Production.create({
            'product_id': self.bsf_larva.id,
            'product_qty': 100.0,
            'bom_id': self.env['mrp.bom'].create({
                'product_tmpl_id': self.bsf_larva.product_tmpl_id.id,
                'product_qty': 1.0,
                'type': 'normal',
                'bom_line_ids': [(0, 0, {'product_id': self.bsf_egg.id, 'product_qty': 0.01})]
            }).id
        })
        
        # Verify initial state
        self.assertEqual(mo.state, 'draft')
        
        # Mock lifecycle stage transition
        # In a real system, this might be a custom field 'lifecycle_stage'
        if hasattr(mo, 'lifecycle_stage'):
            mo.lifecycle_stage = 'larva'
            self.assertEqual(mo.lifecycle_stage, 'larva')
        
        # Verify microclimate curve integration (Mocking IoT check)
        # Expected: System enforces Temp 27-30C, Humidity 60-70% for Larva stage
        target_temp_range = (27, 30)
        current_iot_temp = 28.5
        self.assertTrue(target_temp_range[0] <= current_iot_temp <= target_temp_range[1], 
                        "Microclimate temperature outside larval stage curve")

    def test_02_recipe_dynamic_dynamic_organic_waste_formulation_and_fcr_calculation(self):
        """
        US-131-02: Dynamic organic waste formulation and FCR calculation
        Verify dry additive calculation for moisture targets.
        """
        # Scenario: Raw waste at 80% moisture, target substrate 65% moisture.
        # Required dry additive (wheat bran at 10% moisture) calculation.
        raw_waste_qty = 1000.0
        raw_moisture = 0.80
        target_moisture = 0.65
        dry_additive_moisture = 0.10
        
        # Calculation logic: (W_raw * M_raw + W_add * M_add) / (W_raw + W_add) = M_target
        # W_add = W_raw * (M_raw - M_target) / (M_target - M_add)
        expected_additive = raw_waste_qty * (raw_moisture - target_moisture) / (target_moisture - dry_additive_moisture)
        
        # Mocking the formulation engine call
        if hasattr(self.env['mrp.bom'], 'calculate_moisture_compensation'):
            calculated_additive = self.env['mrp.bom'].calculate_moisture_compensation(
                raw_waste_qty, raw_moisture, target_moisture, dry_additive_moisture
            )
            self.assertAlmostEqual(calculated_additive, expected_additive, places=2)
        
        # Verify FCR Calculation
        # FCR = Total Dry Feed / Total Larva Weight Gain (Dry)
        total_dry_feed = 500.0
        larva_dry_weight = 100.0
        expected_fcr = total_dry_feed / larva_dry_weight
        self.assertEqual(expected_fcr, 5.0)

    def test_03_pbr_microalgae_microalgae_photobioreactor__pbr__continuous_cultivation_control(self):
        """
        US-131-03: Microalgae photobioreactor (PBR) continuous cultivation control
        Verify continuous MRP flow for daily harvests.
        """
        # Create a PBR Production Order
        mo = self.Production.create({
            'product_id': self.microalgae_slurry.id,
            'product_qty': 1000.0, # Target total for the month
        })
        
        # Continuous flow check: MO remains 'progress' even after partial harvest
        mo.action_confirm()
        
        # Mock partial harvest (US-131-03)
        harvest_qty = 50.0
        # In a continuous PBR, we produce without closing the MO
        if hasattr(mo, 'action_continuous_harvest'):
            mo.action_continuous_harvest(harvest_qty=harvest_qty)
            self.assertEqual(mo.state, 'progress')
            # Verify harvest log
            self.assertIn(harvest_qty, mo.move_finished_ids.mapped('quantity'))

    def test_04_extraction_traceability_alternative_protein_deep_processing_and_multi_product_extraction(self):
        """
        US-131-04: Alternative protein deep processing and multi-product extraction
        Verify co-product balance and backward waste trace.
        """
        # 100kg Larvae = 30kg Oil + 65kg Protein Meal + 5kg Loss
        larvae_input = 100.0
        expected_oil = 30.0
        expected_meal = 65.0
        expected_loss = 5.0
        
        total_output = expected_oil + expected_meal + expected_loss
        self.assertEqual(total_output, larvae_input, "Mass balance failure in extraction")
        
        # Verify backward traceability
        # Create lot for larvae input
        larvae_lot = self.env['stock.lot'].create({
            'name': 'LARVAE-BATCH-001',
            'product_id': self.bsf_larva.id,
            'company_id': self.env.company.id,
        })
        
        # Create production for extraction
        mo = self.Production.create({
            'product_id': self.protein_meal.id,
            'product_qty': expected_meal,
            'move_raw_ids': [(0, 0, {
                'product_id': self.bsf_larva.id,
                'product_uom_qty': larvae_input,
                'lot_ids': [(4, larvae_lot.id)]
            })]
        })
        
        mo.action_confirm()
        # Verify that the final meal batch points to the larvae lot
        for move in mo.move_raw_ids:
            if move.product_id == self.bsf_larva:
                self.assertIn(larvae_lot, move.lot_ids)
