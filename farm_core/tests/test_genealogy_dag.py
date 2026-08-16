# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError

@tagged('post_install', '-at_install')
class TestGenealogyDAG(TransactionCase):

    def setUp(self):
        super(TestGenealogyDAG, self).setUp()
        self.carrier_a = self.env['stock.matter.tracking'].create({'name': 'CARRIER-A', 'dna_integrity_score': 100.0})
        self.carrier_b = self.env['stock.matter.tracking'].create({'name': 'CARRIER-B', 'dna_integrity_score': 90.0})
        self.carrier_c = self.env['stock.matter.tracking'].create({'name': 'CARRIER-C'})

    def test_sequential_link_dna_decay(self):
        """ Verify sequential linkage decays DNA by 1% """
        self.env['stock.matter.tracking.link'].create({
            'parent_id': self.carrier_a.id,
            'child_id': self.carrier_c.id,
            'link_type': 'sequential'
        })
        self.assertAlmostEqual(self.carrier_c.dna_integrity_score, 99.0, places=2)

    def test_blending_link_dna_decay(self):
        """ Verify blending multi-source linkage computes average DNA minus 5% """
        # Link C to A
        self.env['stock.matter.tracking.link'].create({
            'parent_id': self.carrier_a.id,
            'child_id': self.carrier_c.id,
            'link_type': 'blending'
        })
        # Link C to B (triggering multi-source)
        self.env['stock.matter.tracking.link'].create({
            'parent_id': self.carrier_b.id,
            'child_id': self.carrier_c.id,
            'link_type': 'blending'
        })
        # Expected: average(100.0, 90.0) = 95.0. Decayed = 95.0 * 0.95 = 90.25
        self.assertAlmostEqual(self.carrier_c.dna_integrity_score, 90.25, places=2)

    def test_topological_sort_cycle_prevention(self):
        """ Verify circular linkage is correctly blocked with ValidationError """
        self.env['stock.matter.tracking.link'].create({
            'parent_id': self.carrier_a.id,
            'child_id': self.carrier_b.id,
            'link_type': 'sequential'
        })
        self.env['stock.matter.tracking.link'].create({
            'parent_id': self.carrier_b.id,
            'child_id': self.carrier_c.id,
            'link_type': 'sequential'
        })
        # Linking C back to A should fail
        with self.assertRaises(ValidationError):
            self.env['stock.matter.tracking.link'].create({
                'parent_id': self.carrier_c.id,
                'child_id': self.carrier_a.id,
                'link_type': 'sequential'
            })
