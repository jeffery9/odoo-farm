# -*- coding: utf-8 -*-
from odoo.tests.common import tagged
from odoo.exceptions import ValidationError, UserError
from .test_stock_matter_tracking import TestStockMatterTrackingBase

@tagged('post_install', '-at_install')
class TestSfcMapping(TestStockMatterTrackingBase):
    @classmethod
    def setUpClass(cls):
        super(TestSfcMapping, cls).setUpClass()
        cls.TreatmentBatch = cls.env['agri.treatment.batch']
        cls.Link = cls.env['stock.matter.tracking.link']

    def test_01_carrier_transition_rules(self):
        """ Test Carrier State Transition Whitelist Rules Matrix """
        # Create a new carrier container
        carrier_package = self.env['stock.package'].create({'name': 'SFC-TEST-TRANS-01'})
        carrier = self.Tracking.create({
            'package_id': carrier_package.id,
        })
        self.assertEqual(carrier.carrier_state, 'idle', "Carrier should initialize in idle state.")

        # 1. Test illegal state transition: idle -> qc (not allowed, raises UserError)
        with self.assertRaises(UserError):
            carrier.write({'carrier_state': 'qc'})

        # 2. Test allowed transition: idle -> loading (allowed)
        carrier.write({'carrier_state': 'loading'})
        self.assertEqual(carrier.carrier_state, 'loading')

        # 3. Test illegal transition: loading -> done (not allowed)
        with self.assertRaises(UserError):
            carrier.write({'carrier_state': 'done'})

        # 4. Test allowed sequence: loading -> processing -> qc -> done -> consumed
        carrier.write({'carrier_state': 'processing'})
        self.assertEqual(carrier.carrier_state, 'processing')

        carrier.write({'carrier_state': 'qc'})
        self.assertEqual(carrier.carrier_state, 'qc')

        carrier.write({'carrier_state': 'done'})
        self.assertEqual(carrier.carrier_state, 'done')

        carrier.write({'carrier_state': 'consumed'})
        self.assertEqual(carrier.carrier_state, 'consumed')

    def test_02_carrier_process_batch_and_admission_rules(self):
        """ Test batching controls and Admission Rule validations (core part) """
        carrier_p1 = self.env['stock.package'].create({'name': 'SFC-B1'})
        carrier_p2 = self.env['stock.package'].create({'name': 'SFC-B2'})
        
        carrier1 = self.Tracking.create({
            'package_id': carrier_p1.id,
            'dna_integrity_score': 100.0,
            'carrier_state': 'idle'
        })
        carrier2 = self.Tracking.create({
            'package_id': carrier_p2.id,
            'dna_integrity_score': 100.0,
            'carrier_state': 'loading'
        })

        carrier1.write({'carrier_state': 'loading'})

        # Create batch
        batch_vals = {
            'treatment_temperature': 45.5,
            'carrier_ids': [(6, 0, [carrier1.id, carrier2.id])]
        }
        if 'workcenter_id' in self.TreatmentBatch._fields:
            dummy_wc = self.env['mrp.workcenter'].create({'name': 'Dummy WC', 'code': 'DUMMY'})
            batch_vals['workcenter_id'] = dummy_wc.id

        batch = self.TreatmentBatch.create(batch_vals)
        self.assertEqual(batch.state, 'draft')

        # Test Admission Rule violation: state is qc, not idle/loading
        carrier1.with_context(bypass_carrier_transition_rules=True).write({'carrier_state': 'qc'})
        fail_state_vals = {
            'carrier_ids': [(6, 0, [carrier1.id])]
        }
        if 'workcenter_id' in self.TreatmentBatch._fields:
            fail_state_vals['workcenter_id'] = dummy_wc.id

        batch_fail_state = self.TreatmentBatch.create(fail_state_vals)
        with self.assertRaises(ValidationError):
            batch_fail_state.action_start()

        # Test Admission Rule violation: GxP/pedigree score too low (< 50)
        carrier1.with_context(bypass_carrier_transition_rules=True).write({
            'carrier_state': 'idle',
            'dna_integrity_score': 45.0
        })
        fail_dna_vals = {
            'carrier_ids': [(6, 0, [carrier1.id])]
        }
        if 'workcenter_id' in self.TreatmentBatch._fields:
            fail_dna_vals['workcenter_id'] = dummy_wc.id

        batch_fail_dna = self.TreatmentBatch.create(fail_dna_vals)
        with self.assertRaises(ValidationError):
            batch_fail_dna.action_start()

    def test_03_carrier_graph_edges_and_bidirectional_tracing(self):
        """ Test that splits/merges generate graph edges and that CTE tracing resolves correct trees """
        # Create parent source container (empty carrier)
        parent = self.Tracking.create({
            'dna_integrity_score': 100.0,
            'carrier_state': 'processing'
        })
        
        # Add stock quantities to parent container
        self.Quant.create({
            'product_id': self.product_apple.id,
            'quantity': 250.0,
            'location_id': self.location_vessel.id,
            'package_id': parent.package_id.id
        })
        parent._recalculate_consolidation_properties()

        # 1. Execute Fission Split (Parent -> Child1, Child2)
        target_products_data = [
            {'product_id': self.product_apple.id, 'quantity': 100.0, 'lot_name': 'SFC-CHILD1'},
            {'product_id': self.product_apple.id, 'quantity': 150.0, 'lot_name': 'SFC-CHILD2'}
        ]
        children = parent.action_execute_fission(target_products_data)
        self.assertEqual(len(children), 2)
        child1, child2 = children[0], children[1]

        # Verify Split Edges/Links created in DAG
        split_links = self.Link.search([('parent_id', '=', parent.id)])
        self.assertEqual(len(split_links), 2, "Two directed split edges should be logged.")
        self.assertTrue(all(l.transition_type == 'split' for l in split_links))
        self.assertEqual(set(split_links.mapped('child_id').ids), {child1.id, child2.id})

        # 2. Execute Consolidation Merge (Child1 + Child2 -> TARGET)
        target = self.Tracking.create({
            'dna_integrity_score': 100.0,
            'carrier_state': 'idle'
        })

        target.action_execute_merge(children)

        # Verify Merge Edges/Links created in DAG
        merge_links = self.Link.search([('child_id', '=', target.id)])
        self.assertEqual(len(merge_links), 2, "Two directed merge edges should be logged.")
        self.assertTrue(all(l.transition_type == 'merge' for l in merge_links))
        self.assertEqual(set(merge_links.mapped('parent_id').ids), {child1.id, child2.id})

        # Verify source states transitioned to consumed and target is ready/loading
        self.assertEqual(child1.carrier_state, 'consumed')
        self.assertEqual(child2.carrier_state, 'consumed')
        self.assertEqual(target.carrier_state, 'loading')

        # 3. Verify Bidirectional Recursive CTE Tracing Queries
        # Upstream Trace: target should find both child records and the original parent
        upstream_ancestors = target.action_trace_upstream()
        self.assertEqual(set(upstream_ancestors.ids), {child1.id, child2.id, parent.id})

        # Downstream Trace: parent should find both child records and the final target
        downstream_descendants = parent.action_trace_downstream()
        self.assertEqual(set(downstream_descendants.ids), {child1.id, child2.id, target.id})
