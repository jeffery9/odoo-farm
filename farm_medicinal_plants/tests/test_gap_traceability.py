# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestGapTraceability(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        
        cls.ginseng = cls.env['product.product'].create({'name': 'Wild Mountain Ginseng', 'type': 'product'})
        
        # We need an HPLC quality point
        cls.hplc_point = cls.env['agri.quality.point'].create({
            'name': 'Ginsenoside Content HPLC Test',
            'test_type': 'hplc' # Assume this exists or is just a string
        })
        
        # We need a lot
        cls.lot = cls.env['stock.lot'].create({
            'name': 'LOT-GINSENG-001',
            'product_id': cls.ginseng.id,
            'company_id': cls.env.company.id
        })

    def test_01_gap_certification_flow(self):
        """
        Scenario 35: Medicinal Plants Active Ingredient Traceability
        1. Create a medicinal production order.
        2. Attempt to generate passport -> Fails (No GAP certification).
        3. Verify geographical origin (Daodi).
        4. Receive HPLC lab results with active ingredient > threshold.
        5. System auto-certifies GAP.
        6. Passport generation succeeds.
        """
        production = self.env['farm.medicinal.production'].create({
            'product_id': self.ginseng.id,
            'product_qty': 10.0,
            'target_compound_level': 5.0, # Require 5% ginsenosides
            'intervention_type': 'harvesting'
        })
        
        # Should fail initially
        with self.assertRaises(UserError):
            production.action_generate_passport()
            
        # 1. Geographic verification
        production.write({'is_daodi_verified': True})
        
        # 2. Lab Result
        qc = self.env['agri.quality.check'].create({
            'point_id': self.hplc_point.id,
            'lot_id': self.lot.id,
            'quality_state': 'pass',
            'measure': 6.2 # 6.2% active ingredient, beats 5.0% threshold
        })
        
        production.write({'hplc_lab_result_id': qc.id})
        
        # Assert auto-computation
        self.assertTrue(production.gap_certified, "Production should be GAP certified after lab results.")
        
        # Assert passport success
        self.assertTrue(production.action_generate_passport())

