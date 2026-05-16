# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
import logging

_logger = logging.getLogger(__name__)

class TestSmartRecallFlow(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True, test_mock_llm=True))
        
        # 1. Base Setup
        cls.apple = cls.env['product.product'].create({'name': 'Fuji Apples', 'tracking': 'lot'})
        
        # Parcels
        cls.parcel_a = cls.env['farm.location'].create({'name': 'Parcel A - Toxic Soil'})
        cls.parcel_b = cls.env['farm.location'].create({'name': 'Parcel B - Safe Soil'})
        
        # Lots
        cls.lot_bad_1 = cls.env['stock.lot'].create({'name': 'LOT-A-01', 'product_id': cls.apple.id, 'company_id': cls.env.company.id})
        cls.lot_bad_2 = cls.env['stock.lot'].create({'name': 'LOT-A-02', 'product_id': cls.apple.id, 'company_id': cls.env.company.id})
        cls.lot_good = cls.env['stock.lot'].create({'name': 'LOT-B-01', 'product_id': cls.apple.id, 'company_id': cls.env.company.id})

        # Interventions linking Lots to Parcels
        cls.env['mrp.production'].create({'product_id': cls.apple.id, 'product_qty': 1.0, 'lot_producing_id': cls.lot_bad_1.id, 'land_parcel_id': cls.parcel_a.id, 'intervention_type': 'harvesting'})
        cls.env['mrp.production'].create({'product_id': cls.apple.id, 'product_qty': 1.0, 'lot_producing_id': cls.lot_bad_2.id, 'land_parcel_id': cls.parcel_a.id, 'intervention_type': 'harvesting'})
        cls.env['mrp.production'].create({'product_id': cls.apple.id, 'product_qty': 1.0, 'lot_producing_id': cls.lot_good.id, 'land_parcel_id': cls.parcel_b.id, 'intervention_type': 'harvesting'})

        # Quality Control Setup
        cls.qc_point = cls.env['agri.quality.point'].create({'name': 'Pesticide Residue Check'})

    def test_01_smart_recall_execution(self):
        """
        Scenario:
        1. QC on LOT-A-01 fails due to pesticide residue.
        2. QC Inspector triggers an Emergency Recall.
        3. Trace engine identifies 'Parcel A' as the source.
        4. Trace engine sweeps up LOT-A-02 as well because it shares the same source parcel.
        5. LOT-B-01 is safely ignored.
        6. AI drafts a PR Notice.
        """
        # Step 1: Failed QC
        qc = self.env['agri.quality.check'].create({
            'point_id': self.qc_point.id,
            'lot_id': self.lot_bad_1.id,
            'quality_state': 'fail',
            'measure': 5.5 # Beyond norm
        })
        
        # Step 2: Trigger Recall
        recall = self.env['farm.supply.recall'].create({
            'triggering_qc_id': qc.id
        })
        
        # Step 3 & 4: Execute Engine
        recall.action_execute_recall()
        
        self.assertEqual(recall.state, 'active')
        self.assertEqual(len(recall.affected_location_ids), 1, "Should have traced back to exactly one parcel.")
        self.assertEqual(recall.affected_location_ids[0].id, self.parcel_a.id, "Must identify Parcel A as the source.")
        
        self.assertEqual(len(recall.affected_lot_ids), 2, "Should have quarantined exactly two lots (LOT-A-01 and sibling LOT-A-02).")
        self.assertIn(self.lot_bad_2.id, recall.affected_lot_ids.ids, "Sibling lot from the same toxic parcel must be quarantined.")
        self.assertNotIn(self.lot_good.id, recall.affected_lot_ids.ids, "Lots from safe parcels must not be quarantined.")
        
        # Step 6: Verify AI PR Notice
        self.assertTrue(recall.ai_pr_draft, "AI must have drafted a PR notice.")
        self.assertIn('URGENT PRODUCT RECALL', recall.ai_pr_draft)
        self.assertIn('quarantined 2 batches', recall.ai_pr_draft, "Notice must reflect the exact blast radius of the recall.")

