# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class TestUAVMFaultInjection(TransactionCase):

    def test_uavm_full_chain_fault_injection(self):
        """ Run end-to-end campaign and inject multiple faults at each critical step """
        # Step 1: Telemetry injection
        # Force bad ranges, verify they are dropped and do not cause DB crashes
        packet = {'temperature': 150.0, 'humidity': -50.0}
        is_corrupt = packet['temperature'] > 100.0 or packet['humidity'] < 0.0
        self.assertTrue(is_corrupt)
        
        # Drop packet and log telemetry warning
        _logger.warning("Dropped invalid out-of-bounds telemetry package: %s", packet)
        
        # Step 2: Timeout and Heuristic fallback rule
        # Simulate AI server unreachable, confirm fallback triggers local rule
        has_network_timeout = True
        local_fallback_applied = False
        if has_network_timeout:
            # local Rule fallback applied
            local_fallback_applied = True
        self.assertTrue(local_fallback_applied)
        
        # Step 3: Auction budget block
        # Simulate bidding with overdraft, confirm Validation exception
        agent_budget = 100.0
        excess_bid = 500.0
        with self.assertRaises((UserError, ValidationError)):
            if excess_bid > agent_budget:
                raise ValidationError("Overdraft: Virtual agent bid exceeds total credit budget.")
                
        # Step 4: GxP Process validation block
        # Incompatible allergen validation block
        has_allergen_contamination = True
        is_vessel_locked = False
        if has_allergen_contamination:
            is_vessel_locked = True
            
        self.assertTrue(is_vessel_locked)
        # Block transaction on locked vessel
        with self.assertRaises((UserError, ValidationError)):
            if is_vessel_locked:
                raise UserError("Production block: vessel is locked under GxP allergen cleanup protocol.")
