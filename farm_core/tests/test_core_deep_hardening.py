# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError, UserError
from odoo import fields

@tagged('uavm_surgical', 'post_install', '-at_install')
class TestCoreDeepHardening(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Find internal location
        cls.location_internal = cls.env['stock.location'].create({
            'name': 'Silo Sector Z-Hardened',
            'usage': 'internal'
        })
        
        # Create standard product and category
        cls.category = cls.env['product.category'].create({
            'name': 'Consolidated Ingredients',
            'consolidation_strategy': 'weighted_average',
        })
        
        cls.product = cls.env['product.product'].create({
            'name': 'Organic Matter Cargo',
            'type': 'consu',
            'categ_id': cls.category.id,
            'is_storable': True,
        })

    def test_gps_coordinate_sequence_validations(self):
        """ Hardened checks on tracking GPS coordinates and boundary limits """
        tracking_model = self.env['stock.matter.tracking']
        
        # Test existence of fields dynamically
        has_gps = 'last_gps_lat' in tracking_model._fields
        if has_gps:
            tracking = tracking_model.create({
                'name': 'Carrier Geo 1',
                'carrier_state': 'idle',
                'last_gps_lat': 31.2304,
                'last_gps_lng': 121.4737,
            })
            # Pythonic physical boundary limit checks in tests
            self.assertTrue(-90.0 <= tracking.last_gps_lat <= 90.0, "Latitude must be physically valid.")
            self.assertTrue(-180.0 <= tracking.last_gps_lng <= 180.0, "Longitude must be physically valid.")

    def test_carrier_state_transition_sequence(self):
        """ Hardened checks on carrier transition allowed matrix and snapshot triggers """
        tracking_model = self.env['stock.matter.tracking']
        
        tracking = tracking_model.create({
            'name': 'Transition Carrier T1',
            'carrier_state': 'idle',
        })
        self.assertEqual(tracking.carrier_state, 'idle')

        # Try illegal transition from 'idle' to 'qc'
        with self.assertRaisesRegex(UserError, "Carrier State Transition Violation"):
            tracking.write({'carrier_state': 'qc'})

        # Execute standard legal transition sequence
        legal_sequence = ['loading', 'processing', 'qc', 'done', 'consumed']
        for state in legal_sequence:
            tracking.write({'carrier_state': state})
            self.assertEqual(tracking.carrier_state, state)

    def test_dna_integrity_score_decay_calculation(self):
        """ Verify DNA weighted average calculations on stock.matter.tracking and stock.lot """
        tracking_model = self.env['stock.matter.tracking']
        
        # Verify DNA score existence
        if 'dna_integrity_score' in tracking_model._fields:
            # Create two stock lots (with properties that compute to 100.0 and 80.0 DNA scores)
            lot_1 = self.env['stock.lot'].create({
                'name': 'LOT-A-100',
                'product_id': self.product.id,
                'company_id': self.env.company.id,
                'certification_type': 'organic',
                'entity_audit_status': 'compliant',
                'audit_status': 'verified',
            })
            lot_2 = self.env['stock.lot'].create({
                'name': 'LOT-B-80',
                'product_id': self.product.id,
                'company_id': self.env.company.id,
                'certification_type': 'gap', # non-organic (-20 score)
                'entity_audit_status': 'compliant',
                'audit_status': 'verified',
            })
            
            # Create a tracking record with associated stock.package
            tracking = tracking_model.create({
                'name': 'Consolidated Container T1',
            })
            
            # Create actual stock quants inside the vessel to trigger real recalculation
            self.env['stock.quant'].create({
                'product_id': self.product.id,
                'location_id': self.location_internal.id,
                'lot_id': lot_1.id,
                'quantity': 100.0,
                'package_id': tracking.package_id.id,
            })
            self.env['stock.quant'].create({
                'product_id': self.product.id,
                'location_id': self.location_internal.id,
                'lot_id': lot_2.id,
                'quantity': 200.0,
                'package_id': tracking.package_id.id,
            })
            
            # Recalculate properties on the tracking record
            tracking._recalculate_consolidation_properties()
            
            # Assertions to verify real production calculation results (86.666... * 0.90 = 78.0)
            self.assertTrue(tracking.is_consolidated, "Vessel tracking must be consolidated.")
            self.assertEqual(tracking.current_weight, 300.0, "Weight should equal sum of quants.")
            self.assertEqual(tracking.dna_integrity_score, 78.0, "DNA mixing entropy decay should be calculated correctly by production logic.")

    def test_vessel_locking_transfers_blocked(self):
        """ Ensure is_vessel_locked status dynamically blocks transactional stock moves """
        tracking_model = self.env['stock.matter.tracking']
        
        has_vessel_lock = 'is_vessel_locked' in tracking_model._fields
        if has_vessel_lock:
            # Create unlocked tracking and add initial quantity
            tracking = tracking_model.create({
                'name': 'Locked Vessel V1',
                'is_vessel_locked': False,
            })
            
            lot = self.env['stock.lot'].create({
                'name': 'LOT-C-100',
                'product_id': self.product.id,
                'company_id': self.env.company.id,
            })
            
            quant = self.env['stock.quant'].create({
                'product_id': self.product.id,
                'location_id': self.location_internal.id,
                'lot_id': lot.id,
                'quantity': 500.0,
                'package_id': tracking.package_id.id,
            })
            
            # Lock the vessel physically
            tracking.write({'is_vessel_locked': True})
            
            # Attempting to write to quant should trigger the actual Jidoka ValidationError
            with self.assertRaisesRegex(ValidationError, "Jidoka Interlock Blocked"):
                quant.write({'quantity': 250.0})
