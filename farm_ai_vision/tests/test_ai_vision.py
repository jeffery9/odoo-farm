# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
import base64

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
        
    def test_02_image_processing_simulation(self):
        """ Test image processing simulation """
        # Create a small dummy image
        image_data = base64.b64encode(b'dummy_image_content')
        
        vision = self.VisionBase.create({
            'name': 'Leaf Health Check',
            'image': image_data,
            'model_type': 'health_analysis',
        })
        
        # Trigger processing
        vision.action_process_image()
        
        self.assertIn(vision.status, ['completed', 'processing'])
        if vision.status == 'completed':
            self.assertTrue(vision.analysis_result)
