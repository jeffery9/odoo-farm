# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestAiDecision(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Irrigation = cls.env['agri.ai.irrigation.decision']
        cls.Location = cls.env['farm.location'].create({
            'name': 'Test Block 1',
            'usage': 'internal',
        })
        cls.Product = cls.env['product.template'].create({
            'name': 'Test Crop',
            'type': 'consu',
        })
        
    def test_01_irrigation_decision_logic(self):
        """ Test irrigation need calculation logic """
        # Case 1: Low moisture
        decision = self.Irrigation.create({
            'name': 'Drought Condition',
            'land_location_id': self.Location.id,
            'product_id': self.Product.id,
            'current_soil_moisture': 20.0, # < 30%
        })
        decision.calculate_irrigation_needs()
        self.assertEqual(decision.recommended_water_amount, 25.0)
        self.assertEqual(decision.priority, 'high')
        
        # Case 2: Medium moisture
        decision_med = self.Irrigation.create({
            'name': 'Moderate Condition',
            'land_location_id': self.Location.id,
            'product_id': self.Product.id,
            'current_soil_moisture': 40.0, # between 30 and 45
        })
        decision_med.calculate_irrigation_needs()
        self.assertEqual(decision_med.recommended_water_amount, 15.0)
        
    def test_02_decision_state_workflow(self):
        """ Test the recommendation application workflow """
        decision = self.Irrigation.create({
            'name': 'Standard Decision',
            'current_soil_moisture': 35.0,
        })
        self.assertEqual(decision.status, 'draft')
        
        decision.action_apply_recommendation()
        self.assertEqual(decision.status, 'applied')
        
        decision.action_reject_recommendation()
        self.assertEqual(decision.status, 'rejected')

    def test_03_base_mixin_inheritance(self):
        """ Test if decision model correctly inherits from AI base mixin """
        decision = self.Irrigation.create({'name': 'Mixin Test'})
        self.assertTrue(hasattr(decision, 'ai_confidence_score'))
        self.assertTrue(hasattr(decision, 'ai_status'))
        self.assertEqual(decision.ai_status, 'pending')
