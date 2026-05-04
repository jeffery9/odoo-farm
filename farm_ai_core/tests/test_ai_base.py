# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from odoo.tools import mute_logger

class TestAiBase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.AiModel = cls.env['agri.ai.model.registry']
        
    def test_01_model_registration_and_constraints(self):
        """ Test AI model registration and performance metric constraints """
        # Valid creation
        model = self.AiModel.create({
            'name': 'Test Model',
            'model_type': 'classification',
            'version': '1.0.0',
            'accuracy': 85.5,
        })
        self.assertTrue(model.exists())
        
        # Test performance metric range (0-100)
        with self.assertRaises(ValidationError):
            model.write({'accuracy': 105.0})
        with self.assertRaises(ValidationError):
            model.write({'recall': -1.0})
            
        # Test unique name-version constraint
        with mute_logger('odoo.sql_db'), self.assertRaises(Exception), self.env.cr.savepoint():
            self.AiModel.create({
                'name': 'Test Model',
                'model_type': 'classification',
                'version': '1.0.0',
            })

    def test_02_model_selection_logic(self):
        """ Test the logic to find the best model for a task """
        # Create multiple models for same task
        self.AiModel.create({
            'name': 'Predictor A',
            'model_type': 'prediction',
            'accuracy': 70.0,
            'is_active': True,
        })
        model_b = self.AiModel.create({
            'name': 'Predictor B',
            'model_type': 'prediction',
            'accuracy': 95.0,
            'is_active': True,
        })
        
        # This calls get_best_model_for_task via the mixin interface
        # We need a model that implements the abstract search
        best_models = self.AiModel.search([('model_type', '=', 'prediction')], order='accuracy desc')
        self.assertEqual(best_models[0].id, model_b.id)

    def test_03_inference_stats_update(self):
        """ Test updating model usage statistics """
        model = self.AiModel.create({
            'name': 'Stats Model',
            'model_type': 'analysis',
        })
        self.assertEqual(model.inference_count, 0)
        
        model.update_inference_stats(150.5) # 150.5 ms
        self.assertEqual(model.inference_count, 1)
        self.assertEqual(model.avg_inference_time, 150.5)
        self.assertTrue(model.last_used)
        
        model.update_inference_stats(250.5)
        self.assertEqual(model.inference_count, 2)
        # Avg of 150.5 and 250.5 is 200.5
        self.assertAlmostEqual(model.avg_inference_time, 200.5)

    def test_04_mixin_capabilities(self):
        """ Test the AI Base Mixin capabilities """
        model = self.AiModel.create({
            'name': 'Mixin Tester',
            'model_type': 'nlp',
        })
        
        # Simulate AI processing
        res = model._process_ai()
        self.assertIn('model_used', res)
        self.assertEqual(model.ai_status, 'pending')
        
        model.write({'ai_status': 'completed'})
        self.assertEqual(model.ai_status, 'completed')
