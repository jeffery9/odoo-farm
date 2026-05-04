# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestA2ACollaboration(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Coordination = cls.env['agri.ai.coordination.layer']
        
    def test_01_coordination_layer_creation(self):
        """ Test basic coordination layer setup """
        coord = self.Coordination.create({
            'name': 'Pest-Irrigation Sync',
            'coordination_type': 'vision_decision_integration',
            'result_aggregation_method': 'weighted_average',
        })
        self.assertTrue(coord.exists())
        self.assertEqual(coord.status, 'draft')
        
    def test_02_multi_service_linkage(self):
        """ Test linking multiple AI services to the coordination layer """
        coord = self.Coordination.create({
            'name': 'Full Automation Loop',
            'coordination_type': 'cross_module_workflow',
        })
        
        # Link a decision agent if available
        agent = self.env['agri.ai.agent'].create({
            'name': 'Planner Agent',
            'agent_type': 'planning',
        })
        coord.ai_decision_ids = [(4, agent.id)]
        
        # Link a vision service if available
        vision = self.env['agri.ai.pest.disease.detection'].create({
            'name': 'Pest Detector',
            'detection_type': 'pest',
        })
        coord.ai_vision_ids = [(4, vision.id)]
        
        self.assertEqual(len(coord.ai_decision_ids), 1)
        self.assertEqual(len(coord.ai_vision_ids), 1)

    def test_03_coordination_execution_workflow(self):
        """ Test coordination execution state changes """
        coord = self.Coordination.create({
            'name': 'Workflow Test',
            'coordination_type': 'cross_module_workflow',
        })
        
        if hasattr(coord, 'action_execute_coordination'):
            coord.action_execute_coordination()
            self.assertEqual(coord.status, 'completed')
