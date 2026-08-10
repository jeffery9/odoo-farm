# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic138(TransactionCase):
    """ BDD Test Suite for Epic 138: Epic 138 Autonomous Water Gating (农场智能水阀自动闭锁控制) """

    def setUp(self):
        super(TestEpic138, self).setUp()
        # Initialize basic test environments
        self.partner = self.env['res.partner'].create({'name': 'BDD Test Partner'})

    def test_01_water_pressure_overload_valve_cutoff_safety_gate(self):
        """
        Scenario: Water pressure overload valve cutoff safety gate
        Given a water supply valve registered on model "farm.water.valve" in status "open"
        When the telemetric sensor reports pressure exceeding 150.0 PSI (150.0磅每平方英寸) with a reading of 165.0 PSI
        Then the system must raise a ValidationError and transition status to "cutoff"
        And block any water flow validation with message "WATER_PRESSURE_OVERLOAD_BLOCK"
        """
        valve_model = self.env['farm.water.valve']
        
        # We expect a ValidationError raised naturally from the model constraints
        with self.assertRaises(ValidationError) as context:
            valve_model.create({
                'name': 'VALVE-MAIN-01',
                'status': 'open',
                'pressure_psi': 165.0 # Exceeds 150.0 PSI safety gate!
            })
            
        self.assertIn("WATER_PRESSURE_OVERLOAD_BLOCK", str(context.exception))
