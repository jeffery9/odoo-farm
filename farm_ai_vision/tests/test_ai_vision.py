# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
import base64
import json

class TestAiVision(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.VisionBase = cls.env['agri.ai.vision.base']
        
    def test_01_vision_record_creation(self):
        """ Test basic vision record creation """
        vision = self.VisionBase.create({
            'name': 'Test Leaf Analysis',
            'model_type': 'pest_detection',
        })
        self.assertTrue(vision.exists())
        self.assertEqual(vision.status, 'draft')
        
    def test_02_image_processing_workflow(self):
        """ Test the full image processing workflow and metadata capture """
        # Create a small dummy image
        image_data = base64.b64encode(b'dummy_image_content')
        
        vision = self.VisionBase.create({
            'name': 'Leaf Health Check',
            'image': image_data,
            'model_type': 'health_analysis',
        })
        
        # Trigger processing
        vision.action_process_image()
        
        # Verify results
        self.assertEqual(vision.status, 'completed')
        self.assertTrue(vision.analysis_result)
        self.assertTrue(vision.ai_confidence_score > 0)
        self.assertTrue(vision.ai_processing_time > 0)
        self.assertEqual(vision.ai_model_used, 'Default Vision Model')
        
        # Verify JSON output
        output = json.loads(vision.output_data)
        self.assertIn('classification', output)
        self.assertIn('features_detected', output)

    def test_03_base_mixin_integration(self):
        """ Test if vision model correctly integrates AI base mixin fields """
        vision = self.VisionBase.create({'name': 'Integration Test'})
        self.assertTrue(hasattr(vision, 'ai_confidence_score'))
        # Default value from mixin is 50.0, but base model might override
        self.assertEqual(vision.ai_confidence_score, 50.0)
