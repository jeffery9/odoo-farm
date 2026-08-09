# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from datetime import datetime, timedelta

class TestStockMatterTrackingBase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestStockMatterTrackingBase, cls).setUpClass()
        cls.Product = cls.env['product.product']
        cls.Lot = cls.env['stock.lot']
        cls.Location = cls.env['stock.location']
        cls.Tracking = cls.env['stock.matter.tracking']
        cls.Quant = cls.env['stock.quant']
        cls.BiologicalAsset = cls.env['agri.biological.asset']
        
        # Create test products
        cls.product_apple = cls.Product.create({
            'name': 'Organic Red Apple',
            'type': 'consu',
            'is_storable': True
        })
        
        # Create test lots
        cls.lot_a = cls.Lot.create({
            'name': 'LOT-APP-001',
            'product_id': cls.product_apple.id
        })
        
        # Create test location
        cls.location_vessel = cls.Location.create({
            'name': 'Staging Bin A',
            'usage': 'internal'
        })

        # Create individual biological asset for tracking
        cls.biological_asset = cls.BiologicalAsset.create({
            'name': 'Cow #1204',
            'agricultural_type': 'animal'
        })

    def test_01_delegation_creation_and_sequence(self):
        """ Test that creating a stock.matter.tracking record automatically creates stock.package with sequence name """
        tracking = self.Tracking.create({
            'vessel_phase': 'idle'
        })
        
        self.assertTrue(tracking.package_id, "Underlying package must be automatically created via delegation.")
        self.assertTrue(tracking.name.startswith('MAT-'), "Name should be generated automatically from the sequence.")
        self.assertEqual(tracking.vessel_phase, 'idle')

    def test_02_gxp_sealing_and_expiration(self):
        """ Test sealing the vessel starts the GxP clean-hold timer """
        tracking = self.Tracking.create({
            'vessel_phase': 'idle'
        })
        
        # Seal vessel
        tracking.action_seal_vessel()
        self.assertEqual(tracking.vessel_phase, 'ready')
        self.assertTrue(tracking.gxp_open_time)
        self.assertTrue(tracking.gxp_expiry_time)
        
        # Check clean-hold 24h duration
        expected_expiry = tracking.gxp_open_time + timedelta(hours=24)
        self.assertAlmostEqual(
            tracking.gxp_expiry_time.timestamp(),
            expected_expiry.timestamp(),
            delta=5,
            msg="GxP clean-hold limit must be exactly 24 hours from opening."
        )

    def test_03_biological_asset_individual_tracking(self):
        """ Test linking an individual biological asset for agricultural tracking """
        tracking = self.Tracking.create({
            'vessel_phase': 'idle',
            'biological_asset_id': self.biological_asset.id
        })
        
        self.assertEqual(tracking.biological_asset_id, self.biological_asset)

    def test_04_before_state_snapshot_capture(self):
        """ Test that changing process phase automatically captures a Before-State snapshot """
        tracking = self.Tracking.create({
            'vessel_phase': 'idle',
            'biological_asset_id': self.biological_asset.id
        })
        
        # Capture first snapshot by changing phase
        self.assertEqual(len(tracking.snapshot_ids), 0)
        
        # Trigger transition
        tracking.write({'vessel_phase': 'ready'})
        
        # A snapshot of the 'idle' phase should have been captured before transitioning to 'ready'
        self.assertEqual(len(tracking.snapshot_ids), 1, "A snapshot must be automatically captured on state transitions.")
        snapshot = tracking.snapshot_ids[0]
        self.assertEqual(snapshot.vessel_phase, 'idle', "The snapshot must capture the BEFORE-state of the vessel.")
        self.assertEqual(snapshot.biological_asset_id, self.biological_asset, "The snapshot must preserve individual biological asset context.")

    def test_05_dna_ancestry_and_purity(self):
        """ Test the matter-trinity dna computation """
        tracking = self.Tracking.create({
            'vessel_phase': 'idle'
        })
        
        # Place quant inside the package
        quant = self.Quant.create({
            'product_id': self.product_apple.id,
            'lot_id': self.lot_a.id,
            'quantity': 10.0,
            'location_id': self.location_vessel.id,
            'package_id': tracking.package_id.id
        })
        
        # Recompute
        tracking._compute_lot_ids()
        
        # Verify lot ancestry is detected on the tracking record
        self.assertIn(self.lot_a, tracking.lot_ids, "DNA lot must be propagated and displayed on the Matter Tracking record.")

    def test_06_adaptive_enforcement_computation(self):
        """ Test that changing a category enforcement level correctly propagates active level """
        tracking = self.Tracking.create({'vessel_phase': 'idle'})
        
        # Base category default is 'guidance'
        self.assertEqual(tracking.active_enforcement_level, 'guidance')
        
        # Update product category to strict
        self.product_apple.categ_id.matter_enforcement_level = 'strict'
        
        # Link product quant to tracking vessel
        self.Quant.create({
            'product_id': self.product_apple.id,
            'quantity': 5.0,
            'location_id': self.location_vessel.id,
            'package_id': tracking.package_id.id
        })
        
        # Trigger dependency compute
        tracking._compute_active_enforcement()
        self.assertEqual(tracking.active_enforcement_level, 'strict', "Active level must resolve to strict if any contained product is high-risk.")

    def test_07_fission_split_math_and_dna_decay(self):
        """ Test that executing fission generates child records, balances quantities, and applies DNA decay """
        # Set base tracking record with 100% DNA score
        parent_tracking = self.Tracking.create({
            'vessel_phase': 'ready',
            'dna_integrity_score': 100.0,
            'location_id': self.location_vessel.id
        })
        
        # Split target data representing carcass division
        target_splits = [
            {'product_id': self.product_apple.id, 'quantity': 4.0, 'lot_name': 'SPLIT-1'},
            {'product_id': self.product_apple.id, 'quantity': 6.0, 'lot_name': 'SPLIT-2'}
        ]
        
        child_records = parent_tracking.action_execute_fission(target_splits)
        
        self.assertEqual(len(child_records), 2, "Must create exactly 2 split offspring vessels.")
        self.assertEqual(parent_tracking.vessel_phase, 'dirty', "Parent vessel must be marked dirty/depleted.")
        
        # Verify DNA Integrity score decay (100 * 0.95 = 95.0%)
        for child in child_records:
            self.assertAlmostEqual(child.dna_integrity_score, 95.0, delta=0.1, msg="Offspring must inherit decayed DNA integrity score.")

    def test_08_matter_physical_properties_and_geofencing(self):
        """ Test weight tracking, GPS alignment, and Ray-casting Plot geofencing inside Matter Tracking """
        tracking = self.Tracking.create({
            'vessel_phase': 'idle',
            'current_weight': 450.5,
            'life_stage': 'growing'
        })
        self.assertEqual(tracking.current_weight, 450.5)
        self.assertEqual(tracking.life_stage, 'growing')

        # Create land parcel with geojson polygon
        import json
        boundary = {
            "type": "Polygon",
            "coordinates": [[
                [120.0, 30.0],
                [121.0, 30.0],
                [121.0, 31.0],
                [120.0, 31.0],
                [120.0, 30.0]
            ]]
        }
        plot = self.env['farm.location'].create({
            'name': 'Greenhouse Poly Block A',
            'is_land_parcel': True,
            'boundary_geojson': json.dumps(boundary)
        })

        # Test GPS outside boundary
        matched_plot = tracking.action_update_location_by_gps(lat=29.5, lng=120.5)
        self.assertFalse(matched_plot)

        # Test GPS inside boundary
        matched_plot = tracking.action_update_location_by_gps(lat=30.5, lng=120.5)
        self.assertEqual(matched_plot, plot)
        self.assertEqual(tracking.location_id, plot)
        self.assertEqual(tracking.last_gps_lat, 30.5)


