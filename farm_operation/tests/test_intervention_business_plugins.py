# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
import json
from datetime import datetime, timedelta

class TestInterventionBusinessPlugins(TransactionCase):
    """
    Test specialized agricultural plugins integrated via farm_operation.
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Intervention = cls.env['mrp.production'] # AgriIntervention implementation
        cls.Product = cls.env['product.product']
        cls.Location = cls.env['farm.location']
        
        # 1. Setup fertilizer with nutrient content
        cls.fertilizer = cls.Product.create({
            'name': 'Super NPK',
            'standard_price': 10.0,
            'n_content': 20.0,
            'p_content': 10.0,
            'k_content': 10.0,
        })
        
        # 2. Setup crop for harvesting
        cls.apple = cls.Product.create({
            'name': 'Red Apple',
            'type': 'product',
            'tracking': 'lot',
        })
        
        # 3. Setup Organic Parcel
        cls.parcel = cls.Location.create({
            'name': 'Organic Field A',
            'certification_level': 'organic',
        })

    def test_01_nutrient_plugin(self):
        """ Test Nutrient Mass Balance Plugin """
        intervention = self.Intervention.create({
            'product_id': self.apple.id,
            'product_qty': 1.0,
            'intervention_type': 'fertilizing',
            'move_raw_ids': [(0, 0, {
                'product_id': self.fertilizer.id,
                'product_uom_qty': 100.0, # 100kg
                'product_uom': self.fertilizer.uom_id.id,
                'location_id': self.env.ref('stock.stock_location_stock').id,
                'location_dest_id': self.env.ref('stock.location_production').id,
            })]
        })
        
        # Trigger Confirmation (which calls plugin)
        intervention.action_confirm()
        
        # 100kg * 20% N = 20kg Pure N
        self.assertEqual(intervention.pure_n_qty, 20.0)
        self.assertEqual(intervention.pure_p_qty, 10.0)
        self.assertEqual(intervention.pure_k_qty, 10.0)

    def test_02_compliance_plugin_real_name(self):
        """ Test China Real-name Registration (ID Card) """
        intervention = self.Intervention.create({
            'product_id': self.apple.id,
            'product_qty': 1.0,
            'intervention_type': 'protection',
            'operator_id_card': 'invalid_id',
        })
        
        with self.assertRaises(UserError):
            intervention.action_confirm()
            
        # Correct ID
        intervention.operator_id_card = '11010119900307123X'
        intervention.action_confirm()
        self.assertEqual(intervention.state, 'confirmed')

    def test_03_compliance_plugin_organic(self):
        """ Test Organic Blocking Plugin """
        # Create non-approved chemical
        bad_chemical = self.Product.create({
            'name': 'Forbidden Pesticide',
            'is_agri_input': True,
            'is_safety_approved': False,
        })
        
        # Create task linked to organic parcel
        task = self.env['project.task'].create({
            'name': 'Spraying Task',
            'land_parcel_id': self.parcel.id,
        })
        
        intervention = self.Intervention.create({
            'product_id': self.apple.id,
            'product_qty': 1.0,
            'intervention_type': 'protection',
            'agri_task_id': task.id,
            'operator_id_card': '11010119900307123X',
            'move_raw_ids': [(0, 0, {
                'product_id': bad_chemical.id,
                'product_uom_qty': 1.0,
                'product_uom': bad_chemical.uom_id.id,
                'location_id': self.env.ref('stock.stock_location_stock').id,
                'location_dest_id': self.env.ref('stock.location_production').id,
            })]
        })
        
        # Should raise error and reset conversion date
        with self.assertRaises(UserError):
            intervention.action_confirm()
        
        self.assertTrue(self.parcel.last_prohibited_substance_date)

    def test_04_harvest_plugin_grading(self):
        """ Test Multi-grade Harvesting and QC Trigger """
        intervention = self.Intervention.create({
            'product_id': self.apple.id,
            'product_qty': 100.0,
            'intervention_type': 'harvesting',
            'grade_a_qty': 60.0,
            'grade_b_qty': 30.0,
            'grade_c_qty': 10.0,
        })
        intervention.action_confirm()
        intervention.action_assign()
        
        # Finish work (triggers Harvest Plugin)
        intervention.button_mark_done()
        
        # Verify 3 lots were created
        lots = self.env['stock.lot'].search([('product_id', '=', self.apple.id)])
        # filter by names containing GRADE
        grade_a_lots = lots.filtered(lambda l: 'GRADE_A' in l.name)
        self.assertTrue(grade_a_lots)
        
        # Verify 3 QC checks were created (requires farm_quality/farm_operation logic)
        qc_checks = self.env['farm.quality.check'].search([('name', 'like', intervention.name)])
        self.assertEqual(len(qc_checks), 3)

    def test_05_verification_plugin_drone(self):
        """ Test Drone Depletion Plugin """
        intervention = self.Intervention.create({
            'product_id': self.apple.id,
            'product_qty': 1.0,
            'intervention_type': 'aerial_spraying',
            'actual_flight_area': 10.0, # 10 units
            'move_raw_ids': [(0, 0, {
                'product_id': self.fertilizer.id,
                'product_uom_qty': 1.0, # Initial demand
                'product_uom': self.fertilizer.uom_id.id,
                'location_id': self.env.ref('stock.stock_location_stock').id,
                'location_dest_id': self.env.ref('stock.location_production').id,
            })]
        })
        intervention.action_confirm()
        
        # Simulate completion
        intervention.button_mark_done()
        
    def test_06_dna_certification_tainting(self):
        """ Test DNA Certification Tainting (Organic + Commodity -> Green) """
        # 1. Create one organic lot and one commodity lot
        organic_lot = self.env['stock.lot'].create({
            'name': 'ORG-INPUT-01',
            'product_id': self.fertilizer.id,
            'certification_type': 'organic',
        })
        commodity_lot = self.env['stock.lot'].create({
            'name': 'COM-INPUT-02',
            'product_id': self.fertilizer.id,
            'certification_type': False, # Commodity
        })
        
        # 2. Create intervention producing a lot, initially marked as organic
        intervention = self.Intervention.create({
            'product_id': self.apple.id,
            'product_qty': 100.0,
            'intervention_type': 'harvesting',
        })
        intervention.action_confirm()
        
        # Manually create output move with a lot
        output_move = self.env['stock.move'].create({
            'name': 'Harvest',
            'product_id': self.apple.id,
            'product_uom_qty': 100.0,
            'location_id': self.env.ref('stock.location_production').id,
            'location_dest_id': self.env.ref('stock.stock_location_stock').id,
            'production_id': intervention.id,
            'state': 'done',
        })
        output_lot = self.env['stock.lot'].create({
            'name': 'OUTPUT-LOT-99',
            'product_id': self.apple.id,
            'certification_type': 'organic',
        })
        output_move.lot_ids = [(6, 0, [output_lot.id])]
        
        # 3. Define raw moves using the lots
        raw_move_1 = self.env['stock.move'].create({
            'name': 'Input 1',
            'product_id': self.fertilizer.id,
            'product_uom_qty': 50.0,
            'raw_material_production_id': intervention.id,
            'lot_ids': [(6, 0, [organic_lot.id])],
        })
        raw_move_2 = self.env['stock.move'].create({
            'name': 'Input 2',
            'product_id': self.fertilizer.id,
            'product_uom_qty': 50.0,
            'raw_material_production_id': intervention.id,
            'lot_ids': [(6, 0, [commodity_lot.id])],
        })
        
        # 4. Trigger DNA Inheritance
        output_lot.inherit_dna_from_source(intervention.move_raw_ids)
        
        # Verify output lot was tainted/downgraded to 'green'
        self.assertEqual(output_lot.certification_type, 'green', "Lot should be downgraded to Green due to non-organic input")
        
        # Verify chatter notification
        messages = self.env['mail.message'].search([('res_id', '=', output_lot.id), ('model', '=', 'stock.lot')])
        self.assertTrue(any("DNA Tainting" in m.body for m in messages))

    def test_07_lot_kinship_tracking(self):
        """ Test Lot Kinship / Ancestry recording """
        # 1. Create parent lots
        parent_lot_1 = self.env['stock.lot'].create({
            'name': 'P-LOT-01',
            'product_id': self.fertilizer.id,
        })
        parent_lot_2 = self.env['stock.lot'].create({
            'name': 'P-LOT-02',
            'product_id': self.fertilizer.id,
        })
        
        # 2. Create output lot
        child_lot = self.env['stock.lot'].create({
            'name': 'C-LOT-01',
            'product_id': self.apple.id,
        })
        
        # 3. Simulate inputs via stock moves
        intervention = self.Intervention.create({
            'product_id': self.apple.id,
            'product_qty': 1.0,
            'intervention_type': 'process',
        })
        
        inputs = self.env['stock.move'].create([
            {
                'name': 'In 1',
                'product_id': self.fertilizer.id,
                'product_uom_qty': 1.0,
                'raw_material_production_id': intervention.id,
                'lot_ids': [(6, 0, [parent_lot_1.id])],
            },
            {
                'name': 'In 2',
                'product_id': self.fertilizer.id,
                'product_uom_qty': 1.0,
                'raw_material_production_id': intervention.id,
                'lot_ids': [(6, 0, [parent_lot_2.id])],
            }
        ])
        
        # 4. Trigger DNA Inheritance (which now includes kinship)
        child_lot.inherit_dna_from_source(inputs)
        
        # 5. Verify Kinship records
        kinship_links = self.env['agri.lot.kinship'].search([('child_lot_id', '=', child_lot.id)])
        self.assertEqual(len(kinship_links), 2, "Should have 2 parent kinship links")
        
        parents = kinship_links.mapped('parent_lot_id')
        self.assertIn(parent_lot_1, parents)
        self.assertIn(parent_lot_2, parents)
        self.assertEqual(kinship_links[0].derivation_type, 'process')
        
        # Check reverse relation on parent
        descendants = parent_lot_1.child_kinship_ids.mapped('child_lot_id')
        self.assertIn(child_lot, descendants)
