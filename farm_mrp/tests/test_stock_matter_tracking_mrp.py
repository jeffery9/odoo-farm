# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestStockMatterTrackingMrp(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestStockMatterTrackingMrp, cls).setUpClass()
        cls.Tracking = cls.env['stock.matter.tracking']
        cls.Workcenter = cls.env['mrp.workcenter']
        
        # We need a routing operation / phase
        # If mrp is installed, mrp.routing.workcenter is available
        cls.RoutingWorkcenter = cls.env['mrp.routing.workcenter']
        
        # Create a test workcenter and routing phase
        cls.workcenter = cls.Workcenter.create({
            'name': 'Mixing Station Alpha',
            'code': 'MIX-A',
            'time_start': 0,
            'time_stop': 0,
            'time_efficiency': 100,
        })
        
        # Create a test product and dummy BOM (bom_id is a not-null required field in Odoo 19 routing operations)
        cls.product_bom = cls.env['product.product'].create({
            'name': 'Test BOM Product',
            'type': 'consu',
            'is_storable': True
        })
        cls.bom = cls.env['mrp.bom'].create({
            'product_tmpl_id': cls.product_bom.product_tmpl_id.id,
            'product_qty': 1.0,
            'type': 'normal'
        })
        
        # Create dummy routing operation representing Mixing Phase
        cls.routing_phase = cls.RoutingWorkcenter.create({
            'name': 'Mixing Phase',
            'workcenter_id': cls.workcenter.id,
            'bom_id': cls.bom.id,
            'time_cycle': 30.0,
            'sequence': 10,
        })

    def test_01_mrp_vessel_locking_and_lockout(self):
        """ Test MRP physical vessel locking and cleaning lockout safety rules """
        tracking = self.Tracking.create({
            'vessel_phase': 'idle'
        })
        
        # Seal vessel (must be ready to lock)
        tracking.action_seal_vessel()
        self.assertEqual(tracking.vessel_phase, 'ready')
        
        # Lock vessel
        tracking.action_lock_vessel()
        self.assertTrue(tracking.is_vessel_locked, "Vessel must be physically locked to the station.")
        
        # Attempt cleaning while locked should raise UserError
        with self.assertRaises(UserError, msg="Cleaning a locked vessel must raise an exception."):
            tracking.action_clean_vessel()
            
        # Unlock vessel
        tracking.action_unlock_vessel()
        self.assertFalse(tracking.is_vessel_locked)
        
        # Clean vessel now succeeds
        tracking.action_clean_vessel()
        self.assertEqual(tracking.vessel_phase, 'cleaning')

    def test_02_mrp_routing_phase_transition_and_snapshot(self):
        """ Test that changing the MRP process phase triggers Before-State snapshot with phase info """
        tracking = self.Tracking.create({
            'vessel_phase': 'idle'
        })
        
        # Change phase
        tracking.write({
            'current_phase_id': self.routing_phase.id,
            'vessel_phase': 'ready'
        })
        
        # Verify snapshot captures before-state
        self.assertEqual(len(tracking.snapshot_ids), 1, "Snapshot must be captured automatically on phase change.")
        snapshot = tracking.snapshot_ids[0]
        self.assertEqual(snapshot.vessel_phase, 'idle')
        self.assertFalse(snapshot.phase_id, "The before-state snapshot had no process phase.")
        
        # Change phase again
        tracking.write({
            'vessel_phase': 'dirty'
        })
        
        # Now there should be 2 snapshots
        self.assertEqual(len(tracking.snapshot_ids), 2)
        latest_snapshot = tracking.snapshot_ids.sorted(key=lambda s: s.id, reverse=True)[0]
        self.assertEqual(latest_snapshot.vessel_phase, 'ready')
        self.assertEqual(latest_snapshot.phase_id, self.routing_phase, "The before-state snapshot must preserve the MRP routing phase.")
