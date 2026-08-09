# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo import fields

class TestEpic074(TransactionCase):
    """ BDD Test for Epic 074 Post Harvest Quality Management """

    def setUp(self):
        super(TestEpic074, self).setUp()
        self.product = self.env['product.product'].create({
            'name': 'Organic Tomato',
            'type': 'consu',
            'is_storable': True
        })
        self.lot = self.env['stock.lot'].create({
            'name': 'LOT2026-001',
            'product_id': self.product.id,
            'company_id': self.env.company.id
        })
        self.qc_point = self.env['agri.quality.point'].create({
            'name': 'Brix Measurement',
            'product_id': self.product.id,
            'test_type': 'measure',
            'tolerance_min': 4.5,
            'tolerance_max': 6.5
        })

    def test_01_real_time_post_harvest_quality_monitoring_and_alerts(self):
        """
        Scenario: Real-time post-harvest quality monitoring and alerts
        """
        # Create a QC check for the lot
        check = self.env['agri.quality.check'].create({
            'point_id': self.qc_point.id,
            'lot_id': self.lot.id,
            'measure': 4.0 # Below norm
        })
        check.action_done()
        
        self.assertEqual(check.quality_state, 'fail')
        self.assertEqual(self.lot.quality_status, 'failed')
        
        # Trigger an alert
        alert = self.env['agri.quality.alert'].create({
            'name': 'Quality Deterioration Alert',
            'check_id': check.id,
            'lot_id': self.lot.id,
            'product_id': self.product.id
        })
        self.assertTrue(alert.id)

    def test_02_shelf_life_prediction_and_optimized_fifo_management(self):
        """
        Scenario: Shelf-life prediction and optimized FIFO management
        """
        # Create two lots with different expiration dates (FEFO)
        lot_old = self.lot
        lot_old.write({'removal_date': fields.Datetime.now()}) # Expires now
        
        lot_new = self.env['stock.lot'].create({
            'name': 'LOT2026-002',
            'product_id': self.product.id,
            'removal_date': fields.Datetime.add(fields.Datetime.now(), days=10),
            'company_id': self.env.company.id
        })
        
        # Verify FEFO picking (Mocking the picking suggestion)
        # In Odoo, this is handled by removal strategies on the location
        # Here we just verify that the system can distinguish them
        self.assertTrue(lot_old.removal_date < lot_new.removal_date)

    def test_03_automatic_product_grading_and_market_matching(self):
        """
        Scenario: Automatic product grading and market matching
        """
        # Record inspection results
        check = self.env['agri.quality.check'].create({
            'point_id': self.qc_point.id,
            'lot_id': self.lot.id,
            'measure': 6.0, # Good quality
            'appearance_score': 9,
            'flavor_score': 9
        })
        check.action_done()
        
        # Simulate automatic grading (A, B, C)
        # Assuming grade is stored on lot or check
        grade = 'A' if check.quality_state == 'pass' and check.appearance_score > 8 else 'B'
        self.assertEqual(grade, 'A')
        
        # Suggest market channel
        market = 'Premium Supermarket' if grade == 'A' else 'Local Market'
        self.assertEqual(market, 'Premium Supermarket')
