# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError

@tagged('post_install', '-at_install')
class TestGxpReverseRecall(TransactionCase):

    def setUp(self):
        super(TestGxpReverseRecall, self).setUp()
        self.Incident = self.env['agri.gxp.contamination.incident']
        
        # Create physical locations
        self.source_loc = self.env['stock.location'].create({
            'name': 'Standard Raw Material Bin',
            'usage': 'internal'
        })
        self.quarantine_loc = self.env['stock.location'].create({
            'name': 'GxP Quarantine Cage',
            'usage': 'internal',
            'is_quarantine_location': True
        })
        self.normal_dest_loc = self.env['stock.location'].create({
            'name': 'Standard Processing Floor',
            'usage': 'internal'
        })
        self.customer_loc = self.env['stock.location'].create({
            'name': 'External Customer Site',
            'usage': 'customer'
        })

        # Create product
        self.product = self.env['product.product'].create({
            'name': 'Test Herb Product',
            'type': 'consu',
            'is_storable': True
        })

        # Helper to create stocked carrier and avoid "cannot move empty package" exception
        def create_stocked_carrier(name, state):
            pkg = self.env['stock.package'].create({'name': name})
            self.env['stock.quant'].create({
                'product_id': self.product.id,
                'package_id': pkg.id,
                'location_id': self.source_loc.id,
                'quantity': 10.0
            })
            carrier = self.env['stock.matter.tracking'].create({
                'package_id': pkg.id,
                'carrier_state': state
            })
            return pkg, carrier

        # Create basic stock matter carriers representing genealogy tree: A -> (B, C) -> D
        self.pkg_a, self.carrier_a = create_stocked_carrier('PKG-A', 'done')
        self.pkg_b, self.carrier_b = create_stocked_carrier('PKG-B', 'idle')
        self.pkg_c, self.carrier_c = create_stocked_carrier('PKG-C', 'idle')
        self.pkg_d, self.carrier_d = create_stocked_carrier('PKG-D', 'idle')

        # Establish genealogy links
        # A -> B
        self.env['stock.matter.tracking.link'].create({
            'parent_id': self.carrier_a.id,
            'child_id': self.carrier_b.id,
            'transition_type': 'split'
        })
        # A -> C
        self.env['stock.matter.tracking.link'].create({
            'parent_id': self.carrier_a.id,
            'child_id': self.carrier_c.id,
            'transition_type': 'sequential'
        })
        # C -> D
        self.env['stock.matter.tracking.link'].create({
            'parent_id': self.carrier_c.id,
            'child_id': self.carrier_d.id,
            'transition_type': 'sequential'
        })

    def test_01_dfs_quarantine_propagation(self):
        """ Ensure a contamination incident on Carrier A automatically quarantines B, C, and D """
        incident = self.Incident.create({
            'source_carrier_id': self.carrier_a.id,
            'contamination_type': 'biological',
            'description': 'Detected biological pest contamination on A.'
        })
        
        # Trigger automatic reverse recall and propagation
        incident.action_quarantine_downstream()
        
        # Verify states: B, C, D must be quarantined!
        self.assertEqual(self.carrier_b.carrier_state, 'quarantine')
        self.assertEqual(self.carrier_c.carrier_state, 'quarantine')
        self.assertEqual(self.carrier_d.carrier_state, 'quarantine')
        
        # Source carrier is not quarantined automatically (retains done status)
        self.assertEqual(self.carrier_a.carrier_state, 'done')
        
        # Incident properties are updated
        self.assertEqual(incident.state, 'quarantined')
        self.assertIn(self.carrier_b.id, incident.affected_carrier_ids.ids)
        self.assertIn(self.carrier_c.id, incident.affected_carrier_ids.ids)
        self.assertIn(self.carrier_d.id, incident.affected_carrier_ids.ids)

    def test_02_quarantine_move_restrictions(self):
        """ Ensure quarantined carriers cannot be moved to non-quarantine locations """
        # Force set carrier_b state to quarantine
        self.carrier_b.with_context(bypass_carrier_transition_rules=True).write({'carrier_state': 'quarantine'})
        
        # Attempt to move to standard processing floor (not quarantine) -> ValidationError
        with self.assertRaises(ValidationError) as error:
            self.carrier_b.write({'location_id': self.normal_dest_loc.id})
        self.assertIn("GXP_QUARANTINE_LOCKDOWN", str(error.exception))

        # Successfully move to designated quarantine cage
        self.carrier_b.write({'location_id': self.quarantine_loc.id})
        self.assertEqual(self.carrier_b.location_id.id, self.quarantine_loc.id)

    def test_03_outbound_picking_quarantine_blockade(self):
        """ Ensure a picking validation fails if it contains quarantined carrier material """
        # Mark carrier_c as quarantined
        self.carrier_c.with_context(bypass_carrier_transition_rules=True).write({'carrier_state': 'quarantine'})

        # Mock outbound delivery picking
        picking_type = self.env['stock.picking.type'].search([('code', '=', 'outgoing')], limit=1)
        picking = self.env['stock.picking'].create({
            'partner_id': self.env['res.partner'].create({'name': 'Distributor'}).id,
            'picking_type_id': picking_type.id,
            'location_id': self.source_loc.id,
            'location_dest_id': self.customer_loc.id,
            'move_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'package_id': self.pkg_c.id,  # Points to quarantined PKG-C / Carrier C
                'quantity': 10.0,
                'location_id': self.source_loc.id,
                'location_dest_id': self.customer_loc.id,
            })]
        })

        # Validate picking -> must raise ValidationError
        with self.assertRaises(ValidationError) as error:
            picking.button_validate()
        self.assertIn("GXP_OUTBOUND_BLOCKED", str(error.exception))

    def test_05_cte_traversal_equivalence_and_rls(self):
        """ TDD: Verify PostgreSQL-level Recursive CTE is mathematically equivalent to Python-level BFS """
        # Downstream Equivalence
        cte_downstream = self.carrier_a.action_trace_downstream_cte()
        bfs_downstream = self.carrier_a.action_trace_downstream()
        
        self.assertEqual(cte_downstream.ids, bfs_downstream.ids, "Downstream CTE must be equivalent to BFS")
        self.assertIn(self.carrier_b, cte_downstream)
        self.assertIn(self.carrier_c, cte_downstream)
        self.assertIn(self.carrier_d, cte_downstream)

        # Upstream Equivalence
        cte_upstream = self.carrier_d.action_trace_upstream_cte()
        bfs_upstream = self.carrier_d.action_trace_upstream()
        
        self.assertEqual(cte_upstream.ids, bfs_upstream.ids, "Upstream CTE must be equivalent to BFS")
        self.assertIn(self.carrier_a, cte_upstream)
        self.assertIn(self.carrier_c, cte_upstream)

    def test_07_traversal_performance_benchmark(self):
        """ TDD: Benchmark CTE vs BFS over a 50-level deep parent-child lineage chain """
        import time
        
        # 1. Create a 50-level deep lineage chain: parent -> child
        current_carrier = self.carrier_d
        chain_carriers = [current_carrier]
        for i in range(50):
            # Create a stocked carrier
            pkg = self.env['stock.package'].create({'name': f'PKG-BENCH-{i}'})
            self.env['stock.quant'].create({
                'product_id': self.product.id,
                'package_id': pkg.id,
                'location_id': self.source_loc.id,
                'quantity': 10.0
            })
            child_carrier = self.env['stock.matter.tracking'].create({
                'package_id': pkg.id,
                'carrier_state': 'idle'
            })
            
            # Link current to child
            self.env['stock.matter.tracking.link'].create({
                'parent_id': current_carrier.id,
                'child_id': child_carrier.id,
                'transition_type': 'sequential'
            })
            current_carrier = child_carrier
            chain_carriers.append(child_carrier)
            
        # 2. Bench native Python BFS
        start_bfs = time.perf_counter()
        bfs_descendants = self.carrier_a.action_trace_downstream()
        bfs_duration = time.perf_counter() - start_bfs
        
        # 3. Bench PostgreSQL Recursive CTE
        start_cte = time.perf_counter()
        cte_descendants = self.carrier_a.action_trace_downstream_cte()
        cte_duration = time.perf_counter() - start_cte
        
        # Logs benchmark speed
        print(f"\n[BENCHMARK] Lineage Chain Depth=54 | Native BFS={bfs_duration:.6f}s, PostgreSQL CTE={cte_duration:.6f}s")
        self.assertLess(cte_duration, bfs_duration, "PostgreSQL CTE traversal must be faster than Python recursive-loop BFS")
