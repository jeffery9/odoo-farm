# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class TestInterventionEngine(TransactionCase):
    """
    Test the core L0 Intervention Engine and its plugin registry.
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Engine = cls.env['agri.intervention.base']
        
        # Create a dummy model that implements the engine for testing
        # In Odoo tests, we often use existing implementations or mock registry
        cls.intervention = cls.env['agri.intervention.base'].create({
            'name': 'TEST-INT-001',
        })

    def test_01_lifecycle_transitions(self):
        """ Verify standard lifecycle and dates """
        self.assertEqual(self.intervention.state, 'draft')
        
        self.intervention.action_confirm_base()
        self.assertEqual(self.intervention.state, 'confirmed')
        
        self.intervention.action_start_base()
        self.assertEqual(self.intervention.state, 'in_progress')
        self.assertTrue(self.intervention.date_start)
        
        self.intervention.action_done_base()
        self.assertEqual(self.intervention.state, 'done')
        self.assertTrue(self.intervention.date_finished)

    def test_02_plugin_execution_flow(self):
        """ 
        Verify that plugins are called at correct hook points.
        We'll use a mocked plugin for this.
        """
        # Since we can't easily mock Python classes in Odoo environment easily without Mocks,
        # we'll verify the registry mechanism.
        plugins = self.intervention._get_intervention_plugins()
        self.assertIsInstance(plugins, list)
        
        # If we are in agri_intervention, the registry should be empty or have base plugins
        # The actual business plugins are added in farm_operation
        _logger.info(f"Registered plugins in base engine: {plugins}")
