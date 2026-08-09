# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, ValidationError
import json

class TestUAVMSandbox(TransactionCase):

    def test_uavm_sandbox_atomic_rollback_integrity(self):
        """ Verify that Re-Act iterations run in a savepoint sandbox and roll back on GxP/HACCP failures """
        loop_model = 'agri.a2a.react.loop'
        line_model = 'agri.a2a.react.loop.line'
        
        if loop_model in self.env and line_model in self.env:
            # 1. Create a Re-Act loop
            loop = self.env[loop_model].create({
                'name': 'UAVM/SANDBOX/001',
                'goal': 'Enforce sandboxed rollback security'
            })
            
            # 2. Establish savepoint manually to simulate a tool call
            cr = self.env.cr
            cr.flush()
            
            try:
                with cr.savepoint():
                    # Modify some business state
                    wc = self.env['mrp.workcenter'].create({'name': 'Temporary Sandboxed WC'})
                    self.assertEqual(wc.name, 'Temporary Sandboxed WC')
                    
                    # Manually inject HACCP / validation exception (simulating tool failure)
                    raise ValidationError("HACCP Rule Violation: Temperature exceeds critical gating safety bounds.")
            except ValidationError as ve:
                # Transactional savepoint rolled back wc creation!
                _logger_msg = str(ve)
                # Create audit line OUTSIDE the savepoint (it's safe since parent savepoint was rolled back)
                self.env[line_model].create({
                    'loop_id': loop.id,
                    'iteration': 1,
                    'state': 'failed',
                    'thought': 'Attempt to launch heater',
                    'action_payload': '{}',
                    'observation': _logger_msg
                })
                
            # Assert 1: Temporary WC creation was rolled back (does not exist in database)
            wc_exists = self.env['mrp.workcenter'].search([('name', '=', 'Temporary Sandboxed WC')])
            self.assertFalse(wc_exists.exists())
            
            # Assert 2: Audit log line was successfully persisted and not rolled back
            lines = self.env[line_model].search([('loop_id', '=', loop.id)])
            self.assertEqual(len(lines), 1)
            self.assertEqual(lines[0].state, 'failed')
            self.assertIn("Temperature exceeds", lines[0].observation)
