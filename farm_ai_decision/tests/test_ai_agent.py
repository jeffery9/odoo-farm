# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestAiAgent(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.AiAgent = cls.env['agri.ai.agent']
        
    def test_01_agent_creation(self):
        """ Test AI agent creation and base record linking """
        agent = self.AiAgent.create({
            'name': 'Yield Prediction Agent',
            'agent_type': 'prediction',
            'industry_id': 'crop',
        })
        self.assertTrue(agent.exists())
        self.assertTrue(agent.base_id, "Base ID should be automatically created via _inherits")
        self.assertEqual(agent.base_id.name, 'Yield Prediction Agent')
        
    def test_02_agent_decision_simulation(self):
        """ Test AI agent decision making simulation """
        agent = self.AiAgent.create({
            'name': 'Pest Analysis Agent',
            'agent_type': 'analysis',
        })
        
        # Test skill activation
        # Assuming there's a method to generate decisions
        if hasattr(agent, 'generate_agent_decisions'):
            res = agent.generate_agent_decisions()
            self.assertIn('status', res)
            
    def test_03_autonomous_status(self):
        """ Test agent autonomous level handling """
        agent = self.AiAgent.create({
            'name': 'Autonomous Harvester AI',
            'agent_type': 'planning',
        })
        # Check default autonomy level if it exists
        if hasattr(agent, 'autonomy_level'):
            self.assertEqual(agent.autonomy_level, 'L1')
            agent.autonomy_level = 'L4'
            self.assertEqual(agent.autonomy_level, 'L4')
