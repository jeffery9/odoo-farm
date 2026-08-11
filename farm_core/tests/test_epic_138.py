# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic138(BddTransactionCase):
    """ BDD Test Suite for Epic 138: Epic 138 Autonomous Water Gating (农场智能水阀自动闭锁控制) """

    def setUp(self):
        super(TestEpic138, self).setUp()

    def test_01_water_pressure_overload_valve_cutoff_safety_gate(self):
        """
        Scenario: Water pressure overload valve cutoff safety gate
        Given a water supply valve registered on model "farm.water.valve" in status "open"
        When the telemetric sensor reports pressure exceeding 150.0 PSI (150.0磅每平方英寸) with a reading of 165.0 PSI
        Then the system must raise a ValidationError and transition status to "cutoff"
        And block any water flow validation with message "WATER_PRESSURE_OVERLOAD_BLOCK"
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a water supply valve registered on model "farm.water.valve" in status "open"',
            'When the telemetric sensor reports pressure exceeding 150.0 PSI (150.0磅每平方英寸) with a reading of 165.0 PSI',
            'Then the system must raise a ValidationError and transition status to "cutoff"',
            'And block any water flow validation with message "WATER_PRESSURE_OVERLOAD_BLOCK"'
        ])
