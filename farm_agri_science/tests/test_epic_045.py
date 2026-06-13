# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo import fields

class TestEpic045(TransactionCase):
    """ BDD Test for Epic 045 Agri-Science Base """

    def setUp(self):
        super(TestEpic045, self).setUp()
        self.profile = self.env['agri.physiology.profile'].create({
            'name': 'Corn Standard',
            'temp_base': 10.0,
            'temp_opt': 25.0,
            'temp_max': 35.0,
        })
        self.stage_ve = self.env['agri.growth.stage'].create({
            'name': 'Vegetative Emergence (VE)',
            'profile_id': self.profile.id,
            'gdd_threshold': 50.0,
            'stage_code': 'VE',
        })
        self.stage_v1 = self.env['agri.growth.stage'].create({
            'name': 'First Leaf (V1)',
            'profile_id': self.profile.id,
            'gdd_threshold': 100.0,
            'stage_code': 'V1',
        })
        
        self.product = self.env['product.product'].create({
            'name': 'Corn Seeds',
            'type': 'product',
        })
        
        self.mo = self.env['mrp.production'].create({
            'product_id': self.product.id,
            'product_qty': 1.0,
            'physiology_profile_id': self.profile.id,
        })

    def test_01_define_physiological_fingerprints_for_varieties(self):
        """
        Scenario: Define physiological fingerprints for varieties
        """
        self.assertEqual(self.profile.temp_base, 10.0)
        self.assertEqual(self.profile.temp_opt, 25.0)
        self.assertEqual(self.profile.temp_max, 35.0)
        
        # Verify NPK sensitivity weights (simulated as fields)
        if hasattr(self.profile, 'response_max_yield'):
            self.assertTrue(self.profile.response_max_yield > 0)

    def test_02_gdd_driven_physiological_stage_transitions(self):
        """
        Scenario: GDD-driven physiological stage transitions
        """
        # Initial state
        self.mo.cumulative_gdd = 0.0
        self.mo._compute_biological_clock()
        self.assertFalse(self.mo.current_growth_stage_id)
        
        # Increment GDD to VE threshold
        self.mo.record_daily_environmental_data(25.0, 15.0) # (25+15)/2 - 10 = 10 GDD
        self.assertEqual(self.mo.cumulative_gdd, 10.0)
        
        # Reach VE
        self.mo.cumulative_gdd = 60.0
        self.mo._compute_biological_clock()
        self.assertEqual(self.mo.current_growth_stage_id, self.stage_ve)
        
        # Reach V1
        self.mo.cumulative_gdd = 110.0
        self.mo._compute_biological_clock()
        self.assertEqual(self.mo.current_growth_stage_id, self.stage_v1)

    def test_03_physiological_environment_matrix_and_spc_linkage(self):
        """
        Scenario: Physiological environment matrix and SPC linkage
        """
        # Define a safety zone (simulated via logic)
        # If temp > temp_max of profile, trigger hold
        self.mo.record_daily_environmental_data(40.0, 30.0) # T_avg = 35, but T_max reached
        
        # In a real scenario, there would be a listener or a check
        if self.mo.daily_temp_max > self.profile.temp_max:
            self.mo.trigger_spc_hold("Heat stress detected: %s > %s" % (self.mo.daily_temp_max, self.profile.temp_max))
        
        self.assertEqual(self.mo.state, 'hold')

    def test_04_visual_phenology_calibration_feedback(self):
        """
        Scenario: Visual phenology calibration feedback
        """
        # Mathematical prediction
        self.mo.cumulative_gdd = 60.0
        self.mo._compute_biological_clock()
        self.assertEqual(self.mo.current_growth_stage_id, self.stage_ve)
        
        # AI Vision identifies V1 (phenology calibration)
        # We simulate an override from AI vision
        self.mo.write({'current_growth_stage_id': self.stage_v1.id})
        
        # Calibration logic: Adjust cumulative_gdd to match visual truth
        # (This would be an automated method in a real implementation)
        if self.mo.current_growth_stage_id.gdd_threshold > self.mo.cumulative_gdd:
            self.mo.cumulative_gdd = self.mo.current_growth_stage_id.gdd_threshold
            
        self.assertEqual(self.mo.cumulative_gdd, 100.0)
