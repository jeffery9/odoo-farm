# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
import json

class TestContinuousPipelineMixin(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Package = cls.env['stock.package']
        cls.Tracking = cls.env['stock.matter.tracking']
        
        cls.package1 = cls.Package.create({'name': 'PBR-TANK-01'})
        cls.tracking1 = cls.Tracking.create({
            'name': 'PBR-TRACK-01',
            'package_id': cls.package1.id
        })

    def test_01_continuous_pipeline_dna_propagation(self):
        """Verify dynamic mixing and DNA propagation over continuous flows."""
        # Assume two input pipelines feeding into this tracking object
        input_nodes = [
            {'name': 'INPUT-TANK-A', 'dna_integrity_score': 90.0},
            {'name': 'INPUT-TANK-B', 'dna_integrity_score': 80.0}
        ]
        weights = [200.0, 100.0]  # 2:1 ratio
        
        self.tracking1.propagate_continuous_genealogy(input_nodes, weights=weights)
        
        # Expected weighted average: (90*200 + 80*100) / 300 = 26000 / 300 = 86.666
        # Entropy penalty for multiple inputs: 0.95
        # Final: 86.666 * 0.95 = 82.333
        
        self.assertAlmostEqual(self.tracking1.dna_integrity_score, 82.333, places=2)
        
        # Verify JSON log
        log_data = json.loads(self.tracking1.upstream_pipeline_log)
        self.assertIn('sources', log_data)
        self.assertEqual(len(log_data['sources']), 2)
        self.assertEqual(log_data['sources'][0]['source'], 'INPUT-TANK-A')
        self.assertEqual(log_data['sources'][0]['dna'], 90.0)
