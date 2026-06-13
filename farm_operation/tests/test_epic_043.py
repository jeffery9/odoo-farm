# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo import fields
from datetime import datetime

class TestEpic043(TransactionCase):
    """ BDD Test for Epic 043 Agri-Precision Bridge Core """

    @classmethod
    def setUpClass(cls):
        super(TestEpic043, cls).setUpClass()
        cls.Production = cls.env['mrp.production']
        cls.Product = cls.env['product.product']
        cls.Lot = cls.env['stock.lot']
        
        cls.product = cls.Product.create({
            'name': 'Test Agri Product',
            'type': 'consu',
            'tracking': 'lot'
        })
        
        cls.location_src = cls.env.ref('stock.stock_location_stock')
        cls.location_dest = cls.env.ref('stock.stock_location_output')

    def setUp(self):
        super(TestEpic043, self).setUp()
        # Initialize generic models for testing
        self.partner = self.env['res.partner'].create({'name': 'Test Partner'})
        self.product = self.env['product.product'].create({'name': 'Test Product', 'type': 'consu'})

        self.production = self.Production.create({
            'product_id': self.product.id,
            'product_qty': 100.0,
            'product_uom_id': self.product.uom_id.id,
            'location_src_id': self.location_src.id,
            'location_dest_id': self.location_dest.id,
        })

    def test_01_dynamic_yield_uncertainty_handling_and_calibration(self):
        """ Scenario: Dynamic yield uncertainty handling and calibration """
        # Initial qty is 100
        self.assertEqual(self.production.product_qty, 100.0)
        
        # Calibration event
        new_qty = 85.0
        self.production.action_update_yield_estimate(new_qty)
        
        self.assertEqual(self.production.product_qty, 85.0, "Yield should be updated to 85.0")
        self.assertTrue(self.production.last_metrology_date, "Last metrology date should be recorded")

    def test_02_product_grading_and_stock_lot_integration(self):
        """ Scenario: Product grading and stock lot integration """
        # Set intervention type to harvesting for grading logic
        self.production.intervention_type = 'harvesting'
        self.production.grade_a_qty = 80.0
        self.production.grade_b_qty = 20.0
        
        # Confirm and start
        self.production.action_confirm()
        self.production.action_assign()
        self.production.action_start_work()
        
        # Complete intervention (triggers harvest grading plugin)
        self.production.action_stop_work()
        
        # Check if graded lots were created
        lots = self.Lot.search([('product_id', '=', self.product.id)])
        grades = lots.mapped('quality_grade')
        self.assertIn('grade_a', grades)
        self.assertIn('grade_b', grades)

    def test_03_intervention_mechanism_and_corrective_skill_application(self):
        """ Scenario: Intervention mechanism and corrective skill application """
        initial_count = self.production.intervention_count
        
        # Trigger an IoT-based intervention
        self.production.action_trigger_iot_based_intervention("Critical: Temperature too high")
        
        self.assertEqual(self.production.intervention_count, initial_count + 1, "Intervention count should increment")
        self.assertEqual(self.production.iot_status, 'critical', "IoT status should be set to critical")

    def test_04_iot_integration_bridge_and_sensor_driven_intervention(self):
        """ Scenario: IoT integration bridge and sensor-driven intervention """
        # Normal status
        self.production.iot_status = 'normal'
        
        # Trigger warning
        self.production.action_trigger_iot_based_intervention("Warning: Humidity deviation")
        self.assertEqual(self.production.iot_status, 'warning', "IoT status should be warning")
        
        # Trigger critical
        self.production.action_trigger_iot_based_intervention("Emergency: Leak detected")
        self.assertEqual(self.production.iot_status, 'critical', "IoT status should be critical")
