# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
import logging

_logger = logging.getLogger(__name__)

class TestAiDisasterBridge(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True, test_mock_llm=True))
        
        # 1. Create a dummy product for intervention creation
        try:
            cls.env.ref('farm_disaster_risk.product_dummy_service')
        except ValueError:
            product = cls.env['product.product'].create({
                'name': 'Emergency Service',
                'type': 'service'
            })
            cls.env['ir.model.data'].create({
                'name': 'product_dummy_service',
                'module': 'farm_disaster_risk',
                'model': 'product.product',
                'res_id': product.id
            })

    def test_01_frost_disaster_ai_flow(self):
        """
        Flow:
        1. A frost disaster is logged.
        2. User requests AI strategy.
        3. LLM returns JSON strategy.
        4. System parses JSON and auto-generates a Protection intervention.
        """
        incident = self.env['farm.disaster.incident'].create({
            'disaster_type': 'frost',
            'intensity': 'severe',
            'description': 'Unexpected late spring frost hitting region A.'
        })
        
        _logger.info("Triggering AI Strategy for %s", incident.disaster_type)
        incident.action_request_ai_strategy()
        
        self.assertTrue(incident.ai_strategy_log, "AI strategy log should be populated.")
        self.assertTrue('Anti-Frost Spraying' in incident.ai_strategy_log, "Mock strategy should suggest anti-frost spraying.")
        
        self.assertTrue(incident.intervention_ids, "An intervention order should have been automatically created.")
        
        intervention = incident.intervention_ids[0]
        self.assertEqual(intervention.intervention_type, 'protection', "The parsed action_type should be 'protection'.")
        self.assertEqual(intervention.origin, incident.name, "Intervention origin should point to the disaster incident.")
        _logger.info("Successfully validated End-to-End AI Disaster Flow.")

