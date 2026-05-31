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
        
        # Verify move quantity was updated based on flight area
        # Assuming BOM qty was 1.0, new qty should be 10.0
        self.assertEqual(intervention.move_raw_ids[0].product_uom_qty, 10.0)
