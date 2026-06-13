# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
import json
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)

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
            'type': 'consu',
            'tracking': 'lot', # REQUIRED for lot linkage
        })
        
        # 2. Setup crop for harvesting
        cls.apple = cls.Product.create({
            'name': 'Red Apple',
            'type': 'consu',
            'tracking': 'lot',
        })
        
        # 3. Setup Organic Parcel
        # Create a production location if it doesn't exist
        cls.production_location = cls.env['stock.location'].create({
            'name': 'Virtual Production',
            'usage': 'production',
        })
        
        cls.parcel = cls.Location.create({
            'name': 'Organic Field A',
            'certification_type': 'organic',
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
                'location_dest_id': self.production_location.id,
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
        # Create a regulated input (e.g. pesticide)
        pesticide = self.Product.create({
            'name': 'Regulated Pesticide',
            'type': 'consu',
            'is_regulated_input': True,
        })
        
        intervention = self.Intervention.create({
            'product_id': self.apple.id,
            'product_qty': 1.0,
            'intervention_type': 'protection',
            'operator_id_card': 'invalid_id',
            'move_raw_ids': [(0, 0, {
                'product_id': pesticide.id,
                'product_uom_qty': 1.0,
                'product_uom': pesticide.uom_id.id,
                'location_id': self.env.ref('stock.stock_location_stock').id,
                'location_dest_id': self.production_location.id,
            })]
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
            'type': 'consu',
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
                'location_dest_id': self.production_location.id,
            })]
        })
        
        # Should raise error
        with self.assertRaises(UserError):
            intervention.action_confirm()
            
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
        
        # Verify 3 lots were created (filter out ungraded lots created by Odoo's default logic if any)
        lots = self.env['stock.lot'].search([
            ('product_id', '=', self.apple.id),
            ('quality_grade', '!=', 'ungraded')
        ])
        self.assertEqual(len(lots), 3, "Should have created 3 graded lots")
        self.assertTrue(any(l.quality_grade == 'grade_a' for l in lots), "Should have a Grade A lot")
        
        # Verify 3 QC checks were created (requires farm_quality/farm_operation logic)
        if 'farm.quality.check' in self.env:
            qc_checks = self.env['farm.quality.check'].search([('name', 'like', intervention.name)])
            self.assertEqual(len(qc_checks), 3)

    def test_05_verification_plugin_drone(self):
        """ Test Drone Depletion Plugin """
        # Create a lot for the tracked fertilizer
        ferti_lot = self.env['stock.lot'].create({
            'name': 'FERTI-LOT-DRONE',
            'product_id': self.fertilizer.id,
        })
        
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
                'location_dest_id': self.production_location.id,
                'move_line_ids': [(0, 0, {
                    'product_id': self.fertilizer.id,
                    'lot_id': ferti_lot.id,
                    'quantity': 1.0,
                    'location_id': self.env.ref('stock.stock_location_stock').id,
                    'location_dest_id': self.production_location.id,
                })],
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
            'product_id': self.apple.id,
            'product_uom_qty': 100.0,
            'location_id': self.production_location.id,
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
            'product_id': self.fertilizer.id,
            'product_uom_qty': 50.0,
            'raw_material_production_id': intervention.id,
            'move_line_ids': [(0, 0, {
                'product_id': self.fertilizer.id,
                'lot_id': organic_lot.id,
                'quantity': 50.0,
                'location_id': self.env.ref('stock.stock_location_stock').id,
                'location_dest_id': self.production_location.id,
            })],
        })
        raw_move_2 = self.env['stock.move'].create({
            'product_id': self.fertilizer.id,
            'product_uom_qty': 50.0,
            'raw_material_production_id': intervention.id,
            'move_line_ids': [(0, 0, {
                'product_id': self.fertilizer.id,
                'lot_id': commodity_lot.id,
                'quantity': 50.0,
                'location_id': self.env.ref('stock.stock_location_stock').id,
                'location_dest_id': self.production_location.id,
            })],
        })
        
        self.env.flush_all()
        # 4. Trigger DNA Inheritance
        output_lot.inherit_dna_from_source(intervention.move_raw_ids)
        
        # Verify output lot was tainted/downgraded to 'green'
        output_lot.invalidate_recordset(['certification_type'])
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
        
        # 3. Simulate inputs via stock moves (Create one by one to avoid Odoo 19 recordset bug in _set_lot_ids)
        intervention = self.Intervention.create({
            'product_id': self.apple.id,
            'product_qty': 1.0,
            'intervention_type': 'process',
        })
        
        move1 = self.env['stock.move'].create({
            'product_id': self.fertilizer.id,
            'product_uom_qty': 1.0,
            'raw_material_production_id': intervention.id,
            'move_line_ids': [(0, 0, {
                'product_id': self.fertilizer.id,
                'lot_id': parent_lot_1.id,
                'quantity': 1.0,
                'location_id': self.env.ref('stock.stock_location_stock').id,
                'location_dest_id': self.production_location.id,
            })],
        })
        move2 = self.env['stock.move'].create({
            'product_id': self.fertilizer.id,
            'product_uom_qty': 1.0,
            'raw_material_production_id': intervention.id,
            'move_line_ids': [(0, 0, {
                'product_id': self.fertilizer.id,
                'lot_id': parent_lot_2.id,
                'quantity': 1.0,
                'location_id': self.env.ref('stock.stock_location_stock').id,
                'location_dest_id': self.production_location.id,
            })],
        })
        inputs = move1 + move2
        self.env.flush_all()
        
        # 4. Trigger DNA Inheritance (which now includes kinship)
        child_lot.inherit_dna_from_source(inputs)
        self.env.flush_all()
        
        # 5. Verify Kinship records
        # Use filtered on all records of the child lot to be more robust across Odoo versions
        # or search by child_lot_id Many2one which should be reliable.
        self.env['agri.lot.kinship'].invalidate_model()
        kinship_links = self.env['agri.lot.kinship'].search([('child_lot_id', '=', child_lot.id)])
        
        _logger.info("TEST: Found %s kinships for child lot %s", len(kinship_links), child_lot.name)
        if len(kinship_links) < 2:
             # Fallback check for debug
             all_k = self.env['agri.lot.kinship'].search([])
             _logger.info("TEST: All kinships in DB: %s", [(k.parent_lot_id.name, k.child_lot_id.name) for k in all_k])
             
        self.assertEqual(len(kinship_links), 2, "Should have 2 parent kinship links")
        
        parents = kinship_links.mapped('parent_lot_id')
        self.assertIn(parent_lot_1, parents)
        self.assertIn(parent_lot_2, parents)
        self.assertEqual(kinship_links[0].derivation_type, 'process')
        
        # Check reverse relation on parent
        descendants = parent_lot_1.child_kinship_ids.mapped('child_lot_id')
        self.assertIn(child_lot, descendants)

    def test_08_entity_compliance_trust_dna(self):
        """ Test Entity Compliance -> Lot Integrity linkage """
        if 'farm.entity' not in self.env:
            return

        # 1. Setup Farm Entity and Franchise with 'warning' status
        farm_entity = self.env['farm.entity'].create({
            'name': 'Warning Farm',
            'code': 'WF-01',
            'company_id': self.env.company.id,
        })
        franchise = self.env['franchise.farm'].create({
            'name': 'Warning Franchise',
            'code': 'WF-FR-01',
            'farm_entity_id': farm_entity.id,
            'compliance_status': 'warning',
        })
        
        # 2. Create intervention in this farm
        intervention = self.Intervention.create({
            'product_id': self.apple.id,
            'product_qty': 100.0,
            'intervention_type': 'harvesting',
            'location_id': self.parcel.id,
        })
        intervention.action_confirm()
        
        # 3. Create output lot
        output_lot = self.env['stock.lot'].create({
            'name': 'TRUST-LOT-01',
            'product_id': self.apple.id,
            'quality_status': 'passed', # Base status is good
        })
        
        # 4. Trigger DNA Inheritance (which calls Entity Compliance plugin)
        # Using a dummy move for context
        move = self.env['stock.move'].create({
            'product_id': self.apple.id,
            'product_uom_qty': 100.0,
            'location_id': self.production_location.id,
            'location_dest_id': self.env.ref('stock.stock_location_stock').id,
            'production_id': intervention.id,
            'state': 'done',
        })
        output_lot.inherit_dna_from_source(move)
        
        # 5. Verify results
        self.assertEqual(output_lot.entity_audit_status, 'warning', "Lot should capture farm's warning status")
        
        # Check integrity score (Base 100 * 0.8 multiplier for warning)
        # Formula: (geofence 100*0.4 + input 100*0.4 + qc 100*0.2) * 0.8 = 80.0
        # Wait, geofence check logic in _compute_integrity_score depends on quality_status
        # lot.quality_status is 'passed' (not 'healthy'), so geofence compliance is 80.0
        # score = (80*0.4 + 100*0.4 + 100*0.2) * 0.8 = (32 + 40 + 20) * 0.8 = 92 * 0.8 = 73.6
        self.assertLess(output_lot.integrity_score, 100.0)
        self.assertEqual(output_lot.integrity_score, 73.6)
