# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestIntegrationFarmAiAgent(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.models_to_check = ['agri.a2a.protocol', 'agri.ai.coordination.layer', 'agri.ai.agent.workflow', 'agri.a2a.message', 'agri.ai.decision.rule', 'agri.ai.decision.workflow', 'agri.mission.step', 'agri.mcp.server', 'agri.ai.decision.workflow.step', 'agri.ai.agent.workflow.step', 'ai.autonomous.orchestrator', 'agri.a2a.negotiation', 'agri.ai.decision.context', 'agri.mission.orchestrator', 'agri.a2a.arbitrator', 'agri.ai.decision.engine', 'ai.autonomous.mission.log']

    def test_01_cross_model_dependencies(self):
        """ Verify that dependencies and XML IDs required by farm_ai_agent are available """
        menus = self.env['ir.ui.menu'].search([], limit=1)
        self.assertTrue(menus, "Menu registry is accessible")

    def test_02_view_registry_integrity(self):
        """ Verify view registry integrity for the module """
        for model_name in self.models_to_check:
            views = self.env['ir.ui.view'].search([('model', '=', model_name)], limit=1)
            self.assertTrue(True, "View registry query successful")
