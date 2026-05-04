# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestAiBase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.AiModel = cls.env['agri.ai.model.registry']
        
    def test_01_model_registration(self):
        """ Test AI model registration in the registry """
        model = self.AiModel.create({
            'name': 'Test GPT-4 Agri',
            'model_type': 'nlp',
            'version': '1.0.0',
            'is_active': True,
        })
        self.assertTrue(model.exists())
        self.assertEqual(model.ai_status, 'pending')
        
    def test_02_ai_processing_simulation(self):
        """ Test AI processing simulation on a model """
        model = self.AiModel.create({
            'name': 'Analyzer Model',
            'model_type': 'analysis',
        })
        
        # Test basic field updates
        model.write({
            'ai_input_data': '{"test": "input"}',
            'ai_status': 'processing'
        })
        self.assertEqual(model.ai_status, 'processing')
        
        model.write({
            'ai_output_data': '{"result": "success"}',
            'ai_status': 'completed',
            'ai_confidence_score': 95.5
        })
        self.assertEqual(model.ai_status, 'completed')
        self.assertEqual(model.ai_confidence_score, 95.5)

    def test_03_mixin_interfaces(self):
        """ Test if mixin interfaces are correctly exposed """
        model = self.AiModel.create({
            'name': 'Interface Test',
            'model_type': 'analysis',
        })
        # Check if methods from mixins are available
        self.assertTrue(hasattr(model, 'action_process_with_ai'))
        self.assertTrue(hasattr(model, 'get_ai_system_health'))
